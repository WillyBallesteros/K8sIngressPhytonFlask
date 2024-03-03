from ..models.model import session
from ..models.route import Route
from .base_command import BaseCommannd

class ExistsFlight(BaseCommannd):
  def __init__(self, flightId):
    self.flightId = flightId
  
  def execute(self):
    flight = session.query(Route).filter(Route.flightId == self.flightId).first()
    if flight is not None:
        return True
    
    return False   