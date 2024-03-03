from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .model import Model

class Post(Model):
    __tablename__ = 'posts'
    userId = Column(String, nullable=False)
    routeId = Column(String, nullable=False)
    expireAt = Column(DateTime, nullable=False)

    def __init__(self, userId, routeId, expireAt):
        Model.__init__(self)
        self.userId = userId
        self.routeId = routeId
        self.expireAt = expireAt
