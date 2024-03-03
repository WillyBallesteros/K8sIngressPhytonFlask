from ..models.model import session
from ..models.post import Post
from .base_command import BaseCommannd

class CreatePost(BaseCommannd):
    def __init__(self, userId, routeId, expireAt):
        self.userId = userId
        self.routeId = routeId
        self.expireAt = expireAt

    def execute(self):
        post = Post(userId=self.userId, routeId=self.routeId, expireAt=self.expireAt)
        session.add(post)
        session.commit()
        return post