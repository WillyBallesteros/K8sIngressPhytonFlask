import logging
from flask import jsonify
from ..models.model import session
from .base_command import BaseCommannd
import requests
from . import host_user

class QueryUser(BaseCommannd):
  def __init__(self, token):
    self.token = token

  def execute(self):

    users_url = f"{host_user}/users/me"
    logging.warning(f'users_url {users_url}')
    headers = {"Authorization": self.token}
    try:
      response = requests.get(users_url, headers=headers)
      logging.warning(f'----------------------------------')
      logging.warning(f'users_url {response}')
      logging.warning(f'----------------------------------')
      if response.status_code == 200:
        info_user = response.json()
        return info_user
      else:
        return "", 404
    except requests.exceptions.RequestException as e:
        return "", 400