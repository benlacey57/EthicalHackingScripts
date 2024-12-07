import pytest
from scripts.utils import load_config

def test_load_config_valid():
    config = load_config("base")
    assert "base_directory" in config

def test_load_config_invalid():
    with pytest.raises(FileNotFoundError):
        load_config("invalid_tool")
