# import pytest
# from unittest.mock import patch
# from src.models.model import session
# from src.models.offer import Offer
# from src.commands.query import QueryOffer

# @pytest.fixture(autouse=True)
# def setup_method(mocker):
#     mock_query = mocker.patch.object(session, 'query')
#     mock_get = mock_query.return_value.get
#     mock_filter = mock_query.return_value.filter
#     mock_first = mock_filter.return_value.first

#     return mock_query, mock_get, mock_filter, mock_first

# class TestQuery:
#     # def test_exists_Offer(self, setup_method):
#     #     _, mock_get, _, _ = setup_method
        
#     #     userId =  'caa8b54a-eb5e-4134-8ae2-a3946a428ec7'
        
#     #     postId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'
#     #     userId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'
#     #     description = 'asd'
#     #     size = 'SMALL'
#     #     fragile = True
#     #     offer = 234
        
#     #     mock_get.return_value = Offer(
#     #         postId=postId, userId=userId, description=description, size=size, fragile=fragile, offer=offer)

#     #     exists_route_cmd = QueryOffer()
#     #     result = exists_route_cmd.execute()

#     #     assert result == True
#     #