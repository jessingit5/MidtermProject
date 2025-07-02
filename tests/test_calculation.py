from app.calculation import Calculation
from datetime import datetime

def test_calculation_creation():
    before = datetime.now()
    calc = Calculation(10, 5, "add", 15)
    after = datetime.now()
    assert calc.operand_a == 10
    assert calc.result == 15
    assert datetime.fromisoformat(calc.timestamp)
    assert before <= datetime.fromisoformat(calc.timestamp) <= after

def test_calculation_to_dict():
    calc = Calculation(10, 5, "add", 15)
    calc_dict = calc.to_dict()
    assert calc_dict['operand_a'] == 10
    assert calc_dict['result'] == 15
    assert 'timestamp' in calc_dict

def test_calculation_from_dict():
    calc_data = {"operand_a": 20, "operand_b": 10, "operation_name": "subtract", "result": 10.0, "timestamp": "2023-01-01T12:00:00"}
    calc = Calculation.from_dict(calc_data)
    assert calc.operand_a == 20
    assert calc.result == 10.0
    assert calc.timestamp == "2023-01-01T12:00:00"

def test_calculation_repr():
    calc = Calculation(10, 2, "divide", 5)
    assert repr(calc) == "10.0 divide 2.0 = 5.0"
