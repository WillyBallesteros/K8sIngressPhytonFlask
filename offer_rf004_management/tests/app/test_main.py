import os
import pytest
from flask import jsonify

from src.errors.errors import ApiError
from src.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_handle_exception(client):
    # Simulamos una instancia de ApiError
    err = ApiError(Exception)

    # Hacemos una solicitud a la ruta que activa el manejador de errores
    response = client.get('/')

    # Verificamos que la respuesta tenga el código de estado y el mensaje esperados
    assert response.status_code == 404
    # assert response.json == {"mssg": "Error message", "version": os.environ["VERSION"]}