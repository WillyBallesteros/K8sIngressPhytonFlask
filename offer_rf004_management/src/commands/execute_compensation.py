from ..utils.utils import DELETE
from ..models.model import session
from ..models.compensation import Compensation
from .base_command import BaseCommannd
import requests
import logging

class ExecuteCompensation(BaseCommannd):
    def __init__(self, transaction_id, auth_header):
        self.transaction_id = transaction_id
        self.auth_header = auth_header

    def execute(self):
        
        compensations = session.query(Compensation).filter_by(transactionId=self.transaction_id).all()
        for compensation in reversed(compensations):
            
            try:
                response=None
                if compensation.action == DELETE:
                    response = requests.delete(f"{compensation.path}/{compensation.detail}", headers={"Authorization": self.auth_header})
                    
            except Exception as e:
                logging.error(f"Failed to execute compensation txn[{self.transaction_id}] action {compensation.action} path {compensation.path} with detail {compensation.detail} error 500")
                return 500
            if response.status_code not in [200, 204]:
                logging.error(f"Failed to execute compensation txn[{self.transaction_id}] action {compensation.action} path {compensation.path} with detail {compensation.detail}, status code: {response.status_code}")
                return response.status_code
            else:
                session.delete(compensation)
            
        session.commit()
        