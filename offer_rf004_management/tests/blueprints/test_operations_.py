from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import create_offer
from src.commands.create_compensation import CreateCompensation
from src.commands.execute_compensation import ExecuteCompensation
from src.commands.query import Query
from src.main import app
from src.models.model import session

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsCreatePost:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')

    def test_operations_create_offer_rf004(self, client, mocker):
        
        current_date = datetime.now()
        one_day_delta = timedelta(days=1)
        new_date = current_date + one_day_delta
        future_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")
        query_post_return = {"userId": "userId", "routeId": "routeId", "id": "someId", "expireAt":future_date_str}
        mocker.patch('src.blueprints.operations.query_post', return_value=query_post_return)
        
        query_user_return = {"name": "Test User", "id": "user123"}
        mocker.patch('src.blueprints.operations.query_user', return_value=query_user_return)
        
        mocker.patch.object(CreateCompensation, 'execute', return_value= {
                "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
                "transactionId": "b79cb3ba-745e-5d9a-8903-4a02327a7e10",
                "action": "delete",
                "path": "some/path",
                "detail": "b79cb3ba-745e-5d9a-8903-4a02327a7e11"
            })
        today_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S")
        create_offer_return = {"name": "Test User", "id": "user123", "createdAt": today_date_str}
        mocker.patch('src.blueprints.operations.create_offer', return_value=create_offer_return)
        
        query_routes_return = {"name": "Test User", "id": "user123", "bagCost":40}
        mocker.patch('src.blueprints.operations.query_routes', return_value=query_routes_return)
        
        mocker.patch.object(CreateCompensation, 'execute', return_value= {
                "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
                "transactionId": "b79cb3ba-745e-5d9a-8903-4a02327a7e10",
                "action": "delete",
                "path": "some/path",
                "detail": "b79cb3ba-745e-5d9a-8903-4a02327a7e11"
            })
        
        create_score_return = {"name": "Test User", "id": "user123"}
        mocker.patch('src.blueprints.operations.create_score', return_value=create_score_return)
        
        data = {
            "description": "some description",
            "size": "LARGE",
            "fragile" : False,
            "offer": 20
        }
        response = client.post('/rf004/posts/someId/offers', json=data, headers={'Authorization': 'valid token'})
        assert response.status_code == 201
    