import logging
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_memento import Caretaker
from app.calculator_config import CalculatorConfig
from app.input_validators import validate_operands
from app.exceptions import CalculatorError
from app.logger import setup_logger


class Observer:
    def update(self, event: str, data: any): raise NotImplementedError

class LoggingObserver(Observer):
    def __init__(self, logger: logging.Logger): self.logger = logger
    def update(self, event: str, data: any):
        if event == "calculation": self.logger.info(f"Calculation: {data.to_dict()}")

class AutoSaveObserver(Observer):
    def __init__(self, history: HistoryManager, config: CalculatorConfig):
        self.history, self.config = history, config
    def update(self, event: str, data: any):
        if event == "calculation" and self.config.auto_save:
            self.history.save(self.config.history_filepath, self.config.encoding)

class CalculatorApp:
    def __init__(self):
        self.config = CalculatorConfig()
        self.logger = setup_logger(self.config.log_dir)
        self.history = HistoryManager(self.config.max_history)
        self.caretaker = Caretaker(self.history)
        self.observers: list[Observer] = []
        self._register_observers()
        self.load_history()

    def _register_observers(self):
        self.attach(LoggingObserver(self.logger))
        self.attach(AutoSaveObserver(self.history, self.config))

    def attach(self, observer: Observer): self.observers.append(observer)
    def _notify(self, event: str, data: any):
        for observer in self.observers: observer.update(event, data)

    def execute_calculation(self, op_name: str, a: float, b: float):
        operation = OperationFactory.create(op_name)
        result = round(operation.execute(a, b), self.config.precision)
        calc = Calculation(a, b, op_name, result)
        self.history.add(calc)
        self.caretaker.save()
        self._notify("calculation", calc)
        return result

    def undo(self): self.caretaker.undo(); print("Undo successful.")
    def redo(self): self.caretaker.redo(); print("Redo successful.")
    def show_history(self):
        history_list = self.history.get_history()
        if not history_list: print("History is empty.")
        else:
            print("\n--- Calculation History ---")
            for calc in history_list:
                print(f"{calc.timestamp}: {calc}")
            print("--------------------------")
    
    def clear_history(self): self.history.clear(); self.caretaker.save(); print("History cleared.")
    def save_history(self): self.history.save(self.config.history_filepath, self.config.encoding); print("History saved.")
    def load_history(self): self.history.load(self.config.history_filepath, self.config.encoding); self.caretaker.save(); print("History loaded.")


class REPL:
    def __init__(self):
        try:
            self.app = CalculatorApp()
            self.commands = {
                "history": self.display_history, "clear": self.clear_history,
                "undo": self.undo, "redo": self.redo, "save": self.save,
                "load": self.load, "help": self.display_help, "exit": self.exit
            }
        except CalculatorError as e:
            print(f"Initialization Error: {e}"); self.app = None
    
    def run(self):
        if not self.app: return
        print("Welcome to the Advanced Calculator!")
        self.display_help()
        while True:
            try:
                user_input = input(">>> ").strip().lower()
                if not user_input: continue
                parts = user_input.split()
                cmd_name, args = parts[0], parts[1:]
                self.execute_command(cmd_name, args)
            except KeyboardInterrupt: print("\nExiting..."); break
            except Exception as e:
                self.app.logger.error(f"An unexpected REPL error: {e}", exc_info=True)
                print("An unexpected error occurred. Please check logs.")
                break

    def execute_command(self, cmd_name: str, args: list):
        try:
            if cmd_name in OperationFactory.get_operations():
                a, b = validate_operands(args, self.app.config.max_input)
                result = self.app.execute_calculation(cmd_name, a, b)
                print(f"Result: {result}")
            elif cmd_name in self.commands:
                self.commands[cmd_name]()
            else:
                print(f"Unknown command: '{cmd_name}'")
        except (CalculatorError, IndexError) as e:
            print(f"Error: {e}")

    def display_history(self): self.app.show_history()
    def clear_history(self): self.app.clear_history()
    def undo(self): self.app.undo()
    def redo(self): self.app.redo()
    def save(self): self.app.save_history()
    def load(self): self.app.load_history()
    def exit(self): raise KeyboardInterrupt

    def display_help(self):
        print("\nAvailable Commands:")
        for op in OperationFactory.get_operations():
            print(f"  {op:<12} <a> <b>")
        # Description map for help text
        descriptions = {
            "history": "Display calculation history.", "clear": "Clear calculation history.",
            "undo": "Undo the last calculation.", "redo": "Redo the last undone calculation.",
            "save": "Manually save history.", "load": "Manually load history.",
            "help": "Display this help menu.", "exit": "Exit the application gracefully."
        }
        for name, func in self.commands.items():
            print(f"  {name:<12} - {descriptions.get(name, '')}")

def start_app():
    REPL().run()

if __name__ == '__main__': 
    start_app()
