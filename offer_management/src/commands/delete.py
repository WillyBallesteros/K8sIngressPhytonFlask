from flask import jsonify
from ..models.model import session
from ..models.offer import Offer
from .base_command import BaseCommannd

class DeleteOffer(BaseCommannd):
  def __init__(self, id):
    self.id = id
     
  def execute(self):
    
    offer = session.query(Offer).filter(Offer.id == self.id).first()
    if not offer:
        return 404
    
    # Elimina la oferta de la base de datos
    session.delete(offer)
    session.commit()
    
    return 200