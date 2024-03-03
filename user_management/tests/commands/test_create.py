import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.models.user import User
from src.commands.create import CreateUser

class TestCreate():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch.object(session, 'add')
        self.mock_commit = mocker.patch.object(session, 'commit')
  
    def test_create(self):
        test_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "fullName": "Test User",
            "dni": "12345678",
            "phoneNumber": "1234567890"
        }

        user_created = CreateUser(**test_data).execute()

        self.mock_add.assert_called_once()
        self.mock_commit.assert_called_once()
        assert isinstance(user_created, User)
        assert user_created.username == test_data['username']
        assert user_created.status == "POR_VERIFICAR"