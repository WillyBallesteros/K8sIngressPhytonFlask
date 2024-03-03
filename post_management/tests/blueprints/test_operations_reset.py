from src.main import app
import pytest
from src.models.model import session
from src.models.post import Post
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsReset:

    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_delete = mocker.patch('src.models.model.session.query.delete')

    # def test_reset_posts(self, client):

    #     response = client.post('/posts/reset')


    #     response_json = json.loads(response.data.decode('utf-8'))


    #     assert response.status_code == 200
