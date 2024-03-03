from flask import jsonify
from ..models.model import session
from ..models.route import Route
from .base_command import BaseCommannd

class QueryRoute(BaseCommannd):
  def __init__(self, flight_id=None, id=None):
    self.flight_id = flight_id
    self.id = id
     
  def execute(self):
    conditions = []
    if self.flight_id:
        conditions.append(Route.flightId == self.flight_id)
    if self.id:
        conditions.append(Route.id == self.id)

    if conditions:
        routes = session.query(Route).filter(*conditions).all()
    else:
        routes = session.query(Route).all()
        
    if routes is not None:
        resultados = [{'id': route.id
                       ,'flightId': route.flightId
                       ,'sourceAirportCode': route.sourceAirportCode
                       ,'sourceCountry': route.sourceCountry
                       ,'destinyAirportCode': route.destinyAirportCode
                       ,'destinyCountry': route.destinyCountry
                       ,'bagCost': route.bagCost
                       ,'plannedStartDate': route.plannedStartDate
                       ,'plannedEndDate': route.plannedEndDate
                       ,'createdAt': route.createdAt} for route in routes]
    
    return jsonify(resultados) 