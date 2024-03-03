import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.models.compensation import Compensation
from src.commands.create import CreateCompensation

class TestCompensationCreate():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch.object(session, 'add')
        self.mock_commit = mocker.patch.object(session, 'commit')
  
    def test_compensation_create(self):
        test_data = {
            "transaction_id": "testuser",
            "action": "testpassword",
            "path": "test@example.com",
            "detail": "Test User"
        }

        created = CreateCompensation(transactionId='transaction_id', action='action', path='path', detail='detail').execute()

        self.mock_add.assert_called_once()
        self.mock_commit.assert_called_once()