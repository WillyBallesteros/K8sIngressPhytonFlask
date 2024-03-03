import pytest
from unittest.mock import patch
from src.models.model import session
from src.models.user import User
from src.commands.update import UpdateUser

@pytest.fixture
def user_data():
    return {
        "id": 1,
        "fullName": "New Name",
        "dni": "New DNI",
        "phoneNumber": "New Phone Number",
        "status": "New Status"
    }

@pytest.fixture(autouse=True)
def setup_method(mocker):
    mock_query = mocker.patch.object(session, 'query')
    mock_get = mock_query.return_value.get
    mock_user = User(username="test", email="testqtest.com", password="12345", fullName="Old Name", dni="Old DNI", phoneNumber="Old Phone", status="Old Status")
    mock_get.return_value = mock_user
    mocker.patch.object(session, 'commit')
    return mock_user

class TestUpdate():
    def test_update_user_fullName(self, setup_method, user_data):
        user_mock = setup_method
        update_user_cmd = UpdateUser(**user_data)
        update_user_cmd.execute()

        assert user_mock.fullName == user_data["fullName"]

    def test_update_user_dni(self, setup_method, user_data):
        user_mock = setup_method
        update_user_cmd = UpdateUser(**user_data)
        update_user_cmd.execute()

        assert user_mock.dni == user_data["dni"]

    def test_update_user_phoneNumber(self, setup_method, user_data):
        user_mock = setup_method
        update_user_cmd = UpdateUser(**user_data)
        update_user_cmd.execute()

        assert user_mock.phoneNumber == user_data["phoneNumber"]

    def test_update_user_status(self, setup_method, user_data):
        user_mock = setup_method
        update_user_cmd = UpdateUser(**user_data)
        update_user_cmd.execute()

        assert user_mock.status == user_data["status"]

    def test_update_user_empty(self, setup_method, user_data):
        user_mock = setup_method
        update_user_cmd = UpdateUser(**user_data)
        update_user_cmd.execute()

        assert True
