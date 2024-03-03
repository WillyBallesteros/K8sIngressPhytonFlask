from ..models.model import session
from ..models.route import Route
from .base_command import BaseCommannd

class ResetRoute(BaseCommannd):
  def execute(self):
    num_deleted = session.query(Route).delete()
    session.commit()

    return num_deleted