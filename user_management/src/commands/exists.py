from ..models.model import session
from ..models.user import User
from .base_command import BaseCommannd

class ExistsUser(BaseCommannd):
  def __init__(self, id, username=None, email=None):
    self.id = id
    self.username = username
    self.email = email
  
  def execute(self):
    if self.id is not None:
      user = session.query(User).get(self.id)
      if user is not None:
          return True
      
    if self.username is not None:
      user = session.query(User).filter(User.username == self.username).first()
      if user is not None:
          return True
    
    if self.email is not None:
      user = session.query(User).filter(User.email == self.email).first()
      if user is not None:
          return True
    
    return False   