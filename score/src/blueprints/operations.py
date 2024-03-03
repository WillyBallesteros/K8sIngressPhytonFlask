from flask import jsonify, request, Blueprint
from ..utils.utils import size_to_percent
from ..commands.exists import ExistsScore
from ..commands.update import UpdateScore
from ..commands.create import CreateScore
from ..commands.get import GetScoreByPost
from ..commands.delete import DeleteScoreByPost


import os

operations_blueprint = Blueprint('operations', __name__)

@operations_blueprint.route('/score/utility/<string:id>', methods = ['GET'])
def get(id):
    scores = GetScoreByPost(id).execute()
    scores_list = []
    for score in scores:
        score_dict = {
            'offerId': score.offerId,
            'score': score.utility
        }
        scores_list.append(score_dict)

    return jsonify(scores_list), 200

@operations_blueprint.route('/score/utility/<string:id>', methods = ['DELETE'])
def delete(id):
    DeleteScoreByPost(id).execute()

    return "", 200

@operations_blueprint.route('/score/utility', methods = ['POST'])
def new():
    json = request.get_json()
    postId = json.get('postId')
    offerId = json.get('offerId')
    offerValue = json.get('offerValue')
    bagSize = json.get('bagSize')
    bagCost = json.get('bagCost')

    if (postId is None or offerId is None or offerValue is None or bagSize is None or bagCost is None):
        return "Parameters are missing. The parameters postId, offerId, offerValue, bagSize and bagCost are expected.", 400
    
    try:
        offerValue = float(offerValue) if offerValue is not None else None
    except ValueError:
        return "offerValue must be valid", 412
    
    try:
        bagCost = float(bagCost) if bagCost is not None else None
    except ValueError:
        return "bagCost value must be valid", 412
    
    bagSize = size_to_percent(bagSize)
    if bagSize < 0:
        return "size value must be valid", 412
    
    utility = offerValue - (bagSize * bagCost)

    score = ExistsScore(postId, offerId).execute()
    if len(score) > 0:
        UpdateScore(score[0].id, utility).execute()

        return jsonify({
            "id": score[0].id,
            "value": utility
        }), 200

    score = CreateScore(postId, offerId, utility).execute()

    return jsonify({
        "id": score.id,
        "value": score.utility
    }), 201

@operations_blueprint.route('/score/ping', methods = ['GET'])
def ping():
    return "pong"
 