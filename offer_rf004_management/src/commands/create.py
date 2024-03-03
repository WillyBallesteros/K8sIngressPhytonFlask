import logging
from flask import jsonify

from ..utils.utils import DELETE
from ..commands.execute_compensation import ExecuteCompensation
from ..commands.create_compensation import CreateCompensation
from .base_command import BaseCommannd
import requests
import json

class Create(BaseCommannd):
  def __init__(self, auth_header, transactionId, request_url, path, payload ):
    self.auth_header = auth_header
    self.transactionId = transactionId
    self.request_url = request_url
    self.path = path
    self.payload = payload
     
  def execute(self):

    headers = {"Authorization": self.auth_header}
    urlOffers = self.request_url + self.path
    try:
      response = requests.post(urlOffers, json=self.payload, headers=headers)
    except Exception as e:
      logging.error(f"Error during compensation operations: {str(e)}")
      ExecuteCompensation(self.transactionId, self.auth_header ).execute() 
      return 500
    if response.status_code != 201:
        ExecuteCompensation(self.transactionId, self.auth_header ).execute() 
        return response.status_code
    response_content = json.loads(response.text)
    CreateCompensation(transactionId=self.transactionId, action=DELETE, path=urlOffers,  detail=response_content['id']).execute() 
    
    return response