import pytest
from unittest.mock import patch, MagicMock
from src.commands.delete_compensation import DeleteCompensation
from src.models.model import session
from src.models.compensation import Compensation
import requests
import uuid

from src.utils.utils import DELETE

@pytest.fixture
def setup_compensations(db_session, compensations):
    pass

@patch('src.models.model.session.commit')
@patch('src.models.model.session.delete')
@patch('requests.delete')
def test_delete_compensation_found(mock_requests_delete, mock_session_delete, mock_session_commit):
    # Configura mocks
    mock_response = MagicMock()
    mock_response.status_code = 200  # Supongamos éxito para las llamadas HTTP
    mock_requests_delete.return_value = mock_response

    # Configura una lista de compensaciones mock
    transactionId = str(uuid.uuid4())  # Genera un transactionId de ejemplo
    compensation_1 = Compensation(transactionId=transactionId, action=DELETE, path="delete_path", detail="123")
    compensation_2 = Compensation(transactionId=transactionId, action=DELETE, path="delete_path", detail="456")

    # Simula la respuesta de session.query().filter_by().all() para devolver las compensaciones mock
    mock_session_query_all = MagicMock(return_value=[compensation_1, compensation_2])
    with patch('src.models.model.session.query', return_value=MagicMock(filter_by=MagicMock(return_value=MagicMock(all=mock_session_query_all)))):

        command = DeleteCompensation(transactionId=transactionId)
        result = command.execute()
        assert result == True

    