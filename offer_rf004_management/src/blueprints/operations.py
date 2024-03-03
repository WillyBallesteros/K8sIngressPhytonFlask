import logging
import requests
import uuid
from flask import Flask, jsonify, request, Blueprint

from src.commands.delete_compensation import DeleteCompensation

from ..commands.query import Query
from ..commands.create import Create
import json
from ..utils.utils import is_future_date
from . import offer_url, post_url, route_url, score_url, user_url

operations_blueprint = Blueprint('operations', __name__)

def query_post(auth_header, postId):
    post_query = Query(auth_header,post_url, '/posts', postId).execute()
    if post_query.status_code != 200:
        return post_query.status_code
    post_content = json.loads(post_query.text)
    #validar que la post este vigente 
    if not is_future_date(post_content['expireAt']):
        return 412
    return post_content


def query_user(auth_header, userId):
    user_query = Query(auth_header, user_url, '/users/me' ).execute()
    if user_query.status_code != 200:
        return user_query.status_code
    logged_user = json.loads(user_query.text)
    #validar que sea un usuario diferente
    if userId == logged_user['id']:
        return 412
    return logged_user


def create_offer(auth_header, transaction_id, json_request, id):
    payload = {
                "postId": id,
                "description": json_request.get('description'),
                "size": json_request.get('size'),
                "fragile": json_request.get('fragile'),
                "offer": json_request.get('offer')
            }
    offer_create = Create(auth_header, transaction_id, offer_url,'/offers', payload).execute()
    if isinstance(offer_create, int):
        return offer_create
    offer_content = json.loads(offer_create.text)
    return offer_content


def query_routes(auth_header, routeId):
    route_query = Query(auth_header,route_url, '/routes', routeId).execute()
    if route_query.status_code != 200:
        return route_query.status_code
    route_content = json.loads(route_query.text)
    return route_content


def create_score(auth_header, transaction_id, json_request,postId, offerId, bagCost ):
    payload = {
                    "postId": postId,
                    "offerId": offerId,
                    "bagSize": json_request.get('size'),
                    "bagCost": bagCost,
                    "offerValue": json_request.get('offer')
                }
    score_create = Create(auth_header, transaction_id, score_url,'/score/utility', payload).execute()
    if isinstance(score_create, int):
        return score_create
    score_content = json.loads(score_create.text)
    return score_content
    
    
@operations_blueprint.route('/rf004/posts/<string:id>/offers', methods = ['POST'])
def offers_id(id):
    json_request = request.get_json()
    auth_header = request.headers.get('Authorization')
    postId = id
    transaction_id = str(uuid.uuid4())
    
    post_content = query_post( auth_header, postId )
    if isinstance(post_content, int):
        return "",post_content
    

    logged_user = query_user(auth_header, post_content['userId'])
    if isinstance(logged_user, int):
        return "",logged_user
    

    offer_content = create_offer(auth_header, transaction_id, json_request, id)
    if isinstance(offer_content, int):
        return "",offer_content
    
    
    route_content = query_routes(auth_header, post_content['routeId'])
    if isinstance(route_content, int):
        return "",route_content
    
    
    score_content = create_score( auth_header, transaction_id, json_request, postId, offer_content['id'], route_content['bagCost'] )
    if isinstance(score_content, int):
        return "",score_content
   
    DeleteCompensation(transaction_id).execute()          
    
    objReturn = {
            "data": {
                "id": offer_content['id'],
                "userId": logged_user['id'],
                "createdAt": offer_content['createdAt'],
                "postId": postId
            },
            "msg": "Exito"
        }
        
    return jsonify(objReturn), 201


@operations_blueprint.route('/rf004/ping', methods = ['GET'])
def ping3():
    
    logging.warning(f'OPERATIONS ping[response /rf004/ping pong /rf004/ping]')
    return "pong",200
