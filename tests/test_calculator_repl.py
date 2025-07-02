import pytest
from unittest.mock import patch
from app.calculator_repl import REPL

@pytest.fixture
def mock_config():

    with patch('app.calculator_config.CalculatorConfig') as MockConfig:
        instance = MockConfig.return_value
        instance.history_file_path = "dummy_history.csv"
        yield instance

@pytest.fixture
def repl_instance(mock_config):

    with patch('app.history.HistoryManager.load_from_csv', return_value=None):
        with patch('app.history.HistoryManager.save_to_csv', return_value=None):
            repl = REPL()
   
            repl.config = mock_config
            repl.calculator._config = mock_config
            yield repl

def test_repl_init_failure(capsys):

    with patch('os.getenv', return_value=None):
        repl = REPL()
        assert repl.calculator is None
        captured = capsys.readouterr()
        assert "Initialization Error" in captured.out

@patch('builtins.input', side_effect=['add 2 3', 'history', 'exit'])
def test_repl_add_and_history(mock_input, capsys, repl_instance):

    repl_instance.run()
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert "[LOG] Calculation performed" in captured.out
    assert "0        2.0        3.0       add     5.0" in captured.out

@patch('builtins.input', side_effect=['add 10 5', 'undo', 'history', 'redo', 'history', 'exit'])
def test_repl_undo_redo(mock_input, capsys, repl_instance):

    repl_instance.run()
    captured = capsys.readouterr()
    assert "Undo successful." in captured.out
    assert "History ---\nEmpty." in captured.out
    assert "Redo successful." in captured.out
    assert "0       10.0        5.0       add    15.0" in captured.out

@patch('builtins.input', side_effect=['add 2 3', 'clear', 'history', 'exit'])
def test_repl_clear(mock_input, capsys, repl_instance):

    repl_instance.run()
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert "History cleared." in captured.out
    assert "History ---\nEmpty." in captured.out

@patch('builtins.input', side_effect=['invalid_command', 'exit'])
def test_repl_invalid_command(mock_input, capsys, repl_instance):
    repl_instance.run()
    captured = capsys.readouterr()
    assert "Unknown command: 'invalid_command'" in captured.out

@patch('builtins.input', side_effect=['add 10', 'exit'])
def test_repl_invalid_args(mock_input, capsys, repl_instance):
    repl_instance.run()
    captured = capsys.readouterr()
    assert "Error: Exactly two numbers are required" in captured.out

def test_observer_not_implemented():

    from app.calculator_repl import Observer
    obs = Observer()
    with pytest.raises(NotImplementedError):
        obs.update("event", "data")