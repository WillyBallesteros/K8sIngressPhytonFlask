from typing import Callable, Generator
from flask.testing import FlaskClient
from pytest_mock import MockerFixture
from src.commands.delete import DeletePost
from src.commands.create import CreatePost
from src.models.post import Post
from src.main import app
import pytest
from src.models.model import session
from tests.utils.utils import INVALID_TOKEN, VALID_TOKEN

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsDeletePosts:

    @pytest.fixture(autouse=True)
    def setup_method(self, mocker: Callable[..., Generator[MockerFixture, None, None]]):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_delete = self.mock_query.return_value.delete
        self.mock_query_post_execute = mocker.patch('src.commands.query.QueryPost.execute')

    def test_delete_post_invalid_id(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
        mocker.patch('src.blueprints.operations.delete_post', return_value=None)
        response = client.delete('/posts/123', headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 400

    def test_delete_post_invalid_token(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):

        mocker.patch('src.blueprints.operations.delete_post', return_value=None)
        response = client.delete('/posts/456', headers={'Authorization': INVALID_TOKEN})
        assert response.status_code == 401
