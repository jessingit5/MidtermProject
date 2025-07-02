from app.exceptions import ValidationError

def validate_operands(inputs: list[str], max_value: float):
    if len(inputs) != 2:
        raise ValidationError("Exactly two numerical inputs are required.")
    
    try:
        a = float(inputs[0])
        b = float(inputs[1])
    except ValueError:
        raise ValidationError("Inputs must be valid numbers.") from None
    
    if abs(a) > max_value or abs(b) > max_value:
        raise ValidationError(f"Inputs must be between -{max_value} and {max_value}.")
    
    return a, b
