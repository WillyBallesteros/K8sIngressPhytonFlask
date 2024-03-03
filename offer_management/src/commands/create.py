from ..models.model import session
from ..models.offer import Offer
from .base_command import BaseCommannd

class CreateOffer(BaseCommannd):
  def __init__(self, postId, userId, description, size, fragile, offer):
    self.postId = postId
    self.userId = userId
    self.description = description
    self.size = size
    self.fragile = fragile
    self.offer = offer
  
  def execute(self):
    print(f"postId={self.postId}userId={self.userId}description={self.description}size={self.size}fragile={self.fragile}offer={self.offer}")
    
    offer = Offer(self.postId, self.userId, self.description, self.size, self.fragile, self.offer)
    
    session.add(offer)
    session.commit()

    return offer