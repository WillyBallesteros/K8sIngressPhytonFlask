from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import search_post, search_route, search_offer, search_score
from src.commands.user import Query
from src.main import app
from src.models.model import session

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsAggregateGetId:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')

    def test_operations_aggregated_get_id(self, client, mocker):
        
        current_date = datetime.now()
        one_day_delta = timedelta(days=1)
        new_date = current_date + one_day_delta
        future_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")

        search_post_return = {"userId": "userId", "routeId": "routeId", "id": "someId", "createdAt": future_date_str , "expireAt":future_date_str}
        mocker.patch('src.blueprints.operations.search_post', return_value=search_post_return)
        
        query_user_return = {"name": "Test User", "id": "user123"}
        mocker.patch('src.blueprints.operations.query_user', return_value=query_user_return)

        search_routes_return = {'bagCost': 909, 'createdAt': future_date_str, 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '470', 'id': 'someId', 'plannedEndDate': future_date_str, 'plannedStartDate': future_date_str, 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}
        mocker.patch('src.blueprints.operations.search_route', return_value=search_routes_return)

        today_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S")
        create_offer_return = [{'createdAt': today_date_str, 'description': 'totam et ea', 'fragile': 'true', 'id': 'offerSomeId', 'offer': '879', 'postId': 'someId', 'size': 'SMALL', 'userId': 'dummyUser'}]
        mocker.patch('src.blueprints.operations.search_offer', return_value=create_offer_return)

        search_score_return = [{"offerId": "offerSomeId", "score": "user123"}]
        mocker.patch('src.blueprints.operations.search_score', return_value=search_score_return)
        
        response = client.get('/rf005/posts/someId', headers={'Authorization': 'Bearer e91813b7-84ee-45b3-b9fd-7f272f8a8bb9'})
        assert response.status_code == 200
    