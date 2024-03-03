from flask import Flask, jsonify, request, Blueprint
from datetime import datetime

from ..commands.delete_compensation import DeleteCompensation
from ..commands.create_compensation import CreateCompensation
from ..commands.execute_compensation import CompensateSagaOperations
from ..commands.user import QueryUser
from ..utils.utils import are_consecutive_dates, get_info_token, is_boolean_and_value, is_uuid_valid, get_valid_id_route, parse_datetime, is_future_date
from . import post_url, route_url, user_url
import os
import requests
import logging
import uuid

operations_blueprint = Blueprint('operations', __name__)
logger = logging.getLogger(__name__)

def get_info_user(auth_header, user_url):
    info_user = QueryUser(auth_header, user_url).execute()
    logger.error(f"Se ejecuta la busqueda de usuario dentro de get_info_user con info_user: {info_user}")
    return info_user
def common_validations(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.error(f"Se presento un error validando el auth_header: {auth_header}")
        return "", 403

    info_token = get_info_token(auth_header)
    if not info_token:
        logger.error(f"Se presento un error validando el info_token: {info_token}")
        return "", 401

@operations_blueprint.route('/rf003/posts', methods=['POST'])
def create_post_rf003():
    transaction_id = str(uuid.uuid4())
    logger.error(f"Comienza el proceso de creacion de post con transactionId: {transaction_id}")
    auth_header = request.headers.get('Authorization')

    logger.error(f"Comienza el proceso de validacion de header con auth_header: {auth_header}")
    validation_response = common_validations(auth_header)
    if validation_response:
        return validation_response

    logger.error(f"Comienza el proceso de validacion de usuario")
    user_id = get_info_user(auth_header, user_url)['id']
    json_data = request.get_json(force=True)


    logger.error(f"Comienza el proceso de validacion de datos requeridos")
    required_fields = ['flightId', 'expireAt', 'plannedStartDate', 'plannedEndDate', 'origin', 'destiny', 'bagCost']
    for field in required_fields:
        if field not in json_data or not json_data[field]:
            logger.error(f"No están todos los datos requeridos: {required_fields}")
            return "", 400

    expire_at = json_data.get('expireAt')
    planned_start_date = json_data.get('plannedStartDate')
    planned_end_date = json_data.get('plannedEndDate')
    flight_id = json_data.get('flightId')

    logger.error(f"Comienza el proceso de validacion de fechas")
    if not is_future_date(expire_at) or not is_future_date(planned_start_date) or not is_future_date(planned_end_date):
        logger.error(f"La fecha expiración no es válida: {expire_at}")
        return jsonify({"msg": "La fecha expiración no es válida"}), 412

    if not are_consecutive_dates(planned_start_date, planned_end_date):
        logger.error(f"Las fechas del trayecto no son válidas: {planned_start_date} , {planned_end_date} ")
        return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412

    logger.error(f"Comienza el proceso de creación de post")
    try:
        logger.error(f"Comienza el proceso de busqueda de ruta")
        route_id = search_route(json_data, auth_header, route_url)
        logger.error(f"Se realiza la busqueda de la ruta y retorna un routeId: {route_id}")
        if not route_id:
            logger.error(f"No se encontro la ruta, se procede a crearla.")
            route_id = create_route(json_data, auth_header, route_url, transaction_id)

        logger.error(f"Se realiza la creacion de la ruta y retorna un routeId: {route_id}")
        posts = query_external_post(user_id, route_id, auth_header, post_url)
        logger.error(f"Se realiza la busqueda de publicaciones por usuario y routeId: {route_id}, userId: {user_id} y retorna posts: {posts}")
        if posts:
            logger.error(f"Se encuentran publicaciones las publicaciones: {posts}")
            return jsonify({"msg": "El usuario ya tiene una publicación para la misma fecha"}), 412

        logger.error(f"No se encuentraron publicaciones por usuario y routeId: {route_id}, userId: {user_id}, se procede a crear la publicación.")

        new_post = create_external_post(user_id, route_id, json_data, auth_header, post_url, transaction_id)

        logger.error(f"Se crea la publicación con los datos: {new_post}")

        try:
            logger.error(f"El proceso fue satisfactorio se procede a eliminar las compensaciones por TransactionId: {transaction_id}")
            delete_success = DeleteCompensation(transactionId=transaction_id).execute()
            logger.error(f"El de eliminar las compensaciones por TransactionId retorno: {delete_success}")
            if not delete_success:
                logger.warning(f"No se encontraron compensaciones para la transacción Id #{transaction_id}")
        except Exception as delete_error:
            logger.error(f"Se presento un error eliminando la compensación para la transacción Id #{transaction_id}: {delete_error}")


        logger.warning(f"Se procede a realizar la respuesta exitosa de la creación de la publicación.")
        return jsonify({
            "data": {
                "id": new_post['id'],
                "userId": user_id,
                "createdAt": new_post['createdAt'],
                "expireAt": expire_at,
                "route": {
                    "id": flight_id,
                    "createdAt": new_post['createdAt'],
                }
            },
            "msg": "Publicación creada exitosamente"
        }), 201

    except Exception as e:
        logger.warning(f"Se han registrado errores en la creación de la publicación, se ejecutan las compensaciones de la saga.")
        CompensateSagaOperations(transaction_id, auth_header, post_url, route_url).execute()
        logger.error(f"Se ejecutan las compensaciones de la saga por TransactionId: {transaction_id}")
        return "", 400


def search_route(json_data, auth_header, route_url):
    search_route_url = f"{route_url}/routes?flight={json_data['flightId']}"
    response = requests.get(search_route_url, headers={"Authorization": auth_header})
    logger.error(f"Se ejecuta la busqueda de ruta dentro de search_route con response: {response}")
    if response.status_code == 200 and response.json():
        route_id = response.json()[0]['id']
        return route_id
    return None

def create_route(json_data, auth_header, route_url, transaction_id):
    create_route_url = f"{route_url}/routes"
    origin = json_data.get('origin', {})
    destiny = json_data.get('destiny', {})
    route_data = {
        "flightId": json_data.get('flightId'),
        "sourceAirportCode": origin.get('airportCode'),
        "sourceCountry": origin.get('country'),
        "destinyAirportCode": destiny.get('airportCode'),
        "destinyCountry": destiny.get('country'),
        "bagCost": json_data.get('bagCost'),
        "plannedStartDate": json_data.get('plannedStartDate'),
        "plannedEndDate": json_data.get('plannedEndDate')
    }
    response = requests.post(create_route_url, json=route_data, headers={"Authorization": auth_header})
    logger.error(f"Se ejecuta la creación de ruta dentro de create_route con response: {response}")
    if response.status_code == 201:
        route_id = response.json()['id']
        CreateCompensation(transactionId=transaction_id, action="delete_route", detail=str(route_id)).execute()
        return route_id
    raise Exception("No se pudo crear la ruta")

def create_external_post(user_id, route_id, json_data, auth_header, post_url, transaction_id):
    post_service_url = f"{post_url}/posts"
    post_data = {
        "userId": user_id,
        "routeId": route_id,
        "expireAt": json_data.get('expireAt'),
    }

    create_response = requests.post(post_service_url, json=post_data, headers={"Authorization": auth_header})
    logger.error(f"Se ejecuta la creación de post dentro de create_external_post con response: {create_response}")
    if create_response.status_code == 201:
        post_id = create_response.json()['id']
        CreateCompensation(transactionId=transaction_id, action="delete_post", detail=str(post_id)).execute()
        new_post = create_response.json()
        return new_post
    else:
        raise Exception("Error al crear el post en el servicio de posts")

def query_external_post(user_id, route_id, auth_header, post_url):
    post_service_url = f"{post_url}/posts?route={route_id}&owner={user_id}"

    query_response = requests.get(post_service_url, headers={"Authorization": auth_header})
    logger.error(f"Se ejecuta la busqueda de posts dentro de query_external_post con response: {query_response}")
    if query_response.status_code == 200:
        posts = query_response.json()
        return posts
    elif query_response.status_code == 404:
        return None
    else:
        raise Exception("Error al consultar el post en el servicio de posts")


@operations_blueprint.route('/rf003/ping', methods = ['GET'])
def ping():
    return "pong"