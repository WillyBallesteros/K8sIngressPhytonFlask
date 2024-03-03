from flask import jsonify
from ..models.model import session
from ..models.offer import Offer
from .base_command import BaseCommannd

class QueryOffer(BaseCommannd):
  def __init__(self, post_id=None, owner=None, id=None):
    self.post_id = post_id
    self.owner = owner
    self.id = id
     
  def execute(self):
    conditions = []
    if self.post_id:
        conditions.append(Offer.postId == self.post_id)
    if self.owner:
        conditions.append(Offer.userId == self.owner)
    if self.id:
        conditions.append(Offer.id == self.id)

    if conditions:
        offers = session.query(Offer).filter(*conditions).all()
    else:
        offers = session.query(Offer).all()
    if offers is not None:
        resultados = [{'id': offer.id, 'postId': offer.postId, 'description': offer.description, 'size': offer.size
                       , 'fragile': offer.fragile
                       , 'offer': offer.offer
                       , 'createdAt': offer.createdAt
                       , 'userId': offer.userId} for offer in offers]
    
    return jsonify(resultados) 