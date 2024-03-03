from ..models.model import session
from ..models.user import User
from .base_command import BaseCommannd

class UpdateUser(BaseCommannd):
  def __init__(self, id, fullName, dni, phoneNumber, status):
    self.id = id
    self.fullName = fullName
    self.dni = dni
    self.phoneNumber = phoneNumber
    self.status = status
  
  def execute(self):
    user = session.query(User).get(self.id)
    if self.fullName:
        user.fullName = self.fullName
    if self.dni:
        user.dni = self.dni
    if self.phoneNumber:
        user.phoneNumber = self.phoneNumber
    if self.status:
        user.status = self.status
    
    session.commit()