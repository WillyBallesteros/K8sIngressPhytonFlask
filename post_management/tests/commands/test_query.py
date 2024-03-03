# import pytest
# from unittest.mock import patch, MagicMock
# from datetime import datetime, timedelta
# from src.commands.query import QueryPost
# from src.models.post import Post

# # Asumiendo la existencia de un app Flask en el contexto
# from src.main import app

# @pytest.fixture
# def posts_data():
#     post1 = MagicMock(spec=Post)
#     post1.configure_mock(id="1", routeId="6b7fcbb7-1441-3c17-8580-7fc490f21e59", userId="bd2cbad1-6ccf-48e3-bb92-bc9961bc011e", expireAt=datetime.utcnow() + timedelta(days=1))

#     post2 = MagicMock(spec=Post)
#     post2.configure_mock(id="2", routeId="962d8197-4d0b-3a25-8e26-25ac0978de72", userId="bd3cbad1-6ccf-48e3-bb92-bc9961bc011e", expireAt=datetime.utcnow() - timedelta(days=1))

#     return [post1, post2]

# @pytest.fixture
# def mock_session(posts_data):
#     with patch('src.models.model.session') as mock_session:
#         mock_query = mock_session.query.return_value
#         mock_filter = mock_query.filter.return_value
#         mock_filter.all.return_value = posts_data  # Ensure this correctly simulates the DB response
#         yield mock_session

# def test_query_post_execute_future_expire(mock_session, posts_data):

#     query_post = QueryPost(expire=False)
#     result = query_post.execute()
#     result_data = result.get_json()

#     expected_route_id = [post.routeId for post in posts_data if post.expireAt > datetime.utcnow()][0]
#     assert result_data[0]['routeId'] == expected_route_id
