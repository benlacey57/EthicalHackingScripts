import pytest
import json

from scripts.utils import validate_command, validate_json_keys
from scripts.utils import load_config

@pytest.fixture
def mock_nmap_config(tmp_path):
    """Creates a mock nmap configuration file."""
    nmap_config = {
        "presets": [
            {"name": "normal", "command": "-sS -sV"},
            {"name": "stealth", "command": "-sS -sV -p-"}
        ]
    }
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "nmap.json"
    with open(config_file, "w") as f:
        json.dump(nmap_config, f)
    return config_file


def test_load_config_valid():
    config = load_config("base")
    assert "base_directory" in config

def test_load_config_invalid():
    with pytest.raises(FileNotFoundError):
        load_config("invalid_tool")
        
def test_validate_command_valid(mock_nmap_config, monkeypatch):
    """Tests validating a valid tool and preset."""
    monkeypatch.setattr("scripts.utils.load_config", lambda tool: json.load(open(mock_nmap_config)))
    assert validate_command("nmap", "stealth") is True

def test_validate_command_invalid(mock_nmap_config, monkeypatch):
    """Tests validating an invalid preset."""
    monkeypatch.setattr("scripts.utils.load_config", lambda tool: json.load(open(mock_nmap_config)))
    assert validate_command("nmap", "invalid-preset") is False

def test_validate_json_keys():
    """Tests validation of JSON keys."""
    data = {"name": "Scenario", "description": "A test scenario."}
    required_keys = ["name", "description", "tasks"]
    missing_keys = validate_json_keys(data, required_keys)
    assert missing_keys == ["tasks"]
