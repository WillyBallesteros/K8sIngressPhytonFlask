from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import create_external_post
from src.commands.create_compensation import CreateCompensation

@pytest.fixture
def mock_request_post(mocker):
    return mocker.patch('requests.post')

def test_create_external_post_success(mock_request_post, mocker):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 201
    fake_post_response.json.return_value = {'id': 'new-post-id'}
    mock_request_post.return_value = fake_post_response

    mocker.patch.object(CreateCompensation, 'execute')

    json_data = {'expireAt': '2035-12-31T23:59:59'}
    new_post = create_external_post('user-id', 'route-id', json_data, 'Bearer validtoken', 'http://post.service', 'transaction-id')

    assert new_post == {'id': 'new-post-id'}

    CreateCompensation.execute.assert_called_once()

def test_create_external_post_failure(mock_request_post):
    fake_post_response = MagicMock()
    fake_post_response.status_code = 400
    mock_request_post.return_value = fake_post_response

    json_data = {'expireAt': '2035-12-31T23:59:59'}
    with pytest.raises(Exception) as excinfo:
        create_external_post('user-id', 'route-id', json_data, 'Bearer validtoken', 'http://post.service', 'transaction-id')

    assert str(excinfo.value) == "Error al crear el post en el servicio de posts"
