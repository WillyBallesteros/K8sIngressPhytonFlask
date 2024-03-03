import pytest
from unittest.mock import patch, MagicMock
from src.models.model import session
from src.models.compensation import Compensation
from src.commands.execute_compensation import CompensateSagaOperations
import requests
import uuid

@pytest.fixture
def setup_compensations(db_session, compensations):
    # Aquí podrías preparar tu base de datos o sesión mock con registros de compensación
    # Por simplicidad, se omite la implementación específica de este fixture
    pass

@patch('src.models.model.session.commit')
@patch('src.models.model.session.delete')
@patch('requests.delete')
def test_compensate_saga_operations_execute_success(mock_requests_delete, mock_session_delete, mock_session_commit):
    # Configura mocks
    mock_response = MagicMock()
    mock_response.status_code = 200  # Supongamos éxito para las llamadas HTTP
    mock_requests_delete.return_value = mock_response

    # Configura una lista de compensaciones mock
    transaction_id = str(uuid.uuid4())  # Genera un transactionId de ejemplo
    compensation_post = Compensation(transactionId=transaction_id, action="delete_post", detail="123")
    compensation_route = Compensation(transactionId=transaction_id, action="delete_route", detail="456")

    # Simula la respuesta de session.query().filter_by().all() para devolver las compensaciones mock
    mock_session_query_all = MagicMock(return_value=[compensation_post, compensation_route])
    with patch('src.models.model.session.query', return_value=MagicMock(filter_by=MagicMock(return_value=MagicMock(all=mock_session_query_all)))):
        # Ejecuta el comando
        command = CompensateSagaOperations(transaction_id=transaction_id, auth_header="Bearer token", post_url="post.service", route_url="route.service")
        command.execute()

        # Verificaciones
        assert mock_requests_delete.call_count == 2  # Esperamos dos llamadas a requests.delete, una para cada compensación
        # Verifica que se intentó eliminar cada objeto de compensación
        mock_session_delete.assert_any_call(compensation_post)
        mock_session_delete.assert_any_call(compensation_route)
        mock_session_commit.assert_called_once()  # Verifica que se hizo commit de los cambios


@patch('src.models.model.session.commit')
@patch('src.models.model.session.delete')
@patch('requests.delete')
def test_compensate_saga_operations_http_error(mock_requests_delete, mock_session_delete, mock_session_commit, caplog):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_requests_delete.return_value = mock_response

    transaction_id = str(uuid.uuid4())
    compensation_post = Compensation(transactionId=transaction_id, action="delete_post", detail="123")

    mock_session_query_all = MagicMock(return_value=[compensation_post])
    with patch('src.models.model.session.query', return_value=MagicMock(filter_by=MagicMock(return_value=MagicMock(all=mock_session_query_all)))):
        command = CompensateSagaOperations(transaction_id=transaction_id, auth_header="Bearer token", post_url="post.service", route_url="route.service")
        command.execute()

        assert "Failed to compensate delete_post" in caplog.text
