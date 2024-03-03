from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import query_post
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

def test_operations_query_post(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 200
    current_date = datetime.now()
    one_day_delta = timedelta(days=1)
    new_date = current_date + one_day_delta
    future_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    fake_post_response.text = '{"name": "Test User", "id": "user123", "expireAt":"'+future_date_str+'"}'
    mock_request_get.return_value = fake_post_response
    new_post = query_post('Bearer validtoken', 'post-id')
    assert new_post['expireAt'] == future_date_str

def test_operations_query_post_expireAt_invalid(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 200
    current_date = datetime.now()
    one_day_delta = timedelta(days=-1)
    new_date = current_date + one_day_delta
    future_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    fake_post_response.text = '{"name": "Test User", "id": "user123", "expireAt":"'+future_date_str+'"}'
    mock_request_get.return_value = fake_post_response
    new_post = query_post('Bearer validtoken', 'post-id')
    assert new_post == 412
    
def test_operations_query_post_status_code_invalid(mock_request_get, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 401
    current_date = datetime.now()
    one_day_delta = timedelta(days=-1)
    new_date = current_date + one_day_delta
    future_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    fake_post_response.text = '{"name": "Test User", "id": "user123", "expireAt":"'+future_date_str+'"}'
    mock_request_get.return_value = fake_post_response
    new_post = query_post('Bearer validtoken', 'post-id')
    assert new_post == 401