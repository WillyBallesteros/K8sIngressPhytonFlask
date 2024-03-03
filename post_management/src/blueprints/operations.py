from flask import Flask, jsonify, request, Blueprint
from datetime import datetime
from ..commands.create import CreatePost
from ..commands.query import QueryPost
from ..commands.user import QueryUser
from ..commands.delete import DeletePost
from ..commands.reset import ResetPost
from ..utils.utils import are_consecutive_dates, get_info_token, is_boolean_and_value, is_uuid_valid, get_valid_id_route, parse_datetime, is_future_date
import os
import requests
import logging

operations_blueprint = Blueprint('operations', __name__)


def get_info_user(auth_header):
    info_user = QueryUser(auth_header).execute()
    return info_user

def common_validations(auth_header):

    if not auth_header or not auth_header.startswith('Bearer '):
        return "", 403

    info_token = get_info_token(auth_header)
    if not info_token:
        return "", 401

@operations_blueprint.route('/posts', methods=['POST'])
def create():
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return validations

    json_data = request.get_json(force=True)
    routeId = json_data.get('routeId')
    expire_at_str = json_data.get('expireAt')

    if not routeId:
        return "", 400
    if not expire_at_str:
        return "", 400
    if not is_uuid_valid(routeId) :
        return "", 400

    expireAt = None
    if expire_at_str:
        expireAt = parse_datetime(expire_at_str)
        if expireAt is None:
            return jsonify({"msg": "La fecha expiración no es válida"}), 412
        if expireAt <= datetime.utcnow():
            return jsonify({"msg": "La fecha expiración no es válida"}), 412
    logging.warning(f'auth_header {auth_header}')
    userId = get_info_user(auth_header)['id']
    if not userId:
        return "", 400
    if not is_uuid_valid(userId) :
        return "", 400

    post = CreatePost(userId, routeId, expireAt).execute()

    return jsonify({
        "id": str(post.id),
        "userId": post.userId,
        "createdAt": post.createdAt
    }), 201


@operations_blueprint.route('/rf003/posts', methods=['POST'])
def create_post_rf003():
    auth_header = request.headers.get('Authorization')
    validation_response = common_validations(auth_header)
    if validation_response:
        return validation_response

    user_id = get_info_user(auth_header)['id']
    json_data = request.get_json(force=True)

    required_fields = ['flightId', 'expireAt', 'plannedStartDate', 'plannedEndDate', 'origin', 'destiny', 'bagCost']
    for field in required_fields:
        if field not in json_data or not json_data[field]:
            return "", 400

    expire_at = json_data.get('expireAt')
    planned_start_date = json_data.get('plannedStartDate')
    planned_end_date = json_data.get('plannedEndDate')
    flight_id = json_data.get('flightId')

    if not is_future_date(expire_at) or not is_future_date(planned_start_date) or not is_future_date(planned_end_date):
        return jsonify({"msg": "La fecha expiración no es válida"}), 412

    if not are_consecutive_dates(planned_start_date, planned_end_date):
        return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412

    routes_service_url = f"http://localhost:3002/routes?flight={flight_id}"
    headers = {"Authorization": auth_header}

    try:
        response = requests.get(routes_service_url, headers=headers)
        if response.status_code == 201:
            routes = response.json()
            id_trayecto_valido = get_valid_id_route(routes, json_data)
            if id_trayecto_valido:
                posts_response = QueryPost(route_id=id_trayecto_valido, owner=user_id).execute()
                posts_list = posts_response.get_json()
                if not posts_list:
                    new_post = CreatePost(user_id, id_trayecto_valido, expire_at).execute()
                else:
                    return jsonify({"msg": "El usuario ya tiene una publicación para la misma fecha"}), 412
            else:
                origin_airport_code = json_data['origin']['airportCode']
                origin_country = json_data['origin']['country']
                destiny_airport_code = json_data['destiny']['airportCode']
                destiny_country = json_data['destiny']['country']
                bag_cost = json_data.get('bagCost')

                payload = {
                    "flightId": flight_id,
                    "sourceAirportCode": origin_airport_code,
                    "sourceCountry": origin_country,
                    "destinyAirportCode": destiny_airport_code,
                    "destinyCountry": destiny_country,
                    "bagCost": bag_cost,
                    "plannedStartDate": planned_start_date,
                    "plannedEndDate": planned_end_date
                }
                urlRoutes = "http://route_management:3002/routes"
                resultado = requests.post(urlRoutes, json=payload, headers=headers)
                if resultado.status_code == 201:
                    data = resultado.json()
                    trayecto_id = data.get("id")
                    new_post = CreatePost(user_id, trayecto_id, expire_at).execute()
                else:
                    return "", 404
        else:
            return "", 404
    except requests.exceptions.RequestException as e:
        return "", 400

    return jsonify({
        "data": {
            "id": str(new_post.id),
            "userId": user_id,
            "createdAt": new_post.createdAt.isoformat(),
            "expireAt": new_post.expireAt,
            "route": {
                "id": flight_id,
                "createdAt": new_post.createdAt.isoformat(),
            }
        },
        "msg": "Publicación creada exitosamente"
    }), 201


@operations_blueprint.route('/posts', methods=['GET'])
def get():
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return validations

    try:
        expire = request.args.get('expire')
        if expire != None:
            expire = is_boolean_and_value( expire )
    except ValueError as e:
        return "", 400

    route_id = request.args.get('route')
    owner = request.args.get('owner')

    #Valido los campos
    if not route_id is None:
        if len(route_id) < 1 or not is_uuid_valid(route_id):
            return "", 400

    if not owner is None:
        if len(owner) < 1:
            return "", 400

    if owner == 'me':
        owner = get_info_user(auth_header)['id']
    if owner is not None:
        if not is_uuid_valid(owner) :
            return "", 400

    posts = QueryPost(expire, route_id, owner).execute()
    return posts

@operations_blueprint.route('/posts/<string:id>', methods=['GET'])
def get_post_id(id):

    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return validations

    if not is_uuid_valid(id) :
        return "", 400

    post = QueryPost(id=id).execute()
    post_result = post.get_json()
    if not len(post_result) > 0:
         return "", 404

    return post_result[0]

@operations_blueprint.route('/posts/<string:id>', methods=['DELETE'])
def delete_post(id):
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return validations

    if not is_uuid_valid(id):
        return "", 400

    execute = DeletePost(id).execute()
    if execute == 200:
        return jsonify({"msg": "la publicación fue eliminada"}), 200
    else:
        return "", 404

@operations_blueprint.route('/posts/ping', methods = ['GET'])
def ping():
    return "pong"

@operations_blueprint.route('/posts/reset', methods = ['POST'])
def reset():
    ResetPost().execute()

    return jsonify({"msg": "Todos los datos fueron eliminados"})