from flask import jsonify
from ..models.model import session
from ..models.offer import Offer
from .base_command import BaseCommannd
import requests
from . import host_user

class QueryUser(BaseCommannd):
  def __init__(self, token):
    self.token = token
    
    
     
  def execute(self):
   
    users_url = f"{host_user}/users/me"
    headers = {"Authorization": self.token}
    try:
      response = requests.get(users_url, headers=headers)
      if response.status_code == 200:
        info_user = response.json()
        return info_user
      else:
        return "", 404
    except requests.exceptions.RequestException as e:
        return "", 400