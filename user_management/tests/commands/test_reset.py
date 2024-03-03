import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.commands.reset import ResetDB

class TestReset():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_delete = self.mock_query.return_value.delete
        self.mock_delete.return_value = 0

    def test_reset(self):
        ResetDB().execute()

        assert self.mock_query.call_count ==  2