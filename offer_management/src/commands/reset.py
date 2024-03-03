from ..models.model import session
from ..models.offer import Offer
from .base_command import BaseCommannd

class ResetOffer(BaseCommannd):
  def execute(self):
    num_deleted = session.query(Offer).delete()
    session.commit()

    return num_deleted