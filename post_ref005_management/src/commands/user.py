from flask import jsonify
from .base_command import BaseCommannd
import requests

class Query(BaseCommannd):
  def __init__(self, auth_header, request_url, path, data=None):
    self.auth_header = auth_header
    self.request_url = request_url
    self.path = path
    self.data = data
     
  def execute(self):

    headers = {"Authorization": self.auth_header}
    url = self.request_url + self.path
    
    if self.data:
      url=url+f'/{self.data}'
      
    response = requests.get(url, headers=headers)
    
    return response