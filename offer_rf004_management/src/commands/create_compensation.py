from ..models.model import session
from ..models.compensation import Compensation
from .base_command import BaseCommannd

class CreateCompensation(BaseCommannd):
    def __init__(self, transactionId, action, path, detail):
        self.transactionId = transactionId
        self.action = action
        self.path = path
        self.detail = detail

    def execute(self):
        compensation = Compensation(transactionId=self.transactionId, action=self.action, path=self.path, detail=self.detail)
        session.add(compensation)
        session.commit()
        return compensation