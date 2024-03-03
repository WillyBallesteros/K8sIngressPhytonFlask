import pytest
from unittest.mock import patch
from src.models.model import session
from src.models.user import User
from src.commands.exists import ExistsUser

@pytest.fixture(autouse=True)
def setup_method(mocker):
    mock_query = mocker.patch.object(session, 'query')
    mock_get = mock_query.return_value.get
    mock_filter = mock_query.return_value.filter
    mock_first = mock_filter.return_value.first

    return mock_query, mock_get, mock_filter, mock_first

class TestExistsUser:
    def test_exists_user_by_id_found(self, setup_method):
        _, mock_get, _, _ = setup_method
        mock_get.return_value = User(
            username="testuser",
            password= "testpassword",
            email= "test@example.com",
            fullName= "Test User",
            dni= "12345678",
            phoneNumber= "1234567890",
            status= "POR_VERIFICAR")

        exists_user_cmd = ExistsUser(id=1)
        result = exists_user_cmd.execute()

        assert result == True

    def test_exists_user_by_id_not_found(self, setup_method):
        _, mock_get, _, _ = setup_method
        mock_get.return_value = None

        exists_user_cmd = ExistsUser(id=1)
        result = exists_user_cmd.execute()

        assert result == False

    def test_exists_user_by_username_found(self, setup_method):
        _, _, _, mock_first = setup_method
        mock_first.return_value = User(
            username="testuser",
            password= "testpassword",
            email= "test@example.com",
            fullName= "Test User",
            dni= "12345678",
            phoneNumber= "1234567890",
            status= "POR_VERIFICAR")

        exists_user_cmd = ExistsUser(id=None, username='testuser')
        result = exists_user_cmd.execute()

        assert result == True

    def test_exists_user_by_email_found(self, setup_method):
        _, _, _, mock_first = setup_method
        mock_first.return_value = User(
            username="testuser",
            password= "testpassword",
            email= "test@example.com",
            fullName= "Test User",
            dni= "12345678",
            phoneNumber= "1234567890",
            status= "POR_VERIFICAR")

        exists_user_cmd = ExistsUser(id=None, email='test@example.com')
        result = exists_user_cmd.execute()

        assert result == True
