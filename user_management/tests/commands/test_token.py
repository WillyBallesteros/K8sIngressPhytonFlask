import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
import base64
import json
from src.models.model import session
from src.models.user import User
from src.commands.token import CreateToken

@pytest.fixture
def user_fixture():
    user = User(username="test", email="testqtest.com", password="12345", fullName="Old Name", dni="Old DNI", phoneNumber="Old Phone", status="Old Status")
    user.id = 1
    user.username = 'testuser'
    user.password = 'testpass'
    return user

@pytest.fixture
def setup_method(mocker, user_fixture):
    mocker.patch.object(session, 'query', return_value=mocker.MagicMock())
    session.query().filter().first.return_value = user_fixture

class TestToken():
    def test_create_token_wrong_password(self, setup_method, user_fixture):
        create_token_cmd = CreateToken('testuser', 'wrongpass')
        result = create_token_cmd.execute()
        
        assert result is None

    def test_create_token_no_user(self, setup_method):
        session.query().filter().first.return_value = None
        
        create_token_cmd = CreateToken('unknown', 'pass')
        result = create_token_cmd.execute()
        
        assert result is None