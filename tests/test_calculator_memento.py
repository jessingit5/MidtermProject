import pytest
import pandas as pd
from app.calculator_memento import Memento, Caretaker
from app.history import HistoryManager

@pytest.fixture
def caretaker():
    history_manager = HistoryManager(max_history=5)
    return Caretaker(history_manager)

@pytest.fixture
def mementos():
    return [
        Memento([]),
        Memento([1]),
        Memento([1, 2])
    ]

def test_caretaker_save(caretaker):
    caretaker.save()
    caretaker._originator.add("dummy_calc")
    caretaker.save()
    assert len(caretaker._undo_mementos) == 2

def test_caretaker_undo(caretaker):
    caretaker.save()
    caretaker._originator.add("calc1")
    caretaker.save()
    caretaker.undo()
    assert len(caretaker._originator.get_history()) == 0

def test_caretaker_redo(caretaker):
    caretaker.save()
    caretaker._originator.add("calc1")
    caretaker.save()
    
    caretaker.undo()
    assert len(caretaker._originator.get_history()) == 0
    
    caretaker.redo()
    assert len(caretaker._originator.get_history()) == 1
    assert caretaker._originator.get_history()[0] == "calc1"

def test_undo_at_limit(caretaker):
    caretaker.save()
    with pytest.raises(IndexError, match="Cannot undo"):
        caretaker.undo()

def test_redo_at_limit(caretaker):
    with pytest.raises(IndexError, match="Cannot redo"):
        caretaker.redo()

def test_save_clears_redo_stack(caretaker):
    caretaker.save()
    caretaker._originator.add("calc1")
    caretaker.save()
    caretaker.undo()
    assert len(caretaker._redo_mementos) == 1
    
    caretaker._originator.add("calc2")
    caretaker.save()
    assert len(caretaker._redo_mementos) == 0
