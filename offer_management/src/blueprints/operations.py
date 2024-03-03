import logging
from flask import Flask, jsonify, request, Blueprint

from ..commands.reset import ResetOffer
from ..commands.delete import DeleteOffer
from ..commands.query import QueryOffer
from ..commands.create import CreateOffer
from ..commands.user import QueryUser
from ..utils.utils import is_positive, get_info_token, is_active_date, is_boolean_and_value, is_size_admited, is_uuid_valid


operations_blueprint = Blueprint('operations', __name__)

def get_info_user(auth_header):
    info_user = QueryUser(auth_header).execute()
    return info_user

def common_validations(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return 403
    
    info_token = get_info_token(auth_header)
    if not info_token:
        return 401

def post_validations(postId, description, size, fragile, offer):
     
     #Valido los campos 
    if (postId is None or description is None or size is None or offer  is None or fragile is None):
        return 400
    
    if not is_size_admited(size):
        return 412
    
    if not is_positive(offer):
        return 412

    try:
        fragile = is_boolean_and_value(fragile) 
    except ValueError as e:
        return 400
    

def process_post_offer(postId, description, size, fragile, offer, auth_header, userId=None):
    logging.warning(f'POST OFFERS start [{postId}, {description}, {size}, {fragile}, {offer}, {auth_header}, {userId}]')
    com_validations = common_validations(auth_header)
    if com_validations:
         return {"ERROR": com_validations}
    
    p_validations = post_validations(postId, description, size, fragile, offer)
    if p_validations:
         return {"ERROR": p_validations}
    
    if not userId:
        userId = get_info_user(auth_header)['id']
    #Almaceno la oferta
    
    logging.warning(f'POST OFFERS bd [{postId}, {description}, {size}, {fragile}, {offer}, {auth_header}, {userId}]')
    offerObj = CreateOffer(postId, userId, description, size, fragile, offer).execute()
    return {"VALUE":offerObj}


@operations_blueprint.route('/offers', methods = ['POST'])
def offers():
    json = request.get_json()
    postId = json.get('postId')
    description = json.get('description')
    size = json.get('size')
    fragile = json.get('fragile')
    offer = json.get('offer')
    auth_header = request.headers.get('Authorization')
    userId = None
    if 'userId' in json:
        userId = json.get('userId')
    
    offerObj = process_post_offer(postId, description, size, fragile, offer, auth_header, userId)

    if 'ERROR' in offerObj:
        return '', offerObj.get('ERROR')
    
    value = offerObj.get('VALUE')
    return jsonify({
        "id": str(value.id),
        "userId": value.userId,
        "createdAt": value.createdAt
    }), 201

@operations_blueprint.route('/offers', methods=['GET'])
def get_offers():

    
    # Obtener los parámetros de la solicitud
    post_id = request.args.get('post')
    owner = request.args.get('owner')
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    #Valido los campos 
    if not post_id is None:
        if len(post_id) < 1:
            return "", 400
        
    if not owner is None:
        if len(owner) < 1:
            return "", 400
    
    if owner=='me':
        owner = get_info_user(auth_header)['id']
    offers = QueryOffer(post_id=post_id, owner=owner).execute()
    return offers

@operations_blueprint.route('/offers/<string:id>', methods=['GET'])
def get_offers_id(id):

    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    #Valido los campos 
    if not is_uuid_valid(id) :
        return "", 400
    
    offers = QueryOffer(id=id).execute()
    aa = offers.get_json()
    if not len(aa) > 0:
         return '',404         
    return aa[0]

@operations_blueprint.route('/offers/<string:id>', methods=['DELETE'])
def delete_offer(id):
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    if not is_uuid_valid(id) :
        return "", 400
    
    execute = DeleteOffer(id).execute()
    if execute == 200:
        return {"msg": "la oferta fue eliminada"},execute
    else:
         return '',execute

@operations_blueprint.route('/offers/ping', methods = ['GET'])
def ping3():
    
    logging.warning(f'OPERATIONS ping[response /offers/ping pong /offers/ping]')
    return "pong",200

@operations_blueprint.route('/offers/reset', methods = ['POST'])
def reset():
    ResetOffer().execute()

    return jsonify({"msg": "Todos los datos fueron eliminados"})