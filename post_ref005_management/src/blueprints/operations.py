from flask import Flask, jsonify, request, Blueprint
from ..utils.utils import get_info_token
from ..commands.user import Query
import os
import json
import requests
import logging
from . import offer_url, post_url, route_url, score_url, user_url

operations_blueprint = Blueprint('operations', __name__)

def common_validations(auth_header):

    if not auth_header or not auth_header.startswith('Bearer '):
        return "", 403

    info_token = get_info_token(auth_header)
    if not info_token:
        return "", 401

def query_user(auth_header, userId):
    user_query = Query(auth_header, user_url, '/users/me' ).execute()
    if user_query.status_code != 200:
        return user_query.status_code
    logged_user = json.loads(user_query.text)
    #validar que sea un usuario diferente
    if userId != logged_user['id']:
        return 403
    return logged_user

@operations_blueprint.route('/rf005/posts/<string:id>', methods=['GET'])
def aggregated_get_id(id): 

    auth_header = request.headers.get('Authorization')
    postId = id

    #Validar que el token exista y no esté vencido
    validation_response = common_validations(auth_header)
    if validation_response:
        return validation_response  

    #Validar que el post exista
    data_post = search_post(postId, auth_header, post_url)
    if not data_post:
        return "", 404    
    
    logged_user = query_user(auth_header, data_post['userId'])
    if isinstance(logged_user, int):
        return "",logged_user

    data_route = search_route(data_post['routeId'], auth_header, route_url)
    if not data_route:
        return "", 404
    
    data_offer = search_offer(postId, auth_header, offer_url)
    if not data_offer:
        return "", 404
    
    data_score = search_score(postId, auth_header, score_url)
    if not data_score:
        return "", 404
    
    offer_list = []
    for item in data_offer:
        for score in data_score:
            if score['offerId'] == item['id']:
                item['score'] = score['score']
                break

        offer_dict = {
            'id': item['id'],
            'userId': item['userId'],
            "description": item['description'],
            "size": item['size'],
            "fragile": item['fragile'],
            "offer": item['offer'],
            "score": item['score'],
            "createdAt": item['createdAt'],
        }
        offer_list.append(offer_dict)
        
    
    sorted_offers = sorted(offer_list, key=lambda x: x['score'], reverse=True)
    
    return jsonify({
        "data": {
            "id": data_post["id"],
            "expireAt": data_post["expireAt"],
            "route": {
                "id": data_route["id"],
                "flightId": data_route["flightId"],
                "origin": {
                    "airportCode": data_route["sourceAirportCode"],
                    "country": data_route["sourceCountry"],
                },
                "destiny": {
                    "airportCode": data_route["destinyAirportCode"],
                    "country": data_route["destinyCountry"],
                },
                "bagCost": data_route["bagCost"]
            },
            "plannedStartDate": data_route["plannedStartDate"],
            "plannedEndDate": data_route["plannedEndDate"],
            "createdAt": data_route["createdAt"],
            "offers": sorted_offers
        }
    }), 200

def search_post(postId, auth_header, post_url):
    
    search_post_url = f"{post_url}/posts/{postId}"
    
    response = requests.get(search_post_url, headers={"Authorization": auth_header})
    if response.status_code == 200 and response.json():
        data_post = response.json()
        
        return data_post
    return None

def search_route(routeId, auth_header, route_url):
    
    search_route_url = f"{route_url}/routes/{routeId}"
    response = requests.get(search_route_url, headers={"Authorization": auth_header})
    if response.status_code == 200 and response.json():
        data_route = response.json()
        return data_route
    return None

def search_offer(postId, auth_header, offer_url):
    
    search_offer_url = f"{offer_url}/offers?post={postId}"
    
    response = requests.get(search_offer_url, headers={"Authorization": auth_header})
    if response.status_code == 200 and response.json():
        data_offer = response.json()
        return data_offer
    return None

def search_score(postId, auth_header, score_url):
    
    search_score_url = f"{score_url}/score/utility/{postId}"
    
    response = requests.get(search_score_url, headers={"Authorization": auth_header})
    if response.status_code == 200 and response.json():
        data_offer = response.json()
        return data_offer
    return None

@operations_blueprint.route('/rf005/ping', methods = ['GET'])
def ping():
    return "pong"