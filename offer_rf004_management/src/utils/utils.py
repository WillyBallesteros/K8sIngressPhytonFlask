from datetime import datetime

DELETE='delete'

def is_future_date(date_str):
    now = datetime.utcnow()
    date = parse_datetime(date_str)
    if date is None:
        return False
    return date > now


def parse_datetime(date_at_str):
    try:
        # Try parsing with 'Z'
        return datetime.strptime(date_at_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        try:
            # Try parsing without 'Z'
            return datetime.strptime(date_at_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
            # Try parsing without 'Z'
                return datetime.strptime(date_at_str, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                # Handle other parsing errors (e.g., completely wrong format)
                return None