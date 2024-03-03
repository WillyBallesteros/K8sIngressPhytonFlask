from  sqlalchemy  import  Column, String, Float
from .model  import  Model, Base

class Score(Model):
    __tablename__ = 'score'

    postId = Column(String, nullable=False)
    offerId = Column(String, nullable=False)
    utility = Column(Float, nullable=False)
    
    def  __init__(self, postId, offerId, utility):
        Model.__init__(self)
        self.postId = postId
        self.offerId = offerId
        self.utility = utility