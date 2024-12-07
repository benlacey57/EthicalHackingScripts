import os
import pytest
from scripts.run_tool import run_tool
from scripts.utils import load_config

@pytest.fixture
def challenge_setup(tmp_path):
    challenge_name = "TestChallenge"
    challenge_path = tmp_path / challenge_name
    challenge_path.mkdir()

    metadata = {"name": challenge_name, "ip": "127.0.0.1"}
    with open(challenge_path / "metadata.json", "w") as f:
        json.dump(metadata, f)
    return challenge_path

def test_run_tool_missing_metadata(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: "NonexistentChallenge")
    with pytest.raises(FileNotFoundError):
        run_tool("nmap")

def test_run_tool_success(challenge_setup, monkeypatch, mocker):
    monkeypatch.setattr("builtins.input", lambda x: "TestChallenge")
    mocker.patch("subprocess.run", return_value=None)  # Mock Nmap execution
    run_tool("nmap")
    
    nmap_file = challenge_setup / "nmap.txt"
    assert nmap_file.exists()
