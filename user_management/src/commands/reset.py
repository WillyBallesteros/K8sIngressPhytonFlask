from ..models.model import session
from ..models.user import User
from ..models.token import Token
from .base_command import BaseCommannd

class ResetDB(BaseCommannd):
  def execute(self):
    num_deleted_user = session.query(User).delete()
    num_deleted_token = session.query(Token).delete()
    session.commit()

    return num_deleted_user + num_deleted_token