from ..models.model import session
from ..models.compensation import Compensation
from .base_command import BaseCommannd

class DeleteCompensation(BaseCommannd):
    def __init__(self, transactionId):
        self.transactionId = transactionId

    def execute(self):
        compensations = session.query(Compensation).filter_by(transactionId=self.transactionId).all()
        for compensation in compensations:
            session.delete(compensation)
            session.commit()
        return True