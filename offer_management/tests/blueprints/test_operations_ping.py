from typing import Callable, Generator
from flask.testing import FlaskClient
from pytest_mock import MockerFixture
from src.commands.create import CreateOffer
from src.main import app
import json
import pytest
from src.models.model import session
from tests.utils.utils import INVALID_TOKEN, VALID_TOKEN


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestOperationsQuery:
    

    @pytest.fixture(autouse=True)
    def setup_method(self, mocker: Callable[..., Generator[MockerFixture, None, None]]):
        self.mock_query = mocker.patch.object(session, 'query')

    def test_query_offer(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
        # Mock para el método common_validations
        mocker.patch('src.blueprints.operations.ping', return_value=None)
        response = client.get('/offers/ping')
        assert response.status_code == 200
