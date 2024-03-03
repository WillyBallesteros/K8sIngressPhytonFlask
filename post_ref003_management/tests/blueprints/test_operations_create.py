import pytest
from src.commands.create_compensation import CreateCompensation
from src.commands.user import QueryUser
from src.main import app
from src.models.model import session
from src.models.compensation import Compensation
from tests.utils.utils import VALID_TOKEN, INVALID_TOKEN, INVALID_TOKEN_USERID
from unittest.mock import MagicMock
from datetime import datetime

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsCreatePost:

    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')

    def test_create_post_rf003_success(self, client, mocker):

        data = {
            "flightId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2035-12-31T23:59:59",
            "plannedStartDate": "2024-12-25T08:00:00",
            "plannedEndDate": "2024-12-25T12:00:00",
            "origin": {
                "airportCode": "ORI123",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "DES456",
                "country": "CountryB"
            },
            "bagCost": 150
        }

        mocker.patch('src.blueprints.operations.search_route', return_value=None)

        mocker.patch('src.blueprints.operations.create_route', return_value="b79cb3ba-745e-5d9a-8903-4a02327a7e09")

        fake_post_response = mocker.MagicMock()
        fake_post_response.status_code = 201

        fake_post_response.json.return_value = {
            "id": "b78cb3ba-785e-5d9a-8903-4a02327a7e87",
            "routeId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "userId": "b79cb5ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt" : "2035-12-31T23:59:59",
            "createdAt" : "2034-12-31T23:59:59"
        }

        mocker.patch.object(QueryUser, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "username": "Juan Test",
            "email": "jjtest@test.com",
            "fullName": "Juan Completo",
            "dni": "12345",
            "phoneNumber": "123144",
            "status": "Activo"
        })

        mocker.patch('requests.post', return_value=fake_post_response)

        mocker.patch.object(CreateCompensation, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "transactionId": "b79cb3ba-745e-5d9a-8903-4a02327a7e10",
            "action": "delete_post",
            "detail": "b79cb3ba-745e-5d9a-8903-4a02327a7e11"
        })

        mocker.patch('src.blueprints.operations.query_external_post', return_value=[])

        mock_post = MagicMock()
        # mock_post.id = "b78c3b3a-785e-5d9a-8903-4a02327a7e87"
        # mock_post.routedId = "b79cb3ba-745e-5d9a-8903-4a02327a7e09"
        # mock_post.userId = "b79cb5ba-745e-5d9a-8903-4a02327a7e09"
        # mock_post.expireAt = "2035-12-31T23:59:59"
        # mock_post.createdAt = datetime(2034, 12, 31, 23, 59, 59)
        # mock_post

        mocker.patch('src.blueprints.operations.create_external_post', return_value={
            "id": "b78c3b3a-785e-5d9a-8903-4a02327a7e87",
            "routedId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "userId": "b79cb5ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2035-12-31T23:59:59",
            "createdAt": datetime(2034, 12, 31, 23, 59, 59)
        })

        response = client.post('/rf003/posts', json=data, headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 201

    def test_create_post_missing_values(self, client, mocker):
        data = {
            "flightId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2028-12-31T23:59:59",
            "plannedStartDate": "2027-12-25T08:00:00",
            "origin": {
                "airportCode": "ORI123",
                "country": "CountryA"
            },
            "bagCost": 150
        }

        mocker.patch.object(QueryUser, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "username": "Juan Test",
            "email": "jjtest@test.com",
            "fullName": "Juan Completo",
            "dni": "12345",
            "phoneNumber": "123144",
            "status": "Activo"
        })

        response = client.post('/rf003/posts', json=data, headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 400

    def test_create_post_no_token(self, client, mocker):
        data = {
            "flightId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2028-12-31T23:59:59",
            "plannedStartDate": "2027-12-25T08:00:00",
            "plannedEndDate": "2027-12-25T12:00:00",
            "origin": {
                "airportCode": "ORI123",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "DES456",
                "country": "CountryB"
            },
            "bagCost": 150
        }

        response = client.post('/rf003/posts', json=data)
        assert response.status_code == 403

    def test_create_post_invalid_token(self, client, mocker):
        data = {
            "flightId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2028-12-31T23:59:59",
            "plannedStartDate": "2027-12-25T08:00:00",
            "plannedEndDate": "2027-12-25T12:00:00",
            "origin": {
                "airportCode": "ORI123",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "DES456",
                "country": "CountryB"
            },
            "bagCost": 150
        }

        response = client.post('/rf003/posts', json=data, headers={'Authorization': INVALID_TOKEN})
        assert response.status_code == 401

    def test_create_post_invalid_userId_token(self, client, mocker):
        data = {
            "flightId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2028-12-31T23:59:59",
            "plannedStartDate": "2027-12-25T08:00:00",
            "plannedEndDate": "2027-12-25T12:00:00",
            "origin": {
                "airportCode": "ORI123",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "DES456",
                "country": "CountryB"
            },
            "bagCost": 150
        }

        response = client.post('/rf003/posts', json=data, headers={'Authorization': INVALID_TOKEN_USERID})
        assert response.status_code in [401, 403]

    def test_search_route_500_response(self, client, mocker):
        data = {
            "flightId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2035-12-31T23:59:59",
            "plannedStartDate": "2024-12-25T08:00:00",
            "plannedEndDate": "2024-12-25T12:00:00",
            "origin": {
                "airportCode": "ORI123",
                "country": "CountryA"
            },
            "destiny": {
                "airportCode": "DES456",
                "country": "CountryB"
            },
            "bagCost": 150
        }

        mocker.patch('requests.get', return_value=MagicMock(status_code=500))

        response = client.post('/rf003/posts', json=data, headers={'Authorization': VALID_TOKEN})

        assert response.status_code == 500
