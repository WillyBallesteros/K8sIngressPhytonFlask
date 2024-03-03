from  sqlalchemy  import  Column, String, DateTime
from .model  import  Model, Base

class Token(Model):
    __tablename__ = 'token'

    userid = Column(String)
    expire_at = Column(DateTime)
    
    def  __init__(self, userid, expire_at):
        Model.__init__(self)
        self.userid = userid
        self.expire_at = expire_at