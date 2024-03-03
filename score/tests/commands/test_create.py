import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.models.score import Score
from src.commands.create import CreateScore

class TestCreate():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch.object(session, 'add')
        self.mock_commit = mocker.patch.object(session, 'commit')
  
    def test_create(self):
        test_data = {
            "postId": "test_post",
            "offerId": "test_offer",
            "utility": 1
        }

        user_created = CreateScore(**test_data).execute()

        self.mock_add.assert_called_once()
        self.mock_commit.assert_called_once()
        assert isinstance(user_created, Score)
        assert user_created.postId == test_data['postId']