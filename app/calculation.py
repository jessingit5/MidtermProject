from datetime import datetime
class Calculation:
    def __init__(self, operand_a: float, operand_b: float, operation_name: str, result: float):
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operation_name = operation_name
        self.result = result
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "operand_a": self.operand_a, "operand_b": self.operand_b,
            "operation_name": self.operation_name, "result": self.result,
            "timestamp": self.timestamp
        }

    def __repr__(self):
        return f"Calculation({self.operand_a}, {self.operand_b}, '{self.operation_name}', {self.result})"
    

    @staticmethod
    def from_dict(data: dict):
        calc = Calculation(
            float(data['operand_a']), float(data['operand_b']),
            data['operation_name'], float(data['result'])
        )
        calc.timestamp = data.get('timestamp', datetime.now().isoformat())
        return calc