from datetime import datetime, timedelta
import pytest
from src.utils.utils import is_future_date, parse_datetime

# Define test cases for is_future_date function

def test_is_future_date_future():
    current_date = datetime.now()
    one_day_delta = timedelta(days=1)
    new_date = current_date + one_day_delta
    future_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    assert is_future_date(future_date_str) is True

def test_is_future_date_past():
    current_date = datetime.now()
    one_day_delta = timedelta(days=-1)
    new_date = current_date + one_day_delta
    past_date_str = new_date.strftime("%Y-%m-%dT%H:%M:%S")
    assert is_future_date(past_date_str) is False

def test_is_future_date_invalid_format():
    invalid_date_str = 'invalid_date_format'
    assert is_future_date(invalid_date_str) is False

# Define test cases for parse_datetime function

def test_parse_datetime_with_z():
    date_str = '2025-01-01T00:00:00.000Z'
    expected_date = datetime(2025, 1, 1, 0, 0, 0)
    assert parse_datetime(date_str) == expected_date

def test_parse_datetime_without_z():
    date_str = '2025-01-01T00:00:00.000'
    expected_date = datetime(2025, 1, 1, 0, 0, 0)
    assert parse_datetime(date_str) == expected_date

def test_parse_datetime_invalid_format():
    invalid_date_str = 'invalid_date_format'
    assert parse_datetime(invalid_date_str) is None