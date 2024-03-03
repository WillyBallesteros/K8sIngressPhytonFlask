import pytest
from unittest.mock import patch
from src.models.model import session
from src.models.route import Route
from src.commands.exists import ExistsFlight

@pytest.fixture(autouse=True)
def setup_method(mocker):
    mock_query = mocker.patch.object(session, 'query')
    mock_get = mock_query.return_value.get
    mock_filter = mock_query.return_value.filter
    mock_first = mock_filter.return_value.first

    return mock_query, mock_get, mock_filter, mock_first

class TestExistsRoute:
    def test_exists_route_by_id_found(self, setup_method):
        _, mock_get, _, _ = setup_method
        mock_get.return_value = Route(
            flightId="867", 
            sourceAirportCode="LIM", 
            sourceCountry="Peru", 
            destinyAirportCode="MIA", 
            destinyCountry="Inglaterra", 
            bagCost=100, 
            plannedStartDate="2024-02-12T16:33:26.612Z", 
            plannedEndDate="2024-03-12T16:33:26.612Z")

        exists_route_cmd = ExistsFlight(flightId="867")
        result = exists_route_cmd.execute()

        assert result == True   