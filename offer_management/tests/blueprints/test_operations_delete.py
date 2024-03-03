# from typing import Callable, Generator
# from flask.testing import FlaskClient
# from pytest_mock import MockerFixture
# from src.commands.create import CreateOffer
# from src.main import app
# import json
# import pytest
# from src.models.model import session
# from tests.utils.utils import INVALID_TOKEN, VALID_TOKEN


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# class TestOperationsDelete:
    

#     @pytest.fixture(autouse=True)
#     def setup_method(self, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         self.mock_query = mocker.patch.object(session, 'query')
#         self.mock_delete = self.mock_query.return_value.delete

#     # def test_delete_offer(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#     #     # Mock para el método common_validations
#     #     mocker.patch('src.blueprints.operations.delete_offer', return_value=None)
#     #     response = client.delete('/offers/acc30af9-8712-4903-9dec-3fff44b9623c', headers={'Authorization': VALID_TOKEN})
#     #     assert response.status_code == 200

#     def test_delete_offer_invalid_id(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.delete_offer', return_value=None)
#         response = client.delete('/offers/123', headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_delete_offer_invalid_token(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.delete_offer', return_value=None)
#         response = client.delete('/offers/123', headers={'Authorization': INVALID_TOKEN})
#         assert response.status_code == 401




#     # def test_delete_offer(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#     #     mock_delete = self.mock_query.return_value.delete
#     #     response = client.delete('/offers/acc30af9-8712-4903-9dec-3fff44b9623c', headers={'Authorization': VALID_TOKEN})
#     #     assert response.status_code == 200
#     #     mock_delete.assert_called_once()

    