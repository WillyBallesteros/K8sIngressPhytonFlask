import pytest
from datetime import datetime, timedelta
from src.utils.utils import *
from tests.utils.utils import INVALID_TOKEN, VALID_TOKEN

# Pruebas para la función is_email
@pytest.mark.parametrize("email, expected_result", [
    ("test@example.com", True),
    ("invalid_email", False),
    ("another@example", False),
    ("test@.com", False),
])
def test_is_email(email, expected_result):
    assert is_email(email) == expected_result

# Pruebas para la función is_boolean_and_value
@pytest.mark.parametrize("value, expected_result", [
    (True, True),
    (False, False),
    ("true", True),
    ("false", False),
])
def test_is_boolean_and_value(value, expected_result):
    assert is_boolean_and_value(value) == expected_result

# Pruebas para la función is_size_admited
@pytest.mark.parametrize("size, expected_result", [
    ("LARGE", True),
    ("MEDIUM", True),
    ("SMALL", True),
    ("EXTRA_LARGE", False),
    ("tiny", False),
])
def test_is_size_admited(size, expected_result):
    assert is_size_admited(size) == expected_result

# Pruebas para la función is_uuid_valid
@pytest.mark.parametrize("uuid_string, expected_result", [
    ("123e4567-e89b-12d3-a456-426614174000", True),
    ("123e4567-e89b-12d3-a456-4266141740", False),
    ("not_a_uuid", False),
])
def test_is_uuid_valid(uuid_string, expected_result):
    assert is_uuid_valid(uuid_string) == expected_result

# Pruebas para la función get_info_token
def test_get_info_token():
    assert get_info_token(VALID_TOKEN) 

def test_invalid_token():
    result = get_info_token(INVALID_TOKEN) 
    assert not result

# Pruebas para la función is_active_date

def test_is_active_date():
    str_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%f')
    assert is_active_date(str_date) == True

# Pruebas para la función is_positive
@pytest.mark.parametrize("str_number, expected_result", [
    ("123", True),
    ("-123", False),
    ("0", True),
    ("not_a_number", False),
])
def test_is_positive(str_number, expected_result):
    assert is_positive(str_number) == expected_result