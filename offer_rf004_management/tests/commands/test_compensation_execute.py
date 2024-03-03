import pytest
from unittest.mock import patch, MagicMock
from src.models.model import session
from src.models.compensation import Compensation
from src.commands.execute_compensation import ExecuteCompensation
import requests
import uuid

from src.utils.utils import DELETE

@pytest.fixture
def setup_compensations(db_session, compensations):
    pass

@patch('src.models.model.session.commit')
@patch('src.models.model.session.delete')
@patch('requests.delete')
def test_compensation_execute(mock_requests_delete, mock_session_delete, mock_session_commit):
    # Configura mocks
    mock_response = MagicMock()
    mock_response.status_code = 200  # Supongamos éxito para las llamadas HTTP
    mock_requests_delete.return_value = mock_response

    # Configura una lista de compensaciones mock
    transaction_id = str(uuid.uuid4())  # Genera un transactionId de ejemplo
    compensation_1 = Compensation(transactionId=transaction_id, action=DELETE, path="delete_path", detail="123")
    compensation_2 = Compensation(transactionId=transaction_id, action=DELETE, path="delete_path", detail="456")

    # Simula la respuesta de session.query().filter_by().all() para devolver las compensaciones mock
    mock_session_query_all = MagicMock(return_value=[compensation_1, compensation_2])
    with patch('src.models.model.session.query', return_value=MagicMock(filter_by=MagicMock(return_value=MagicMock(all=mock_session_query_all)))):

        command = ExecuteCompensation(transaction_id=transaction_id, auth_header="Bearer token")
        command.execute()
        assert mock_requests_delete.call_count == 2  


@patch('src.models.model.session.commit')
@patch('src.models.model.session.delete')
@patch('requests.delete')
def test_compensation_execute_error_code_404(mock_requests_delete, mock_session_delete, mock_session_commit):
    # Configura mocks
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_delete.return_value = mock_response

    # Configura una lista de compensaciones mock
    transaction_id = str(uuid.uuid4())  # Genera un transactionId de ejemplo
    compensation_1 = Compensation(transactionId=transaction_id, action=DELETE, path="delete_path", detail="123")
    compensation_2 = Compensation(transactionId=transaction_id, action=DELETE, path="delete_path", detail="456")

    # Simula la respuesta de session.query().filter_by().all() para devolver las compensaciones mock
    mock_session_query_all = MagicMock(return_value=[compensation_1, compensation_2])
    with patch('src.models.model.session.query', return_value=MagicMock(filter_by=MagicMock(return_value=MagicMock(all=mock_session_query_all)))):

        command = ExecuteCompensation(transaction_id=transaction_id, auth_header="Bearer token")
        result = command.execute()
        assert result == 404 


@patch('src.models.model.session.commit')
@patch('src.models.model.session.delete')
@patch('requests.delete')
def test_compensation_execute_error_exception(mock_requests_delete, mock_session_delete, mock_session_commit):
    # Configura mocks
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_requests_delete.return_value = mock_response
    mock_requests_delete.side_effect = Exception("Test exception")

    # Configura una lista de compensaciones mock
    transaction_id = str(uuid.uuid4())  # Genera un transactionId de ejemplo
    compensation_1 = Compensation(transactionId=transaction_id, action=DELETE, path="delete_path", detail="123")
    compensation_2 = Compensation(transactionId=transaction_id, action=DELETE, path="delete_path", detail="456")

    # Simula la respuesta de session.query().filter_by().all() para devolver las compensaciones mock
    mock_session_query_all = MagicMock(return_value=[compensation_1, compensation_2])
    with patch('src.models.model.session.query', return_value=MagicMock(filter_by=MagicMock(return_value=MagicMock(all=mock_session_query_all)))):

        command = ExecuteCompensation(transaction_id=transaction_id, auth_header="Bearer token")
        result = command.execute()
        assert result == 500 
