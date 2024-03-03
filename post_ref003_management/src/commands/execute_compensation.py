from ..models.model import session
from ..models.compensation import Compensation
from .base_command import BaseCommannd
import requests
import logging

class CompensateSagaOperations(BaseCommannd):
    def __init__(self, transaction_id, auth_header, post_url, route_url):
        self.transaction_id = transaction_id
        self.auth_header = auth_header
        self.post_url = post_url
        self.route_url = route_url

    def execute(self):
        try:
            compensations = session.query(Compensation).filter_by(transactionId=self.transaction_id).all()
            for compensation in reversed(compensations):
                try:
                    if compensation.action == "delete_post":
                        response = requests.delete(f"http://{self.post_url}/posts/{compensation.detail}", headers={"Authorization": self.auth_header})
                    elif compensation.action == "delete_route":
                        response = requests.delete(f"http://{self.route_url}/routes/{compensation.detail}", headers={"Authorization": self.auth_header})

                    if response.status_code not in [200, 204]:
                        logging.error(f"Failed to compensate {compensation.action} with detail {compensation.detail}, status code: {response.status_code}")
                    else:
                        session.delete(compensation)
                except requests.RequestException as e:
                    logging.error(f"Request exception during compensation of {compensation.action}: {str(e)}")
            session.commit()
        except Exception as e:
            logging.error(f"Error during compensation operations: {str(e)}")
            session.rollback()
            raise