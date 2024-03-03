import pytest
from unittest.mock import MagicMock
from src.commands.create import CreateOffer
from src.models.model import session
from src.models.offer import Offer


class TestCreate():
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch.object(session, 'add')
        self.mock_commit = mocker.patch.object(session, 'commit')

    def test_create(self):
        
        test_data = {
            "postId":'postId', 
            "userId":'userId', 
            "description":'description', 
            "size":'size', 
            "fragile":'fragile', 
            "offer":'offer'
        }
        
        result = CreateOffer(**test_data).execute()
        self.mock_add.assert_called_once()
        self.mock_commit.assert_called_once()
        assert isinstance(result, Offer)
        assert result.postId == test_data['postId']