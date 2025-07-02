import pytest
from app.operations import OperationFactory, Root, Operation
from app.exceptions import OperationError

def test_base_operation_not_implemented():
    op = Operation()
    with pytest.raises(NotImplementedError):
        op.execute(1, 2) 


@pytest.mark.parametrize("op_name, a, b, expected", [
    ("add", 10, 5, 15), ("subtract", 20, 5, 15), ("multiply", 6, 7, 42),
    ("divide", 100, 10, 10), ("power", 2, 10, 1024), ("root", 64, 2, 8),
    ("modulus", 10, 3, 1), ("int_divide", 10, 3, 3), ("percent", 10, 50, 20),
    ("abs_diff", 10, 15, 5), ("root", -27, 3, -3)
])
def test_all_operations(op_name, a, b, expected):
    op = OperationFactory.create(op_name)
    assert op.execute(a, b) == expected

def test_get_operations():
    ops = OperationFactory.get_operations()
    assert "add" in ops
    assert "abs_diff" in ops

@pytest.mark.parametrize("op_name, a, b, error_msg", [
    ("divide", 10, 0, "Division by zero"),
    ("modulus", 10, 0, "Modulus by zero"),
    ("int_divide", 10, 0, "Integer division by zero"),
    ("percent", 10, 0, "Cannot calculate percentage with respect to zero"),
    ("root", -4, 2, "Even root of a negative number")
])
def test_operation_errors(op_name, a, b, error_msg):
    op = OperationFactory.create(op_name)
    with pytest.raises(OperationError, match=error_msg):
        op.execute(a, b)

def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation: 'log'"):
        OperationFactory.create("log")
