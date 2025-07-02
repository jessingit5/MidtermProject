
from app.operations import OperationFactory
from app.calculation import Calculation
from app.history import HistoryManager
from app.calculator_memento import Memento, Caretaker
from app.calculator_config import CalculatorConfig
from app.input_validators import validate_operands

class Observer:

    def update(self, event: str, data: any):
        raise NotImplementedError("Subclasses must implement the 'update' method.")

class LoggingObserver(Observer):
    def update(self, event: str, data: any):
        if event == "calculation_done":
            print(f"[LOG] New calculation performed: {data!r}")

class AutosaveObserver(Observer):
    
    def __init__(self, history_manager: HistoryManager, file_path: str):
        self._history_manager = history_manager
        self._file_path = file_path

    def update(self, event: str, data: any):
        if event == "calculation_done":
            self._history_manager.save_to_csv(self._file_path)



class Calculator:
   
    def __init__(self, config: CalculatorConfig):
        self._config = config
        self._history_manager = HistoryManager()
        self._caretaker = Caretaker()
        self._observers: list[Observer] = []
        # Save the initial empty state for undo
        self._save_state()

    def attach(self, observer: Observer):
        
        self._observers.append(observer)

    def _notify(self, event: str, data: any):
       
        for observer in self._observers:
            observer.update(event, data)

    def _save_state(self):
        
        current_history_df = self._history_manager.get_history()
        self._caretaker.save_state(Memento(current_history_df))

    def execute(self, op_name: str, a: float, b: float):
        
        operation = OperationFactory.create_operation(op_name)
        result = operation.execute(a, b)
        calc_record = Calculation(a, b, op_name, result)
        self._history_manager.add_record(calc_record)
        self._save_state()
        self._notify("calculation_done", calc_record)
        print(f"Result: {result}")

    def undo(self):
        
        memento = self._caretaker.undo()
        self._history_manager.set_history(memento.get_state())
        print("Undo successful.")

    def redo(self):
        
        memento = self._caretaker.redo()
        self._history_manager.set_history(memento.get_state())
        print("Redo successful.")

    def show_history(self):
        
        history_df = self._history_manager.get_history()
        if history_df.empty:
            print("History is empty.")
        else:
            print("\n--- Calculation History ---")
            print(history_df.to_string())
            print("-------------------------\n")

    def clear_history(self):
        
        self._history_manager.clear()
        self._save_state() 
        print("History cleared.")

    def save_history(self):
       
        self._history_manager.save_to_csv(self._config.history_file_path)

    def load_history(self):
       
        self._history_manager.load_from_csv(self._config.history_file_path)
        self._save_state()


class REPL:
    
    def __init__(self):
        try:
            self.config = CalculatorConfig()
            self.calculator = Calculator(self.config)
            
            self.calculator.attach(LoggingObserver())
            self.calculator.attach(
                AutosaveObserver(self.calculator._history_manager, self.config.history_file_path)
            )
        except ValueError as e:
            print(f"Initialization Error: {e}")
            self.calculator = None

    def _display_help(self):
        """Displays the help message."""
        print("\nAvailable Commands:")
        print("  add <a> <b>         - Adds two numbers.")
        print("  subtract <a> <b>    - Subtracts two numbers.")
        print("  multiply <a> <b>    - Multiplies two numbers.")
        print("  divide <a> <b>      - Divides two numbers.")
        print("  power <a> <b>       - Raises a to the power of b.")
        print("  root <a> <b>        - Calculates the b-th root of a.")
        print("  history             - Show calculation history.")
        print("  undo                - Undo the last calculation.")
        print("  redo                - Redo the last undone calculation.")
        print("  clear               - Clear the entire history.")
        print("  save                - Manually save history to CSV.")
        print("  load                - Manually load history from CSV.")
        print("  help                - Show this help message.")
        print("  exit                - Exit the application.\n")

    def run(self):
        
        if not self.calculator:
            return

        print("Welcome to the Advanced Command-Line Calculator!")
        self.calculator.load_history()
        self._display_help()
        
        while True:
            try:
                user_input = input(">>> ").strip().lower()
                if not user_input:
                    continue

                parts = user_input.split()
                command = parts[0]
                args = parts[1:]

                if command in OperationFactory._operations:
                    operands = validate_operands(args)
                    self.calculator.execute(command, *operands)
                elif command == "history":
                    self.calculator.show_history()
                elif command == "undo":
                    self.calculator.undo()
                elif command == "redo":
                    self.calculator.redo()
                elif command == "clear":
                    self.calculator.clear_history()
                elif command == "save":
                    self.calculator.save_history()
                elif command == "load":
                    self.calculator.load_history()
                elif command == "help":
                    self._display_help()
                elif command == "exit":
                    print("Exiting Calculator. Goodbye!")
                    break
                else:
                    print(f"Unknown command: '{command}'")
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
