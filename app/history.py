import pandas as pd
from app.calculation import Calculation

class HistoryManager:
    def __init__(self, max_history: int):
        self._max_history = max_history
        self._history: list[Calculation] = []

    def add(self, calculation: Calculation):
        self._history.append(calculation)
        if len(self._history) > self._max_history:
            self._history.pop(0)

    def get_history(self) -> list[Calculation]:
        return self._history.copy()

    def set_history(self, history: list[Calculation]):
        self._history = history.copy()

    def clear(self):
        self._history.clear()

    def save(self, file_path: str, encoding: str):
        if not self._history:
            df = pd.DataFrame(columns=["operand_a", "operand_b", "operation_name", "result", "timestamp"])
        else:
            df = pd.DataFrame([calc.to_dict() for calc in self._history])
        try:
            df.to_csv(file_path, index=False, encoding=encoding)
        except IOError as e:
            print(f"Error saving history: {e}")

    def load(self, file_path: str, encoding: str):
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            df['operand_a'] = pd.to_numeric(df['operand_a'])
            df['operand_b'] = pd.to_numeric(df['operand_b'])
            df['result'] = pd.to_numeric(df['result'])
            self._history = [Calculation.from_dict(row) for _, row in df.iterrows()]
        except FileNotFoundError:
            self._history = []
        except Exception as e:
            print(f"Error loading history: {e}")
            self._history = []