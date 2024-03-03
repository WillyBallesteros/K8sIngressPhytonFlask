from src.main import app
import json
import pytest
from src.models.model import session
from src.models.route import Route
from tests.utils.utils import VALID_TOKEN, INVALID_TOKEN, INVALID_TOKEN_EXPIRE_DATE, INVALID_TOKEN_USERID
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperations:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_delete = self.mock_query.return_value.delete
        self.mock_add = mocker.patch.object(session, 'add')
        self.mock_commit = mocker.patch.object(session, 'commit')
        self.mock_exists_route = mocker.patch('src.commands.exists.ExistsFlight.execute', return_value=False)
        self.mock_route = Route(flightId="867", sourceAirportCode="LIM", sourceCountry="Peru", destinyAirportCode="MIA", destinyCountry="Inglaterra", bagCost=100, plannedStartDate="2024-02-12T16:33:26.612Z", plannedEndDate="2024-02-12T16:33:26.612Z")
        self.mock_create_route = mocker.patch('src.commands.create.CreateFlight.execute', return_value=self.mock_route)        
        self.mock_delete_route = mocker.patch('src.commands.delete.DeleteRoute.execute', return_value=200)
    
    def test_create_route_success(self, client):
        user_data = {
            "flightId":"867", 
            "sourceAirportCode":"LIM", 
            "sourceCountry":"Peru", 
            "destinyAirportCode":"MIA", 
            "destinyCountry":"Inglaterra", 
            "bagCost":100, 
            "plannedStartDate":"2024-02-12T16:33:26.612Z", 
            "plannedEndDate":"2024-03-12T16:33:26.612Z"
        }

        response = client.post('/routes', json=user_data, headers={'Authorization': VALID_TOKEN})
        
        assert response.status_code == 201
        response_json = response.get_json()
        assert "id" in response_json
        assert "createdAt" in response_json
        
        self.mock_exists_route.assert_called_once()
    
    def test_create_route_witout_token(self, client):
        user_data = {
            "flightId":"867", 
            "sourceAirportCode":"LIM", 
            "sourceCountry":"Peru", 
            "destinyAirportCode":"MIA", 
            "destinyCountry":"Inglaterra", 
            "bagCost":100, 
            "plannedStartDate":"2024-02-12T16:33:26.612Z", 
            "plannedEndDate":"2024-03-12T16:33:26.612Z"
        }

        response = client.post('/routes', json=user_data)
        
        assert response.status_code == 403
    
    def test_create_route_invalid_token(self, client):
        user_data = {
            "flightId":"867", 
            "sourceAirportCode":"LIM", 
            "sourceCountry":"Peru", 
            "destinyAirportCode":"MIA", 
            "destinyCountry":"Inglaterra", 
            "bagCost":100, 
            "plannedStartDate":"2024-02-12T16:33:26.612Z", 
            "plannedEndDate":"2024-03-12T16:33:26.612Z"
        }

        response = client.post('/routes', json=user_data, headers={'Authorization': INVALID_TOKEN})
        
        assert response.status_code == 401

    def test_reset(self, client):
        mock_delete = self.mock_query.return_value.delete

        response = client.post('/routes/reset')
            
        response_json = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert 'msg' in response_json
        assert response_json['msg'] == "Todos los datos fueron eliminados"

        mock_delete.assert_called_once()
    
    def test_ping(self, client):
        response = client.get('/routes/ping')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "pong"

    # def test_delete_existing_route(self, client, mocker):
    #   mocker.patch('src.commands.delete.DeleteRoute.execute', return_value=200)

    #   response = client.delete('/routes')

    #   assert response.status_code == 200
    #   assert response.json == {"message": "el trayecto fue eliminado"}

    # def test_delete_nonexistent_route(self, client):
    #   response = client.delete('/routes/999')
    #   assert response.status_code == 404
    #   assert response.json == {"error": "Route not found"}