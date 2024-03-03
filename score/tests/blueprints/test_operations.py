from src.main import app
import json
import pytest
from src.models.model import session
from src.models.score import Score
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
        self.mock_score = Score(postId= "test_post",offerId= "test_offer",utility= 1)
        self.mock_exists = mocker.patch('src.commands.exists.ExistsScore.execute', return_value=[])        
        self.mock_create = mocker.patch('src.commands.create.CreateScore.execute', return_value=self.mock_score)        
        self.mock_update = mocker.patch('src.commands.update.UpdateScore.execute', return_value=self.mock_score)        


    def test_create_success(self, client):
        data = {
            "postId": "post_1",
            "offerId": "offer_5",
            "offerValue": 200,
            "bagSize":"LARGE",
            "bagCost":1
        }

        response = client.post('/score/utility', json=data)
        
        assert response.status_code == 201

    def test_create_failed_1(self, client):
        data = {
            "postId": "post_1",
            "offerValue": 200,
            "bagSize":"LARGE",
            "bagCost":1
        }

        response = client.post('/score/utility', json=data)
        
        assert response.status_code == 400

    def test_create_failed_2(self, client):
        data = {
            "postId": "post_1",
            "offerId": "offer_5",
            "offerValue": 200,
            "bagSize":"",
            "bagCost":1
        }

        response = client.post('/score/utility', json=data)
        
        assert response.status_code == 412

    def test_ping(self, client):
        response = client.get('/score/ping')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "pong"
