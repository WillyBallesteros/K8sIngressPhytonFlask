from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import query_routes
from src.commands.query import Query


# Definir la clase Query simulada
class Query:
    def execute(self):
        # Simular el objeto request con un status_code de 200
        class RequestObject:
            status_code = 200

        return RequestObject()
    
    
@pytest.fixture
def mock_request_get(mocker):
    return mocker.patch('requests.get')

def test_operations_query_routes(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 200
    fake_post_response.text = '{"id": "routeId"}'
    mock_request_get.return_value = fake_post_response
    user = query_routes('Bearer validtoken', 'routeId')
    assert user['id'] == 'routeId'
    
    
def test_operations_query_routes_status_code_invalid(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 401
    fake_post_response.text = '{"id": "user123"}'
    mock_request_get.return_value = fake_post_response
    user = query_routes('Bearer validtoken', 'user123')
    assert user == 401