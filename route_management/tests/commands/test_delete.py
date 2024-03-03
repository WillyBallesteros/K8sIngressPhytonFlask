# import pytest
# from unittest.mock import MagicMock
# from src.models.route import Route
# from src.commands.delete import DeleteRoute

# @pytest.fixture
# def mock_session():
#     session_mock = MagicMock()
#     # Configura el mock para simular la sesión de SQLAlchemy
#     # La sesión debe simular la cadena de llamadas completa usada en DeleteRoute.execute()
#     session_mock.query.return_value.filter.return_value.first.return_value = None
#     session_mock.delete = MagicMock()
#     session_mock.commit = MagicMock()
#     return session_mock

# def test_delete_route_execute_no_id(mock_session):
#     # Suponemos que no hay ninguna ruta con el ID proporcionado
#     # El ID usado aquí no corresponde a ninguna ruta existente
#     non_existent_id = '6061eaa5'
#     delete_route = DeleteRoute(id=non_existent_id)
#     delete_route.session = mock_session  # Inyectar la sesión mockeada

#     # Ejecutar el método execute de DeleteRoute
#     result = delete_route.execute()

#     # Verificar que el método execute devuelva 404, ya que la ruta no existe
#     assert result == 404
#     # Verificar que el método delete no fue llamado, porque no se encontró la ruta
#     mock_session.delete.assert_not_called()
#     # Verificar que el método commit tampoco fue llamado
#     mock_session.commit.assert_not_called()

# def test_delete_route_execute_with_id(mock_session):
#     # Configurar el mock para simular una ruta existente
#     route = MagicMock(spec=Route)
#     route.id = '6061eaa5-ba80-422c-be4c-19c6c5e99128'
#     mock_session.query.return_value.filter.return_value.first.return_value = route

#     delete_route = DeleteRoute(id=route.id)
#     delete_route.session = mock_session  # Inyectar la sesión mockeada

#     # Ejecutar el método execute de DeleteRoute
#     result = delete_route.execute()

#     # Verificar que el método execute devuelva 200, indicando éxito en la eliminación
#     assert result == 200
#     # Verificar que el método delete fue llamado con la ruta correcta
#     mock_session.delete.assert_called_with(route)
#     # Verificar que se llamó al método commit
#     mock_session.commit.assert_called_once()