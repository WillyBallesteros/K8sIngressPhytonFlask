from unittest.mock import patch, MagicMock
import pytest
import requests

from src.commands.create import Create
from src.commands.create_compensation import CreateCompensation
from src.commands.execute_compensation import ExecuteCompensation

@pytest.fixture
def mock_request_post(mocker):
    return mocker.patch('requests.post')

def test_create_success(mock_request_post, mocker):
    
    mocker.patch.object(CreateCompensation, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "transactionId": "b79cb3ba-745e-5d9a-8903-4a02327a7e10",
            "action": "delete",
            "path": "some/path",
            "detail": "b79cb3ba-745e-5d9a-8903-4a02327a7e11"
        })
    
    fake_response = MagicMock()
    fake_response.status_code = 201
    fake_response.json.return_value = {'name': 'Test User', 'id': 'user123'}
    fake_response.text = '{"name": "Test User", "id": "user123"}'
    payload = {'name': 'Test User', 'id': 'user123'}

    mock_request_post.return_value = fake_response

    create = Create( 'Bearer validtoken', 'txid12345', 'http://user.service', 'path', payload)
    create_info = create.execute()

    assert create_info.json.return_value == {'name': 'Test User', 'id': 'user123'}

def test_create_error(mock_request_post, mocker):
    
    mocker.patch.object(ExecuteCompensation, 'execute', return_value= {
        })
    
    fake_response = MagicMock()
    fake_response.status_code = 404
    mock_request_post.return_value = fake_response
    payload = {'name': 'Test User', 'id': 'user123'}

    create = Create( 'Bearer validtoken', 'txid12345', 'http://user.service', 'path', payload)
    create_info = create.execute()

    assert create_info == 404
    
def test_create_error_external_failure(mock_request_post, mocker):
    mocker.patch.object(ExecuteCompensation, 'execute', return_value= {
        })
    
    fake_response = MagicMock()
    fake_response.status_code = 500
    mock_request_post.side_effect = Exception("Test exception")
    payload = {'name': 'Test User', 'id': 'user123'}

    create = Create( 'Bearer validtoken', 'txid12345', 'http://user.service', 'path', payload)
    create_info = create.execute()

    assert create_info == 500