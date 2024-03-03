import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.models.route import Route
from src.commands.create import CreateFlight

class TestCreate():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch.object(session, 'add')
        self.mock_commit = mocker.patch.object(session, 'commit')
  
    def test_create(self):
        test_data = {
            "flightId":"867", 
            "sourceAirportCode":"LIM", 
            "sourceCountry":"Peru", 
            "destinyAirportCode":"MIA", 
            "destinyCountry":"Inglaterra", 
            "bagCost":100, 
            "plannedStartDate":"2024-02-12T16:33:26.612Z", 
            "plannedEndDate":"2024-03-12T16:33:26.612Z"
        }
        route_created = CreateFlight(**test_data).execute()

        self.mock_add.assert_called_once()
        self.mock_commit.assert_called_once()
        assert isinstance(route_created, Route)
        assert route_created.flightId == test_data['flightId']
        assert route_created.sourceAirportCode == test_data['sourceAirportCode']
        assert route_created.sourceCountry == test_data['sourceCountry']