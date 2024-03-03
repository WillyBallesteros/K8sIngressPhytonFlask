from ..models.model import session
from ..models.post import Post
from .base_command import BaseCommannd

class ResetPost(BaseCommannd):
  def execute(self):
    num_deleted = session.query(Post).delete()
    session.commit()

    return num_deleted