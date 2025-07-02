from app.history import HistoryManager

class Memento:
    def __init__(self, state: list):
        self._state = state.copy()
    def get_state(self) -> list:
        return self._state

class Caretaker:
    def __init__(self, originator: HistoryManager):
        self._originator = originator
        self._undo_mementos: list[Memento] = []
        self._redo_mementos: list[Memento] = []

    def save(self):
        memento = Memento(self._originator.get_history())
        self._undo_mementos.append(memento)
        self._redo_mementos.clear()

    def undo(self):
        if len(self._undo_mementos) <= 1:
            raise IndexError("Cannot undo: No previous state.")
        current_memento = self._undo_mementos.pop()
        self._redo_mementos.append(current_memento)
        self._originator.set_history(self._undo_mementos[-1].get_state())

    def redo(self):
        if not self._redo_mementos:
            raise IndexError("Cannot redo: No future state.")
        memento_to_restore = self._redo_mementos.pop()
        self._undo_mementos.append(memento_to_restore)
        self._originator.set_history(memento_to_restore.get_state())