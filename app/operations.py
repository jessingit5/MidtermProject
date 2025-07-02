import math

class Operation:

    def execute(self, a: float, b: float) -> float:
        raise NotImplementedError("Subclasses must implement the 'execute' method.")

class Addition(Operation):
    def execute(self, a: float, b: float) -> float: return a + b

class Subtraction(Operation):
    def execute(self, a: float, b: float) -> float: return a - b

class Multiplication(Operation):
    def execute(self, a: float, b: float) -> float: return a * b

class Division(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0: raise ValueError("Division by zero.")
        return a / b
    
class Power(Operation):
    def execute(self, a: float, b: float) -> float: return math.pow(a, b)

class Root(Operation):
    def execute(self, a: float, b: float) -> float:
        if a < 0 and b % 2 == 0: raise ValueError("Even root of a negative number.")
        return -math.pow(abs(a), 1/b) if a < 0 else math.pow(a, 1/b)
    
class Modulus(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0: raise ValueError("Modulus by zero.")
        return a % b
    
class IntegerDivision(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0: raise ValueError("Integer division by zero.")
        return float(a // b)
    
class Percentage(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0: raise ValueError("Cannot calculate percentage with respect to zero.")
        return (a / b) * 100
    
class AbsoluteDifference(Operation):
    def execute(self, a: float, b: float) -> float: return abs(a - b)

class OperationFactory:
    _operations = {
        "add": Addition, "subtract": Subtraction, "multiply": Multiplication,
        "divide": Division, "power": Power, "root": Root, "modulus": Modulus,
        "int_divide": IntegerDivision, "percent": Percentage, "abs_diff": AbsoluteDifference
    }

    @staticmethod
    def get_operations():
        return OperationFactory._operations.keys()
    
    @staticmethod
    def create(op_name: str) -> Operation:
        op_class = OperationFactory._operations.get(op_name.lower())
        if not op_class: raise ValueError(f"Unknown operation: '{op_name}'")
        return op_class()