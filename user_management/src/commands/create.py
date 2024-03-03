from ..models.model import session
from ..models.user import User
from .base_command import BaseCommannd

class CreateUser(BaseCommannd):
    def __init__(self, username, password, email, fullName, dni, phoneNumber):
        self.username = username
        self.password = password
        self.email = email
        self.fullName = fullName
        self.dni = dni
        self.phoneNumber = phoneNumber
    
    def execute(self):
        user = User(username=self.username, password=self.password, email=self.email, 
                    fullName=self.fullName, dni=self.dni, phoneNumber=self.phoneNumber, status="POR_VERIFICAR")
        
        session.add(user)
        session.commit()

        return user