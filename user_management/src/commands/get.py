from ..utils.utils import is_valid_uuid
from ..models.model import session
from ..models.user import User
from ..models.token import Token
from .base_command import BaseCommannd

class GetUser(BaseCommannd):
  def __init__(self, token):
    self.token = token
  
  def execute(self):
    if not is_valid_uuid(self.token):
        return None
    
    tokendb = session.query(Token).get(self.token)
    
    if tokendb is None:
      return None
    
    return session.query(User).get(tokendb.userid)