import re
import uuid
import json
import base64
from datetime import datetime


email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

size_admited = {"LARGE", "MEDIUM", "SMALL"}

def is_email(value):
    if re.match(email_pattern, value):
        return True
    else:
        return False
    
def is_boolean_and_value(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, int):
        raise ValueError("El texto ${value} no representa un valor booleano")
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError("El texto ${value} no representa un valor booleano")
    
def is_size_admited(size):
    if size in size_admited:
        return True
    else:
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
    
def get_info_token(token):
    
    if len(token) < 1 :
      return False
    elif is_uuid_valid(token[7:]):
      return True
    return False

def is_active_date(str_date):
    date_ = datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%f')
    date_now_ = datetime.now()
    if date_ > date_now_:
        return True
    else:
        return False
    
def is_positive(str_number):
    try:
        # Intenta convertir el string a un entero
        new_number = int(str_number)
        # Verifica si el valor es mayor que cero
        if new_number >= 0:
            return True
        else:
            return False
    except ValueError:
        # Si ocurre un error de ValueError, significa que el string no es un número válido
        return False