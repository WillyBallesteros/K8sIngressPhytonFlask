from ..models.model import session
from ..models.score import Score
from .base_command import BaseCommannd

class UpdateScore(BaseCommannd):
    def __init__(self, id, utility):
        self.id = id
        self.utility = utility
    
    def execute(self):
        score = session.query(Score).get(self.id)
        if score:
            score.utility = self.utility
            session.commit()