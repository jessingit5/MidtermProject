import pytest
from app.input_validators import validate_operands
from app.exceptions import ValidationError

def test_validate_operands_valid():
    assert validate_operands(["5", "10.5"], 1000) == (5.0, 10.5)

@pytest.mark.parametrize("inputs, expected_error", [
    (["5"], "Exactly two numerical inputs are required."),
    (["5", "10", "15"], "Exactly two numerical inputs are required."),
    (["a", "10"], "Inputs must be valid numbers."),
    (["5", "b"], "Inputs must be valid numbers."),
    (["1001", "5"], "Inputs must be between -1000 and 1000."),
])
def test_validate_operands_invalid(inputs, expected_error):
    with pytest.raises(ValidationError, match=expected_error):
        validate_operands(inputs, 1000)
