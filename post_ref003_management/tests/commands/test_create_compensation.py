import uuid
import pytest
from unittest.mock import MagicMock
from src.commands.create_compensation import CreateCompensation
from src.models.model import session
from src.models.compensation import Compensation

def test_create_compensation_execute():
    mock_post = MagicMock()

    mock_session = MagicMock()
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    transaction_id = str(uuid.uuid4())
    action = "some_action"
    detail = "some_detail"

    create_compensation = CreateCompensation(transactionId=transaction_id, action=action, detail=detail)

    create_compensation.session = mock_session

    mock_post.id = uuid.uuid4()
    create_compensation.execute = MagicMock(return_value=mock_post)

    result = create_compensation.execute()

    assert isinstance(result.id, uuid.UUID)
    assert len(str(result.id)) > 0
