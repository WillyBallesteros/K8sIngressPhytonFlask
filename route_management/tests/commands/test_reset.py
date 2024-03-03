import pytest
from unittest.mock import MagicMock
from src.models.model import session
from src.models.route import Route
from src.commands.reset import ResetRoute

class TestReset():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_query = mocker.patch.object(session, 'query')
        self.mock_delete = self.mock_query.return_value.delete
        self.mock_delete.return_value = 0

    def test_reset(self):
        ResetRoute().execute()

        self.mock_query.assert_called_once_with(Route)
        self.mock_delete.assert_called_once()