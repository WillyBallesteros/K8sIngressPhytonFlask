import pytest
from unittest.mock import patch
from src.models.model import session
from src.models.score import Score
from src.commands.exists import ExistsScore

@pytest.fixture(autouse=True)
def setup_method(mocker):
    mock_query = mocker.patch.object(session, 'query')
    mock_get = mock_query.return_value.get
    mock_filter = mock_query.return_value.filter
    mock_all = mock_filter.return_value.all

    return mock_query, mock_get, mock_filter, mock_all

class TestExistsUser:
    def test_exists_found(self, setup_method):
        _, _, _, mock_all = setup_method
        mock_all.return_value = [Score(postId= "test_post",offerId= "test_offer",utility= 1)]

        exists_cmd = ExistsScore(postId="test_post", offerId='test_offer')
        result = exists_cmd.execute()

        assert len(result) > 0

    def test_exists_not_found(self, setup_method):
        _, _, _, mock_all = setup_method
        mock_all.return_value = []

        exists_cmd = ExistsScore(postId="test_post", offerId='test_offer')
        result = exists_cmd.execute()

        assert len(result) < 1