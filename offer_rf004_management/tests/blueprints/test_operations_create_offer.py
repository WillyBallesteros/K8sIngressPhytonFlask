from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import create_offer
from src.commands.create_compensation import CreateCompensation
from src.commands.execute_compensation import ExecuteCompensation
from src.commands.query import Query


   
@pytest.fixture
def mock_request_post(mocker):
    return mocker.patch('requests.post')

def test_operations_create_offer(mock_request_post, mocker):
    mocker.patch.object(CreateCompensation, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "transactionId": "b79cb3ba-745e-5d9a-8903-4a02327a7e10",
            "action": "delete",
            "path": "some/path",
            "detail": "b79cb3ba-745e-5d9a-8903-4a02327a7e11"
        })
    fake_post_response = MagicMock()
    fake_post_response.status_code = 201
    fake_post_response.text = '{"id": "offerId"}'
    mock_request_post.return_value = fake_post_response
    
    json_request = {
        'description':'description',
        'size':'MEDIUM',
        'fragile':False,
        'offer':123
        }
    transaction_id = 'txn123'
    id = 'id'        
    obj = create_offer('Bearer validtoken', transaction_id, json_request, id  )
    assert obj['id'] == 'offerId'
    
def test_operations_create_offer_error(mock_request_post, mocker):
    mocker.patch.object(ExecuteCompensation, 'execute', return_value= {})
    fake_post_response = MagicMock()
    fake_post_response.status_code = 404
    fake_post_response.text = '{"id": "offerId"}'
    mock_request_post.return_value = fake_post_response
    
    json_request = {
        'description':'description',
        'size':'MEDIUM',
        'fragile':False,
        'offer':123
        }
    transaction_id = 'txn123'
    id = 'id'        
    obj = create_offer('Bearer validtoken', transaction_id, json_request, id  )
    assert obj == 404
    
def test_operations_create_offer_external_error(mock_request_post, mocker):
    mocker.patch.object(ExecuteCompensation, 'execute', return_value= {})
    fake_post_response = MagicMock()
    fake_post_response.status_code = 201
    fake_post_response.text = '{"id": "offerId"}'
    mock_request_post.return_value = fake_post_response
    mock_request_post.side_effect = Exception("Test exception")
    
    json_request = {
        'description':'description',
        'size':'MEDIUM',
        'fragile':False,
        'offer':123
        }
    transaction_id = 'txn123'
    id = 'id'        
    obj = create_offer('Bearer validtoken', transaction_id, json_request, id  )
    assert obj == 500