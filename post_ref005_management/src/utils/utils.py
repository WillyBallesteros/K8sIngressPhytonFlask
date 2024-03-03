import re
import uuid
import json
import base64
from datetime import datetime
def get_info_token(token):
    
    if len(token) < 1 :
      return False
    elif is_uuid_valid(token[7:]):
      return True
    return False

def is_uuid_valid(string_uuid):
    try:
        uuid_obj = uuid.UUID(string_uuid)
        return True
    except ValueError:
        return False