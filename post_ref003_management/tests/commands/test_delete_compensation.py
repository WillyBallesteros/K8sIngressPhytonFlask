import pytest
import uuid
from unittest.mock import MagicMock, create_autospec, call
from src.commands.delete_compensation import DeleteCompensation
from src.models.compensation import Compensation
from src.models.model import session

class TestDeleteCompensation:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch('src.models.model.session.add')
        self.mock_query = mocker.patch('src.models.model.session.query')
        self.mock_delete = mocker.patch('src.models.model.session.delete')
        self.mock_commit = mocker.patch('src.models.model.session.commit')

    def test_delete_compensation_found(self):
        # Configuración del entorno de prueba
        transaction_id = str(uuid.uuid4())
        mock_compensation_1 = create_autospec(Compensation)
        mock_compensation_2 = create_autospec(Compensation)
        self.mock_query.return_value.filter_by.return_value.all.return_value = [mock_compensation_1, mock_compensation_2]

        # Ejecución del comando DeleteCompensation
        result = DeleteCompensation(transactionId=transaction_id).execute()

        # Verificaciones
        assert result is True
        self.mock_query.return_value.filter_by.assert_called_once_with(transactionId=transaction_id)
        self.mock_delete.assert_has_calls([call(mock_compensation_1), call(mock_compensation_2)])
        self.mock_commit.assert_called_once()

    def test_delete_compensation_not_found(self):
        # Configuración del entorno de prueba
        transaction_id = str(uuid.uuid4())
        self.mock_query.return_value.filter_by.return_value.all.return_value = []

        # Ejecución del comando DeleteCompensation
        result = DeleteCompensation(transactionId=transaction_id).execute()

        # Verificaciones
        assert result is False
        self.mock_query.return_value.filter_by.assert_called_once_with(transactionId=transaction_id)
        self.mock_delete.assert_not_called()
        self.mock_commit.assert_not_called()
