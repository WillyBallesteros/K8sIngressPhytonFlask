from src.commands.user import QueryUser
from src.main import app
import json
import pytest
from src.models.model import session
from src.models.offer import Offer
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
        self.mock_exists_route = mocker.patch('src.commands.query.QueryOffer.execute', return_value=False)
        
        userId =  'caa8b54a-eb5e-4134-8ae2-a3946a428ec7'
        routeId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'
        expireAt = '2023-12-31T23:59:59'
        
        postId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'
        userId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'
        description = 'asd'
        size = 'SMALL'
        fragile = True
        offer = 234
        
        self.mock_offer = Offer(postId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7', userId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7' , description = 'asd', size = 'SMALL', fragile = True, offer = 234)
        # self.mock_create_route = mocker.patch('src.commands.create.CreateFlight.execute', return_value=self.mock_offer)        
        # self.mock_delete_route = mocker.patch('src.commands.delete.DeleteRoute.execute', return_value=200)
        
    def test_create_route_success(self, client, mocker):
        user_data = {
            'postId' : 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7',
            'userId' : 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7',
            'description' : 'asd',
            'size' : 'SMALL',
            'fragile': True,
            'offer' : 234
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
        
        response = client.post('/offers', json=user_data, headers={'Authorization': 'Bearer caa9b54a-eb5e-4134-8ae2-a3946a428ec7'})
        
        assert response.status_code == 201
        response_json = response.get_json()
        assert "id" in response_json
        assert "createdAt" in response_json
        
        
    def test_create_route_invalid_token(self, client, mocker):
        user_data = {
            'postId' : 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7',
            'userId' : 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7',
            'description' : 'asd',
            'size' : 'SMALL',
            'fragile': True,
            'offer' : 234
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
        
        response = client.post('/offers', json=user_data, headers={'Authorization': 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'})
        
        assert response.status_code == 403