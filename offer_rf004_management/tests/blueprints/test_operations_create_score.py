from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import create_score
from src.commands.create_compensation import CreateCompensation
from src.commands.execute_compensation import ExecuteCompensation
from src.commands.query import Query


# Definir la clase Query simulada
class Query:
    def execute(self):
        # Simular el objeto request con un status_code de 200
        class RequestObject:
            status_code = 200

        return RequestObject()
    
    
@pytest.fixture
def mock_request_post(mocker):
    return mocker.patch('requests.post')

def test_operations_create_score(mock_request_post, mocker):
    mocker.patch.object(CreateCompensation, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "transactionId": "b79cb3ba-745e-5d9a-8903-4a02327a7e10",
            "action": "delete",
            "path": "some/path",
            "detail": "b79cb3ba-745e-5d9a-8903-4a02327a7e11"
        })
    fake_post_response = MagicMock()
    fake_post_response.status_code = 201
    fake_post_response.text = '{"id": "scoreId"}'
    mock_request_post.return_value = fake_post_response
    
    json_request = {
        'size':'MEDIUM',
        'offer':123
        }
    transaction_id = 'txn123'
    
    postId = 'postId'
    offerId = 'offerId'
    bagCost = 'bagCost'
    obj = create_score('Bearer validtoken', transaction_id, json_request,postId, offerId, bagCost )
    assert obj['id'] == 'scoreId'
    
def test_operations_create_score_error(mock_request_post, mocker):
    mocker.patch.object(ExecuteCompensation, 'execute', return_value= {})
    fake_post_response = MagicMock()
    fake_post_response.status_code = 404
    fake_post_response.text = '{"id": "offerId"}'
    mock_request_post.return_value = fake_post_response
    
    json_request = {
        'size':'MEDIUM',
        'offer':123
        }
    transaction_id = 'txn123'
    
    postId = 'postId'
    offerId = 'offerId'
    bagCost = 'bagCost'
    obj = create_score('Bearer validtoken', transaction_id, json_request,postId, offerId, bagCost )
    assert obj == 404
    
def test_operations_create_score_external_error(mock_request_post, mocker):
    mocker.patch.object(ExecuteCompensation, 'execute', return_value= {})
    fake_post_response = MagicMock()
    fake_post_response.status_code = 201
    fake_post_response.text = '{"id": "offerId"}'
    mock_request_post.return_value = fake_post_response
    mock_request_post.side_effect = Exception("Test exception")
    
    json_request = {
        'size':'MEDIUM',
        'offer':123
        }
    transaction_id = 'txn123'
    
    postId = 'postId'
    offerId = 'offerId'
    bagCost = 'bagCost'
    obj = create_score('Bearer validtoken', transaction_id, json_request,postId, offerId, bagCost )
    assert obj == 500