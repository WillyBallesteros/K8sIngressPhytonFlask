import pytest
from datetime import datetime, timedelta
from src.utils.utils import *
from tests.utils.utils import INVALID_TOKEN, VALID_TOKEN

# Pruebas para la función get_info_token
def test_get_info_token():
    assert get_info_token(VALID_TOKEN) 

def test_invalid_token():
    result = get_info_token(INVALID_TOKEN) 
    assert not result