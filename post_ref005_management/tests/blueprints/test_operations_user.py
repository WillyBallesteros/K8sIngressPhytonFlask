from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import query_user
from src.commands.user import Query


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

def test_operations_query_user(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 200
    fake_post_response.text = '{"id": "user123"}'
    mock_request_get.return_value = fake_post_response
    user = query_user('Bearer validtoken', 'user123')
    assert user['id'] == 'user123'
    
    
def test_operations_query_same_user(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 200
    fake_post_response.text = '{"id": "user1234"}'
    mock_request_get.return_value = fake_post_response
    user = query_user('Bearer validtoken', 'user123')
    assert user == 403
    
def test_operations_query_user_status_code_invalid(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 401
    fake_post_response.text = '{"id": "user123"}'
    mock_request_get.return_value = fake_post_response
    user = query_user('Bearer validtoken', 'user123')
    assert user == 401