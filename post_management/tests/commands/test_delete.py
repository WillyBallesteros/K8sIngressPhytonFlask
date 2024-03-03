import pytest
import uuid
from unittest.mock import MagicMock, create_autospec
from src.commands.delete import DeletePost
from src.commands.create import CreatePost
from src.models.post import Post
from src.models.model import session

class TestDeletePost:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_add = mocker.patch('src.models.model.session.add')
        self.mock_query = mocker.patch('src.models.model.session.query')
        self.mock_delete = mocker.patch('src.models.model.session.delete')
        self.mock_commit = mocker.patch('src.models.model.session.commit')

        self.mock_post = create_autospec(Post)
        self.mock_query.return_value.filter.return_value.first.return_value = self.mock_post

    def test_delete_post_found(self):
        mock_post = MagicMock()
        mock_session = MagicMock()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        userId = 'caa8b54a-eb5e-4134-8ae2-a3946a428ec7'
        routeId = 'caa9b54a-eb5e-4134-8ae2-a3946a428ec7'
        expireAt = '2023-12-31T23:59:59'

        create_post = CreatePost(userId=userId, routeId=routeId, expireAt=expireAt)

        create_post.session = mock_session

        mock_post.id = uuid.uuid4()
        create_post.execute = MagicMock(return_value=mock_post)

        result = create_post.execute()

        postId = result.id

        resultDelete = DeletePost(id=postId).execute()

        assert resultDelete == 200
        self.mock_query.return_value.filter.return_value.first.assert_called_once()
        self.mock_delete.assert_called_once_with(self.mock_post)
        self.mock_commit.assert_called_once()

    def test_delete_post_not_found(self):
        # Configurar el mock para simular que el post no se encuentra
        self.mock_query.return_value.filter.return_value.first.return_value = None

        postId = 'algún_id_de_post_inexistente'

        result = DeletePost(id=postId).execute()

        # Verificar el comportamiento cuando el post no se encuentra
        assert result == 404
        self.mock_query.return_value.filter.return_value.first.assert_called_once()
        # Asegurar que session.delete() y session.commit() no se llamen cuando el post no existe
        self.mock_delete.assert_not_called()
        self.mock_commit.assert_not_called()
