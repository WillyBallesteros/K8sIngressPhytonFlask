import pytest
from unittest.mock import patch, MagicMock
from src.models.model import session
from src.models.score import Score
from src.commands.get import GetScoreByPost
import base64
import json

@pytest.fixture(autouse=True)
def setup_method(mocker):
    mock_query = mocker.patch.object(session, 'query')
    mock_get = mock_query.return_value.get
    mock_filter = mock_query.return_value.filter_by
    mock_order = mock_filter.return_value.order_by
    mock_all = mock_order.return_value.all

    return mock_query, mock_get, mock_filter, mock_all

class TestGet():
  def test_get_not_exists(self, setup_method):
      _, _, _, mock_all = setup_method
      mock_all.return_value = []
      get_cmd = GetScoreByPost(postId="test_post")
      result = get_cmd.execute()
      
      assert len(result) == 0

  def test_get_none_post(self, setup_method):
      get_cmd = GetScoreByPost(postId=None)
      result = get_cmd.execute()
      
      assert result is None

  def test_get_exists(self, setup_method):
      _, _, _, mock_all = setup_method
      mock_all.return_value = [
          Score(
            postId= "test_post",
            offerId= "test_offer",
            utility= 1)
          ]

      exists_cmd = GetScoreByPost(postId="test_post")
      result = exists_cmd.execute()

      assert len(result) > 0