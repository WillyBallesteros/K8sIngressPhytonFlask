from typing import Callable, Generator
from flask.testing import FlaskClient
from pytest_mock import MockerFixture
from src.commands.query import QueryPost
from src.commands.user import QueryUser
from src.main import app
import pytest
from src.models.model import session
from tests.utils.utils import INVALID_TOKEN, VALID_TOKEN

@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client

class TestOperationsQueryPosts:

    @pytest.fixture(autouse=True)
    def setup_method(self, mocker: MockerFixture):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_query_post_execute = mocker.patch('src.commands.query.QueryPost.execute')
        self.mock_query_user_execute = mocker.patch('src.commands.user.QueryUser.execute')

    def test_query_posts(self, client: FlaskClient, mocker: MockerFixture):
        mock_posts = [{'id': 'c40b683b-ac7b-5d6b-b0eb-549cb20169b9', 'expireAt': '2025-12-31T23:59:59', 'routeId': 'fb3463a0-7d6e-54a3-bcd8-1b93388c648d', 'userId': 'efe7eedd-89c5-56f5-984c-0712ee41a2eb'}]
        self.mock_query_post_execute.return_value = mock_posts

        mock_user = {
            "id": "b79cb3ba-745e-5d9a-8903-4a02327a7e09",
            "username": "Juan Test",
            "email": "jjtest@test.com",
            "fullName": "Juan Completo",
            "dni": "12345",
            "phoneNumber": "123144",
            "status": "Activo"
        }
        self.mock_query_user_execute.return_value = mock_user

        response = client.get('/posts?expire=true&route=fb3463a0-7d6e-54a3-bcd8-1b93388c648d&owner=me', headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 200
        assert response.json == mock_posts

    def test_query_posts_no_data(self, client: FlaskClient, mocker: MockerFixture):
        self.mock_query_post_execute.return_value = []

        response = client.get('/posts', headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 200

    def test_query_posts_invalid_route_id(self, client: FlaskClient, mocker: MockerFixture):
        self.mock_query_post_execute.return_value = []

        response = client.get('/posts?expire=true&route=invalidRouteId&owner=me', headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 400

    def test_query_posts_invalid_user_id(self, client: FlaskClient, mocker: MockerFixture):
        self.mock_query_post_execute.return_value = []

        response = client.get('/posts?expire=true&route=caa8b54a-eb5e-4134-8ae2-a3946a428ec7&owner=fakeUser', headers={'Authorization': VALID_TOKEN})
        assert response.status_code == 400
