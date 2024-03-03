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

# class TestOperationsQuery:
    

#     @pytest.fixture(autouse=True)
#     def setup_method(self, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         self.mock_query = mocker.patch.object(session, 'query')

#     def test_query_offer(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers', return_value=None)
#         response = client.get('/offers?post=123&owner=456', headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 200

#     # def test_query_offer_me(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#     #      # Mock para el método common_validations
#     #      mocker.patch('src.blueprints.operations.get_offers', return_value=None)
#     #      response = client.get('/offers?post=123&owner=me', headers={'Authorization': VALID_TOKEN})
#     #      assert response.status_code == 200

#     def test_query_offer_bad_post(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers', return_value=None)
#         response = client.get('/offers?post=&owner=me', headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_query_offer_bad_owner(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers', return_value=None)
#         response = client.get('/offers?post=123&owner=', headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_query_offer_invalid_token(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers', return_value=None)
#         response = client.get('/offers?post=123&owner=456', headers={'Authorization': INVALID_TOKEN})
#         assert response.status_code == 401


#     ## get_offers_id

#     # def test_query_offer_id(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#     #     # Mock para el método common_validations
#     #     mocker.patch('src.blueprints.operations.get_offers_id', return_value=[
#     #                     {
#     #                         "createdAt": "Wed, 07 Feb 2024 18:04:54 GMT",
#     #                         "description": "molestias expedita iusto",
#     #                         "fragile": "true",
#     #                         "id": "cba64edf-4275-4607-b9f8-4d63f65ea04e",
#     #                         "offer": "192",
#     #                         "postId": "null",
#     #                         "size": "LARGE",
#     #                         "userId": "a0514db8-c57e-4b1e-a6f0-3fd2538afec3"
#     #                     }
#     #                 ])
#     #     response = client.get('/offers/acc30af9-8712-4903-9dec-3fff44b9623c', headers={'Authorization': VALID_TOKEN})
#     #     assert response.status_code == 200

#     def test_query_offer_id_not_data(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers_id', return_value=[])
#         response = client.get('/offers/acc30af9-8712-4903-9dec-3fff44b9623c', headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 404

#     def test_query_offer_id_invalid_id(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers_id', return_value=[])
#         response = client.get('/offers/123', headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_query_offer_id_invalid_token(self, client: FlaskClient, mocker: Callable[..., Generator[MockerFixture, None, None]]):
#         # Mock para el método common_validations
#         mocker.patch('src.blueprints.operations.get_offers_id', return_value=[])
#         response = client.get('/offers/acc30af9-8712-4903-9dec-3fff44b9623c', headers={'Authorization': INVALID_TOKEN})
#         assert response.status_code == 401