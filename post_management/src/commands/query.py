from flask import jsonify
from ..models.model import session
from ..models.post import Post
from .base_command import BaseCommannd
from datetime import datetime

class QueryPost(BaseCommannd):
    def __init__(self, expire=None, route_id=None, owner=None, id=None):
        self.expire = expire
        self.route_id = route_id
        self.owner = owner
        self.id = id

    def execute(self):
        conditions = []
        if self.expire is not None:
            if self.expire:
                conditions.append(Post.expireAt <= datetime.utcnow())
            else:
                conditions.append(Post.expireAt > datetime.utcnow())
        if self.route_id:
            conditions.append(Post.routeId == self.route_id)
        if self.owner:
            conditions.append(Post.userId == self.owner)
        if self.id:
            conditions.append(Post.id == self.id)

        if conditions:
            posts = session.query(Post).filter(*conditions).all()
        else:
            posts = session.query(Post).all()

        resultados = [{
            'id': post.id,
            'routeId': post.routeId,
            'userId': post.userId,
            'expireAt': post.expireAt.isoformat(),
            'createdAt': post.createdAt.isoformat()
        } for post in posts]

        return jsonify(resultados)