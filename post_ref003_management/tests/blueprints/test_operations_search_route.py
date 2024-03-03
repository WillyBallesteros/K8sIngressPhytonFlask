from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import search_route

@pytest.fixture
def mock_request_get(mocker):
    return mocker.patch('requests.get')

def test_search_route_found(mock_request_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = [{'id': 'route-id'}]
    mock_request_get.return_value = fake_response

    json_data = {'flightId': 'flight123'}

    route_id = search_route(json_data, 'Bearer validtoken', 'http://route.service')

    assert route_id == 'route-id'

def test_search_route_not_found(mock_request_get):
    fake_response_empty = MagicMock()
    fake_response_empty.status_code = 200
    fake_response_empty.json.return_value = []
    mock_request_get.return_value = fake_response_empty

    fake_response_not_found = MagicMock()
    fake_response_not_found.status_code = 404
    fake_response_not_found.json.return_value = None

    json_data = {'flightId': 'flight123'}

    route_id_empty = search_route(json_data, 'Bearer validtoken', 'http://route.service')
    assert route_id_empty is None

    mock_request_get.return_value = fake_response_not_found

    route_id_not_found = search_route(json_data, 'Bearer validtoken', 'http://route.service')
    assert route_id_not_found is None
