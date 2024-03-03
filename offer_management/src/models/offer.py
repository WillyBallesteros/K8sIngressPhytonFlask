from marshmallow import Schema, fields
from  sqlalchemy  import  Column, String
from .model  import  Model, Base

class Offer(Model):
    __tablename__ = 'offers'

    postId = Column(String)
    userId = Column(String)
    description = Column(String)
    size = Column(String)
    fragile = Column(String)
    offer = Column(String)
    def  __init__(self, postId, userId, description, size, fragile, offer ):
        Model.__init__(self )
        self.postId = postId
        self.userId = userId
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer

class  OfferJsonSchema(Schema):
    id  = fields.Str()
    postId  = fields.Str()
    userId  = fields.Str()
    size  = fields.Str()
    fragile  = fields.Str()
    offer  = fields.Str()
    createdAt  = fields.DateTime()
    updatedAt  = fields.DateTime()