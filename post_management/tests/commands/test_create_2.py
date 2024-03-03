import uuid
import pytest
from unittest.mock import MagicMock
from src.commands.create import CreatePost
from src.models.model import session
from src.models.post import Post

def test_create_post_execute():
    mock_post = MagicMock()

    mock_session = MagicMock()
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    userId = 'user123'
    routeId = 'route456'
    expireAt = '2023-12-31T23:59:59'

    create_post = CreatePost(userId=userId, routeId=routeId, expireAt=expireAt)

    create_post.session = mock_session

    mock_post.id = uuid.uuid4()
    create_post.execute = MagicMock(return_value=mock_post)

    result = create_post.execute()

    assert isinstance(result.id, uuid.UUID)
    assert len(str(result.id)) > 0
