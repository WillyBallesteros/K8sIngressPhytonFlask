import pytest
from src.commands.create import CreatePost
from src.commands.user import QueryUser
from src.main import app
from src.models.model import session
from src.models.post import Post
from tests.utils.utils import VALID_TOKEN, INVALID_TOKEN, INVALID_TOKEN_USERID

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsCreatePost:

    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')

    def test_create_post_success(self, client, mocker):
        data = {
            "routeId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2035-12-31T23:59:59"
        }

        mocker.patch.object(CreatePost, 'execute', return_value=Post(
            userId="b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            routeId=data['routeId'],
            expireAt=data['expireAt']
        ))

        mocker.patch.object(QueryUser, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "username": "Juan Test",
            "email": "jjtest@test.com",
            "fullName": "Juan Completo",
            "dni": "12345",
            "phoneNumber": "123144",
            "status": "Activo"
        })

        response = client.post('/posts', json=data, headers={'Authorization': VALID_TOKEN})

        response_data = response.get_json()
        assert response.status_code == 201

    def test_create_post_future_expire_at(self, client, mocker):
      data = {
          "routeId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
          "expireAt": "2000-01-01T00:00:00"
      }

      response = client.post('/posts', json=data, headers={'Authorization': VALID_TOKEN})

      response_data = response.get_json()
      assert response_data['msg'] == "La fecha expiración no es válida"

    def test_create_post_invalid_date_format(self, client):
      data = {
          "routeId": "route123",
          "expireAt": "not-a-date"
      }

      response = client.post('/posts', json=data, headers={'Authorization': VALID_TOKEN})
      assert response.status_code == 400

    def test_create_post_invalid_userId(self, client, mocker):
        data = {
            "routeId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "expireAt": "2023-12-31T23:59:59",
            "userId": "invalidUserId"
        }
        mocker.patch.object(CreatePost, 'execute', return_value=Post(
            routeId=data['routeId'],
            userId=None,
            expireAt=data['expireAt']
        ))

        response = client.post('/posts', json=data, headers={'Authorization': INVALID_TOKEN_USERID})
        assert response.status_code == 401


    def test_create_post_invalid_routeId(self, client, mocker):
      data = {
          "routeId": None,
          "expireAt": "2023-12-31T23:59:59"
      }

      response = client.post('/posts', json=data, headers={'Authorization': VALID_TOKEN})
      assert response.status_code == 400

    def test_create_post_missing_additional_fields(self, client):
      incomplete_data = {
          "routeId": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
      }
      response = client.post('/posts', json=incomplete_data, headers={'Authorization': VALID_TOKEN})
      assert response.status_code == 400

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

        mock_response = mocker.MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = [
            {
                "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
                "flightId": "flight123",
                "plannedStartDate": "2028-12-25T08:00:00",
                "plannedEndDate": "2028-12-25T12:00:00",
                "sourceAirportCode": "ORI123",
                "sourceCountry": "CountryA",
                "destinyAirportCode": "DES456",
                "destinyCountry": "CountryB"
            }
        ]
        mocker.patch('requests.get', return_value=mock_response)


        mocker.patch('src.utils.utils.get_valid_id_route', return_value="b79cb3ba-745e-5d9a-8903-4a02327a7e09")

        fake_response = mocker.MagicMock()
        fake_response.status_code = 201
        fake_response.json.return_value = {"id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09"}
        mocker.patch('requests.post', return_value=fake_response)

        mocker.patch.object(QueryUser, 'execute', return_value= {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "username": "Juan Test",
            "email": "jjtest@test.com",
            "fullName": "Juan Completo",
            "dni": "12345",
            "phoneNumber": "123144",
            "status": "Activo"
        })


        mocker.patch.object(CreatePost, 'execute', return_value=Post(
            routeId="b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            userId="b78cb3ba-785e-5d9a-8903-4a02327a7e09",
            expireAt=data['expireAt']
        ))

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
