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
        # Intenta convertir el string a un objeto UUID
        uuid_obj = uuid.UUID(string_uuid)
        # Si la conversión es exitosa, devuelve True
        return True
    except ValueError:
        # Si ocurre un error de ValueError, significa que el string no es un UUID válido
        return False