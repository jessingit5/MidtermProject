from app.history import HistoryManager
from app.calculation import Calculation

def test_history_add_and_trim():
    history = HistoryManager(max_history=2)
    history.add(Calculation(1, 1, 'add', 2))
    history.add(Calculation(2, 2, 'add', 4))
    assert len(history.get_history()) == 2
    
    history.add(Calculation(3, 3, 'add', 6)) 
    assert len(history.get_history()) == 2
    assert history.get_history()[0].operand_a == 2 

def test_history_clear():
    history = HistoryManager(max_history=5)
    history.add(Calculation(1, 1, 'add', 2))
    history.clear()
    assert len(history.get_history()) == 0

def test_history_save_and_load(tmp_path):
    history1 = HistoryManager(5)
    history1.add(Calculation(10, 5, 'add', 15))
    
    file_path = tmp_path / "history.csv"
    history1.save(file_path, 'utf-8')
    
    history2 = HistoryManager(5)
    history2.load(file_path, 'utf-8')
    
    assert len(history2.get_history()) == 1
    assert history2.get_history()[0].result == 15

def test_save_empty_history(tmp_path):
    history = HistoryManager(5)
    file_path = tmp_path / "history.csv"
    history.save(file_path, 'utf-8')
    assert file_path.is_file()
    assert file_path.read_text().strip() == "operand_a,operand_b,operation_name,result,timestamp"
