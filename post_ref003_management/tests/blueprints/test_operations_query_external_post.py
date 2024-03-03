from unittest.mock import patch, MagicMock
import pytest
import requests

from src.blueprints.operations import query_external_post

@pytest.fixture
def mock_request_get(mocker):
    return mocker.patch('requests.get')

def test_query_external_post_success(mock_request_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = [{'id': '123', 'content': 'Test post'}]
    mock_request_get.return_value = fake_response

    posts = query_external_post('user123', 'route456', 'Bearer validtoken', 'http://post.service')

    assert posts == [{'id': '123', 'content': 'Test post'}]

def test_query_external_post_not_found(mock_request_get):
    fake_response = MagicMock()
    fake_response.status_code = 404
    mock_request_get.return_value = fake_response

    posts = query_external_post('user123', 'route456', 'Bearer validtoken', 'http://post.service')

    assert posts is None

def test_query_external_post_error(mock_request_get):
    fake_response = MagicMock()
    fake_response.status_code = 500
    mock_request_get.return_value = fake_response

    with pytest.raises(Exception) as excinfo:
        query_external_post('user123', 'route456', 'Bearer validtoken', 'http://post.service')

    assert str(excinfo.value) == "Error al consultar el post en el servicio de posts"