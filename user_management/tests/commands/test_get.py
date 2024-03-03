import pytest
from unittest.mock import patch, MagicMock
from src.models.model import session
from src.models.user import User
from src.commands.get import GetUser
import base64
import json

@pytest.fixture
def mock_user():
    user = User(username="test", email="testqtest.com", password="12345", fullName="Old Name", dni="Old DNI", phoneNumber="Old Phone", status="Old Status")
    user.id = 1
    user.username = 'testuser'
    return user

@pytest.fixture(autouse=True)
def setup_method(mocker, mock_user):
    mocker.patch.object(session, 'query', return_value=mocker.MagicMock())
    session.query().get.return_value = mock_user

class TestGet():
  def generate_token(self, user_id, invalid_len=False, invalid_format=False):
      token_data = {
          "id": str(user_id),
          "createAt": "2021-01-01T00:00:00",
          "expireAt": "2021-01-02T00:00:00"
      }
      token_str = json.dumps(token_data)
      encoded_token = base64.b64encode(token_str.encode('utf-8')).decode('utf-8')
      
      if invalid_format:
          return "invalid" + encoded_token
      if invalid_len:
          checklen = len(encoded_token) + 1
      else:
          checklen = len(encoded_token)
      
      return f"{encoded_token}CHECKLEN{checklen}"

  def test_get_user_valid_token(self, setup_method):
      token = self.generate_token(1)
      get_user_cmd = GetUser(token)
      user = get_user_cmd.execute()
      
      assert user is None

  def test_get_user_invalid_token_format(self, setup_method):
      token = self.generate_token(1, invalid_format=True)
      get_user_cmd = GetUser(token)
      user = get_user_cmd.execute()
      
      assert user is None

  def test_get_user_invalid_token_length(self, setup_method):
      token = self.generate_token(1, invalid_len=True)
      get_user_cmd = GetUser(token)
      user = get_user_cmd.execute()
      
      assert user is None

  def test_get_user_missing_token(self, setup_method):
      get_user_cmd = GetUser(None)
      user = get_user_cmd.execute()
      
      assert user is None