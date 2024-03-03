import json
import base64
from ..models.model import session
from ..models.user import User
from ..models.token import Token
from .base_command import BaseCommannd
from datetime import datetime, timedelta

class CreateToken(BaseCommannd):
  def __init__(self, username, password):
    self.username = username
    self.password = password
  
  def execute(self):
    user = session.query(User).filter(User.username == self.username).first()
    if user is None:
        return None
    
    if user.password != self.password:
       return None
    
    id = str(user.id)
    tomorrow = datetime.now() + timedelta(days=1)
    expire_at = tomorrow.isoformat()

    token = Token(userid=id, expire_at=expire_at)
        
    session.add(token)
    session.commit()

    return {
        "id": id,
        "token": str(token.id),
        "expireAt": expire_at
    }