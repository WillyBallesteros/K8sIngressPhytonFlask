from ..models.model import session
from ..models.score import Score
from .base_command import BaseCommannd

class CreateScore(BaseCommannd):
    def __init__(self, postId, offerId, utility):
        self.postId = postId
        self.offerId = offerId
        self.utility = utility
    
    def execute(self):
        score = Score(postId=self.postId, offerId=self.offerId, utility=self.utility)
        
        session.add(score)
        session.commit()

        return score