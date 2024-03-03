from  sqlalchemy  import  Column, String
from .model  import  Model, Base

class User(Model):
    __tablename__ = 'users'

    username = Column(String)
    password = Column(String)
    email = Column(String)
    fullName = Column(String)
    dni = Column(String)
    phoneNumber = Column(String)
    status = Column(String)
    
    def  __init__(self, username, password, email, fullName, dni, phoneNumber, status):
        Model.__init__(self)
        self.username = username
        self.password = password
        self.email = email
        self.fullName = fullName
        self.dni = dni
        self.phoneNumber = phoneNumber
        self.status = status