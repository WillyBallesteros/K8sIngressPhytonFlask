from flask import jsonify
from ..models.model import session
from ..models.route import Route
from .base_command import BaseCommannd

class DeleteRoute(BaseCommannd):
  def __init__(self, id):
    self.id = id
     
  def execute(self):
    
    route = session.query(Route).filter(Route.id == self.id).first()
    if not route:
        return 404
    
    # Elimina la oferta de la base de datos
    session.delete(route)
    session.commit()
    
    return 200