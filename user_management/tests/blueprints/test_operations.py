from src.main import app
import json
import pytest
from src.models.model import session
from src.models.user import User
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
        self.mock_exists_user = mocker.patch('src.commands.exists.ExistsUser.execute', return_value=False)
        self.mock_user = User(username="test", email="testqtest.com", password="12345", fullName="Old Name", dni="Old DNI", phoneNumber="Old Phone", status="Old Status")
        self.mock_create_user = mocker.patch('src.commands.create.CreateUser.execute', return_value=self.mock_user)
        mocker.patch('src.commands.update.UpdateUser.execute')


    def test_reset(self, client):
        mock_delete = self.mock_query.return_value.delete

        response = client.post('/users/reset')
            
        response_json = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert 'msg' in response_json
        assert response_json['msg'] == "Todos los datos fueron eliminados"

        assert self.mock_query.call_count ==  2

    def test_create_user_success(self, client):
        user_data = {
            "id": "12345",
            "username": "newuser",
            "password": "securepassword",
            "email": "user@example.com",
            "fullName": "New User",
            "dni": "12345678",
            "phoneNumber": "1234567890"
        }

        response = client.post('/users', json=user_data)
        
        assert response.status_code == 201
        response_json = response.get_json()
        assert "id" in response_json
        assert "createdAt" in response_json
        
        self.mock_exists_user.assert_called_once() 

    def test_user_not_exists(self, client):
        response = client.patch('/users/1', json={"fullName": "Updated Name"})
        assert response.status_code == 404
        assert response.get_data(as_text=True) == "El usuario no existe"

    def test_update_user_valid(self, client, mocker):
        mocker.patch('src.commands.exists.ExistsUser.execute', return_value=True)
        response = client.patch('/users/1', json={
            "fullName": "Updated Name",
            "phoneNumber": "1234567890",
            "dni": "12345678",
            "status": "active"
        })
        assert response.status_code == 200
        response_json = response.get_json()
        assert response_json['msg'] == "el usuario ha sido actualizado"

    def test_no_fields_to_update(self, client):
        response = client.patch('/users/1', json={})
        assert response.status_code == 400
        assert response.get_data(as_text=True) == "No hay campos para actualizar"

    def test_missing_credentials(self, client):
        response = client.post('/users/auth', json={})
        assert response.status_code == 404

        response = client.post('/users/auth', json={"username": "testuser"})
        assert response.status_code == 400

    @patch('src.commands.token.CreateToken.execute')
    def test_invalid_credentials(self, mock_create_token, client):
        mock_create_token.return_value = None
        response = client.post('/users/auth', json={"username": "testuser", "password": "wrongpass"})
        assert response.status_code == 404

    @patch('src.commands.token.CreateToken.execute')
    def test_auth_success(self, mock_create_token, client):
        mock_create_token.return_value = {"token": "fakeToken123", "expireAt": "2023-01-01T00:00:00"}
        response = client.post('/users/auth', json={"username": "testuser", "password": "correctpass"})
        
        assert response.status_code == 200
        response_json = response.get_json()
        assert "token" in response_json and response_json["token"] == "fakeToken123"

    @patch('src.commands.get.GetUser.execute')
    def test_missing_or_invalid_auth_header(self, mock_get_user, client):
        response = client.get('/users/me')
        assert response.status_code == 403
        
        response = client.get('/users/me', headers={'Authorization': 'Token abc123'})
        assert response.status_code == 403

    @patch('src.commands.get.GetUser.execute')
    def test_user_not_found(self, mock_get_user, client):
        mock_get_user.return_value = None
        response = client.get('/users/me', headers={'Authorization': 'Bearer fakeToken123'})
        assert response.status_code == 401

    @patch('src.commands.get.GetUser.execute')
    def test_get_user_success(self, mock_get_user, client):
        mock_get_user.return_value = self.mock_user
        response = client.get('/users/me', headers={'Authorization': 'Bearer validToken123'})
        
        assert response.status_code == 200
        response_json = response.get_json()
        assert response_json['id'] == str(self.mock_user.id)
        assert response_json['username'] == self.mock_user.username

    def test_ping(self, client):
        response = client.get('/users/ping')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "pong"
