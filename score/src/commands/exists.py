import json
import base64
from ..models.model import session
from ..models.score import Score
from .base_command import BaseCommannd
from sqlalchemy import and_

class ExistsScore(BaseCommannd):
  def __init__(self, postId, offerId):
    self.postId = postId
    self.offerId = offerId
  
  def execute(self):
    if self.postId is None or self.offerId is None:
        return None
    
    return session.query(Score).filter(and_(Score.postId == self.postId, Score.offerId == self.offerId)).all()
