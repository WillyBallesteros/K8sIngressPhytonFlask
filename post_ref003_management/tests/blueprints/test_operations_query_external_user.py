from unittest.mock import patch, MagicMock
import pytest
import requests

from src.commands.user import QueryUser

@pytest.fixture
def mock_request_get(mocker):
    return mocker.patch('requests.get')

def test_query_user_success(mock_request_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {'name': 'Test User', 'id': 'user123'}
    mock_request_get.return_value = fake_response

    user_query = QueryUser('Bearer validtoken', 'http://user.service')
    user_info = user_query.execute()

    assert user_info == {'name': 'Test User', 'id': 'user123'}

def test_query_user_not_found(mock_request_get):
    fake_response = MagicMock()
    fake_response.status_code = 404
    mock_request_get.return_value = fake_response

    user_query = QueryUser('Bearer validtoken', 'http://user.service')
    user_info, status_code = user_query.execute()

    assert user_info == ""
    assert status_code == 404

def test_query_user_error(mock_request_get):
    mock_request_get.side_effect = requests.exceptions.RequestException

    user_query = QueryUser('Bearer validtoken', 'http://user.service')

    user_info, status_code = user_query.execute()

    assert user_info == ""
    assert status_code == 400
