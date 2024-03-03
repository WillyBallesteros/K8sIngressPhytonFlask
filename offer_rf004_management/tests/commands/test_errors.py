from src.errors.errors import ApiError, CantDivideByZero

def test_api_error():
    # Create an instance of ApiError
    error = ApiError()
    
    # Assert that code and description match the defaults
    assert error.code == 422
    assert error.description == "Default message"

def test_cant_divide_by_zero():
    # Create an instance of CantDivideByZero
    error = CantDivideByZero()
    
    # Assert that code and description match the values for CantDivideByZero
    assert error.code == 400
    assert error.description == "Cant divide by zero"

def test_cant_divide_by_zero_inheritance():
    # Verify that CantDivideByZero inherits from ApiError
    assert issubclass(CantDivideByZero, ApiError)