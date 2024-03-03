from src.commands.create import CreateOffer
from src.main import app
import json
import pytest
from src.models.model import session
from src.models.offer import Offer


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsReset:
    
    
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_delete = self.mock_query.return_value.delete

    def test_reset(self, client):
        mock_delete = self.mock_query.return_value.delete

        response = client.post('/offers/reset')
            
        response_json = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert 'msg' in response_json
        assert response_json['msg'] == "Todos los datos fueron eliminados"

        mock_delete.assert_called_once()

    