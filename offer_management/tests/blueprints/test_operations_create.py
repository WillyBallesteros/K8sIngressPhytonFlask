# from src.commands.create import CreateOffer
# from src.main import app
# import json
# import pytest
# from src.models.model import session
# from src.models.offer import Offer
# from tests.utils.utils import VALID_TOKEN, INVALID_TOKEN, INVALID_TOKEN_EXPIRE_DATE, INVALID_TOKEN_USERID

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# class TestOperationsCreate:
    
#     @pytest.fixture(autouse=True)
#     def setup_method(self, mocker):
#         self.mock_query = mocker.patch.object(session, 'query')

#     def test_create_offer(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 201

#     def test_create_offer_id(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId='132123123',
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/rf004/posts/132123123/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 201

#     def test_create_offer_id_missing_values(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "fragile": True,
#                 "offer": 703
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId='132123123',
#             description=data['description'],
#             size='MEDIUM',
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/rf004/posts/132123123/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_create_offer_no_token(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data)
#         assert response.status_code == 403

#     def test_create_offer_token_invalido(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': INVALID_TOKEN})
#         assert response.status_code == 401

#     def test_create_offer_missing_fields(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description='description',
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_create_offer_invalid_size(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "EXTRA",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 412

#     def test_create_offer_positive_offer(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": -1,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 412

#     def test_create_offer_fragile_bad_value(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": 1,
#                 "offer": 123,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': VALID_TOKEN})
#         assert response.status_code == 400

#     def test_create_offer_token_invalido_userId(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': INVALID_TOKEN_USERID})
#         assert response.status_code == 401

#     def test_create_offer_token_invalido_expireAt(self, client, mocker):
#         data = {
#                 "postId": "asdasdasd",
#                 "description": "nobis suscipit velit",
#                 "size": "MEDIUM",
#                 "fragile": True,
#                 "offer": 703,
#                 "userId":"132123123"
#             }
#         # Mock para CreateOffer.execute()
#         mocker.patch.object(CreateOffer, 'execute', return_value=Offer(
#             postId=data['postId'],
#             userId=data['userId'],
#             description=data['description'],
#             size=data['size'],
#             fragile=data['fragile'],
#             offer=data['offer']
#         ))
        
#         response = client.post('/offers', json=data, headers={'Authorization': INVALID_TOKEN_EXPIRE_DATE})
#         assert response.status_code == 401