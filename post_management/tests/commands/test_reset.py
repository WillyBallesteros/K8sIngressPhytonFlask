import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.models.post import Post
from src.commands.reset import ResetPost

class TestResetPost():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_delete = self.mock_query.return_value.delete
        self.mock_delete.return_value = 5
        self.mock_commit = mocker.patch('src.models.model.session.commit')

    def test_reset_post(self):
        reset_post = ResetPost()
        num_deleted = reset_post.execute()
        self.mock_query.assert_called_once_with(Post)
        self.mock_delete.assert_called_once()
        self.mock_commit.assert_called_once()
        assert num_deleted == 5
