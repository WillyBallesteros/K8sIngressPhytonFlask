import pytest
from src.utils.utils import *
from datetime import datetime, timedelta

# Prueba para is_uuid_valid
@pytest.mark.parametrize("string_uuid, expected", [
    ("123e4567-e89b-12d3-a456-426614174000", True),
    ("invalid-uuid", False),
])
def test_is_uuid_valid(string_uuid, expected):
    assert is_uuid_valid(string_uuid) == expected

# Prueba para is_future_date
def test_is_future_date():
    future_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
    past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()

    assert is_future_date(future_date) == True
    assert is_future_date(past_date) == False

# Prueba para parse_datetime
@pytest.mark.parametrize("expire_at_str, expected_result", [
    ("2023-01-23T12:05:08.395804Z", True),
    ("invalid-date-format", False),
])
def test_parse_datetime(expire_at_str, expected_result):
    result = parse_datetime(expire_at_str)
    assert (result is not None) == expected_result

def test_get_info_token():
    assert get_info_token("Bearer 123e4567-e89b-12d3-a456-426614174000")

def test_invalid_token():
    result = get_info_token("")
    assert not result

# Prueba para are_consecutive_dates
def test_are_consecutive_dates():
    now_str = (datetime.utcnow() + timedelta(days=1)).isoformat()
    tomorrow_str = (datetime.utcnow() + timedelta(days=2)).isoformat()
    assert are_consecutive_dates(now_str, tomorrow_str) == True
    assert are_consecutive_dates(tomorrow_str, now_str) == False


@pytest.mark.parametrize("value, expected_result", [
    (True, True),
    (False, False),
    ("true", True),
    ("false", False),
])
def test_is_boolean_and_value(value, expected_result):
    assert is_boolean_and_value(value) == expected_result
