import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

def test_config_load_success(monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "test_logs")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "test_data")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "999")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "latin-1")
    
    config = CalculatorConfig()
    assert config.log_dir == "test_logs"
    assert config.max_history == 50
    assert not config.auto_save
    assert config.precision == 2
    assert config.max_input == 999
    assert config.encoding == "latin-1"

def test_config_defaults(monkeypatch):
    monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
    monkeypatch.delenv("CALCULATOR_MAX_HISTORY_SIZE", raising=False)
    
    config = CalculatorConfig()
    assert config.log_dir == "logs"
    assert config.max_history == 100 

@pytest.mark.parametrize("var_name, bad_value", [
    ("CALCULATOR_MAX_HISTORY_SIZE", "abc"),
    ("CALCULATOR_PRECISION", "xyz"),
    ("CALCULATOR_MAX_INPUT_VALUE", "one"),
    ("CALCULATOR_AUTO_SAVE", "maybe")
])
def test_config_invalid_values(monkeypatch, var_name, bad_value):
    monkeypatch.setenv(var_name, bad_value)
    with pytest.raises(ConfigurationError):
        CalculatorConfig()
