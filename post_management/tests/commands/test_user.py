import pytest
from unittest.mock import patch, MagicMock
from src.commands.user import QueryUser
from src.models.model import session

@pytest.fixture
def mock_session(mocker):
    mocker.patch.object(session, 'query')
    mocker.patch.object(session, 'commit')

@pytest.fixture
def token():
    return 'Bearer validToken'

class TestQueryUser:
    @patch('src.commands.user.requests.get')
    def test_query_user_success(self, mock_get, mock_session, token):

        expected_user_info = {
            "id": "123",
            "username": "testuser",
            "email": "test@example.com"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_user_info
        mock_get.return_value = mock_response

        query_user_cmd = QueryUser(token=token)
        user_info = query_user_cmd.execute()


        assert user_info == expected_user_info
        mock_get.assert_called_once()

    @patch('src.commands.user.requests.get')
    def test_query_user_failure(self, mock_get, mock_session, token):

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        query_user_cmd = QueryUser(token=token)
        user_info, status_code = query_user_cmd.execute()


        assert user_info == ""
        assert status_code == 404
        mock_get.assert_called_once()
