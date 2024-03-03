from flask import jsonify
from ..models.model import session
from ..models.post import Post
from .base_command import BaseCommannd  # Asegúrate de que el nombre es correcto, parece haber un error tipográfico en BaseCommannd

class DeletePost(BaseCommannd):
    def __init__(self, id):
        self.id = id

    def execute(self):
        post = session.query(Post).filter(Post.id == self.id).first()
        if not post:
            return 404

        session.delete(post)
        session.commit()

        return 200
