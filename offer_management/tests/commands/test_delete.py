# import pytest
# from unittest.mock import MagicMock
# from src.commands.create import CreateOffer
# from src.commands.delete import DeleteOffer
# from src.models.model import session
# from src.models.offer import Offer
# from src.commands.reset import ResetOffer

       
# @pytest.fixture
# def mock_offer():
#     return MagicMock()

# @pytest.fixture
# def mock_session(mock_offer):
#     session_mock = MagicMock()
#     # Configura el mock para que retorne el objeto Offer cuando se llame a query().filter().first()
#     session_mock.query().filter().first.return_value = mock_offer
#     return session_mock


# def test_delete_offer_execute(mock_session):

#     create_offer = CreateOffer( postId='postId', userId='userId', description='description', size='size', fragile='fragile', offer='offer' )
#     create_offer.session = mock_session
#     result = create_offer.execute()
#     id = str(result.id)
#     # Crea una instancia de DeleteOffer con el ID del objeto a borrar
#     delete_offer = DeleteOffer(id=id)
#     delete_offer.session = mock_session

#     # Ejecuta el método execute de DeleteOffer
#     result = delete_offer.execute()

#     # Verifica que el método execute devuelva el resultado esperado
#     assert result == 200


# def test_delete_offer_execute_no_id(mock_session):

#     id = 'acc30af9-8712-4903-9999-3fff44b9623c'
#     # Crea una instancia de DeleteOffer con el ID del objeto a borrar
#     delete_offer = DeleteOffer(id=id)
#     delete_offer.session = mock_session

#     # Ejecuta el método execute de DeleteOffer
#     result = delete_offer.execute()

#     # Verifica que el método execute devuelva el resultado esperado
#     assert result == 404