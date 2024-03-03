import json
import base64
from ..models.model import session
from ..models.score import Score
from .base_command import BaseCommannd
from sqlalchemy import desc

class GetScoreByPost(BaseCommannd):
  def __init__(self, postId):
    self.postId = postId
  
  def execute(self):
    if self.postId is None:
        return None
    
    return session.query(Score).filter_by(postId=self.postId).order_by(desc(Score.utility)).all()
