from ..models.model import session
from ..models.route import Route
from .base_command import BaseCommannd

class CreateFlight(BaseCommannd):
  def __init__(self, flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, plannedStartDate, plannedEndDate):
    self.flightId = flightId
    self.sourceAirportCode = sourceAirportCode
    self.sourceCountry = sourceCountry
    self.destinyAirportCode = destinyAirportCode
    self.destinyCountry = destinyCountry
    self.bagCost = bagCost
    self.plannedStartDate = plannedStartDate
    self.plannedEndDate = plannedEndDate
    
  def execute(self):
    print(f"flightId={self.flightId}sourceAirportCode={self.sourceAirportCode}sourceCountry={self.sourceCountry}destinyAirportCode={self.destinyAirportCode}destinyCountry={self.destinyCountry}bagCost={self.bagCost}plannedStartDate={self.plannedStartDate}plannedEndDate={self.plannedEndDate}")
    
    route = Route(self.flightId, self.sourceAirportCode, self.sourceCountry, self.destinyAirportCode, self.destinyCountry, self.bagCost, self.plannedStartDate, self.plannedEndDate)
    
    session.add(route)
    session.commit()

    return route