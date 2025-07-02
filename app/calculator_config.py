import os

class CalculatorConfig:

    def __init__(self):
        self.log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
        self.history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'data')
        self.max_history = self._get_env_as_int('CALCULATOR_MAX_HISTORY_SIZE', 100)
        self.auto_save = self._get_env_as_bool('CALCULATOR_AUTO_SAVE', "true")
        self.precision = self._get_env_as_int('CALCULATOR_PRECISION', 4)
        self.max_input = self._get_env_as_float('CALCULATOR_MAX_INPUT_VALUE', 1e9)
        self.encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')


        self.history_filepath = os.path.join(self.history_dir, "calculation_history.csv")
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)

    def _get_env_as_int(self, name, default):
        try: return int(os.getenv(name, default))
        except (ValueError, TypeError): raise ValueError(f"Invalid value for {name}. Must be an integer.")

    def _get_env_as_float(self, name, default):
        try: return float(os.getenv(name, default))
        except (ValueError, TypeError): raise ValueError(f"Invalid value for {name}. Must be a float.")

    def _get_env_as_bool(self, name, default):
        val = str(os.getenv(name, default)).lower()
        if val in ('true', '1', 't', 'y', 'yes'): return True
        if val in ('false', '0', 'f', 'n', 'no'): return False
        raise ValueError(f"Invalid boolean value for {name}: {val}")