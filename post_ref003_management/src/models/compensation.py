from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .model import Model

class Compensation(Model):
    __tablename__ = 'compensations'
    transactionId = Column(String, nullable=False)
    action = Column(String, nullable=False)
    detail = Column(String, nullable=False)

    def __init__(self, transactionId, action, detail):
        Model.__init__(self)
        self.transactionId = transactionId
        self.action = action
        self.detail = detail
