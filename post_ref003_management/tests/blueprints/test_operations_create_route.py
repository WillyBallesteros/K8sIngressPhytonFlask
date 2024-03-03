from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import create_route
from src.commands.create_compensation import CreateCompensation

@pytest.fixture
def mock_request_post(mocker):
    return mocker.patch('requests.post')

def test_create_route_success(mock_request_post, mocker):
    fake_response = MagicMock()
    fake_response.status_code = 201
    fake_response.json.return_value = {'id': 'new-route-id'}
    mock_request_post.return_value = fake_response

    mocker.patch.object(CreateCompensation, 'execute')

    json_data = {
        'flightId': 'flight123',
        'origin': {'airportCode': 'ABC', 'country': 'CountryA'},
        'destiny': {'airportCode': 'XYZ', 'country': 'CountryB'},
        'bagCost': 150,
        'plannedStartDate': '2035-12-31T08:00:00',
        'plannedEndDate': '2035-12-31T12:00:00'
    }
    route_id = create_route(json_data, 'Bearer validtoken', 'http://route.service', 'transaction-id')

    assert route_id == 'new-route-id'

    CreateCompensation.execute.assert_called_once()

def test_create_route_failure(mock_request_post):
    fake_response = MagicMock()
    fake_response.status_code = 500  # O cualquier otro código de error apropiado
    mock_request_post.return_value = fake_response

    json_data = {
        'flightId': 'flight123',
        'origin': {'airportCode': 'ABC', 'country': 'CountryA'},
        'destiny': {'airportCode': 'XYZ', 'country': 'CountryB'},
        'bagCost': 150,
        'plannedStartDate': '2035-12-31T08:00:00',
        'plannedEndDate': '2035-12-31T12:00:00'
    }

    with pytest.raises(Exception) as excinfo:
        create_route(json_data, 'Bearer validtoken', 'http://route.service', 'transaction-id')

    assert str(excinfo.value) == "No se pudo crear la ruta"
