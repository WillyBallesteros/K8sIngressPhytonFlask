import pytest
from unittest.mock import MagicMock
from src.commands.create import CreatePost
from src.models.post import Post
from src.models.model import session

class TestCreatePost:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        # Mock para session.add() y session.commit() para no afectar la base de datos real
        self.mock_add = mocker.patch('src.models.model.session.add')
        self.mock_commit = mocker.patch('src.models.model.session.commit')

    def test_create_post(self):
        userId = 'user123'
        routeId = 'route456'
        expireAt = '2023-12-31T23:59:59'

        result = CreatePost(userId=userId, routeId=routeId, expireAt=expireAt).execute()

        assert isinstance(result, Post)
        assert result.userId == userId
        assert result.routeId == routeId
        assert result.expireAt == expireAt


        self.mock_add.assert_called_once()
        self.mock_commit.assert_called_once()
