from src.main import app
import pytest

@pytest.fixture
def client():
    """Create and configure a test client for the app."""
    app.testing = True
    with app.test_client() as client:
        yield client
        
def test_ping_route(client):
    response = client.get('/rf005/ping')
    assert response.status_code == 200
    assert response.data == b'pong'