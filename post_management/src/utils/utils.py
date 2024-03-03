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

def is_future_date(date_str):
    now = datetime.utcnow()
    try:
        date = datetime.fromisoformat(date_str)
        return date > now
    except ValueError:
        return False

def parse_datetime(expire_at_str):
    try:
        # Try parsing with 'Z'
        return datetime.strptime(expire_at_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        try:
            # Try parsing without 'Z'
            return datetime.strptime(expire_at_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            # Handle other parsing errors (e.g., completely wrong format)
            return None

def are_consecutive_dates(start_date_str, end_date_str):
    try:
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        now = datetime.utcnow()
        return now < start_date < end_date
    except ValueError:
        return False

def get_valid_id_route(routes, payload):
    # Convertir las fechas del payload a objetos datetime para comparación
    payload_start_date = datetime.fromisoformat(payload["plannedStartDate"])
    payload_end_date = datetime.fromisoformat(payload["plannedEndDate"])

    for route in routes:
        # Verificar coincidencia del flightId
        if route["flightId"] != payload["flightId"]:
            continue

        # Verificar coincidencia de fechas
        route_start_date = datetime.fromisoformat(route["plannedStartDate"])
        route_end_date = datetime.fromisoformat(route["plannedEndDate"])
        if route_start_date != payload_start_date or route_end_date != payload_end_date:
            continue

        # Verificar coincidencia de aeropuertos y países
        if (route["sourceAirportCode"] != payload["origin"]["airportCode"] or
            route["sourceCountry"] != payload["origin"]["country"] or
            route["destinyAirportCode"] != payload["destiny"]["airportCode"] or
            route["destinyCountry"] != payload["destiny"]["country"]):
            continue

        # Si todas las verificaciones pasan, retornar el id del route válido
        return route["id"]

    # Si no se encuentra un route válido, retornar None
    return None

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