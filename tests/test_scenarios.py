import os
import json
import pytest
from scripts.scenarios import list_scenarios, validate_scenarios, run_scenario
from scripts.utils import load_config

@pytest.fixture
def setup_scenario_files(tmp_path):
    """Creates valid and invalid scenario files for testing."""
    valid_scenario = {
        "name": "Recon",
        "description": "Performs reconnaissance tasks.",
        "tasks": [
            {"name": "Nmap Scan", "command": "nmap stealth"},
            {"name": "Gobuster Scan", "command": "gobuster directory"}
        ]
    }
    invalid_scenario = {
        "description": "Missing required keys.",
        "tasks": [{"command": "nmap normal"}]
    }
    scenarios_dir = tmp_path / "scenarios"
    scenarios_dir.mkdir()
    with open(scenarios_dir / "valid.json", "w") as f:
        json.dump(valid_scenario, f)
    with open(scenarios_dir / "invalid.json", "w") as f:
        json.dump(invalid_scenario, f)
    return scenarios_dir

def test_list_scenarios(setup_scenario_files, monkeypatch):
    """Tests listing all scenarios."""
    monkeypatch.setattr("os.listdir", lambda x: os.listdir(setup_scenario_files))
    scenarios = list_scenarios()
    assert len(scenarios) == 2
    assert scenarios[0]["name"] == "Recon"

def test_validate_scenarios(setup_scenario_files, monkeypatch):
    """Tests validating scenarios for missing keys or invalid commands."""
    monkeypatch.setattr("os.listdir", lambda x: os.listdir(setup_scenario_files))
    monkeypatch.setattr("os.path.join", lambda x, y: setup_scenario_files / y)

    validate_scenarios()

def test_run_scenario_success(setup_scenario_files, monkeypatch, mocker):
    """Tests running a valid scenario."""
    valid_scenario_file = setup_scenario_files / "valid.json"
    with open(valid_scenario_file, "r") as f:
        scenario = json.load(f)

    challenge_path = setup_scenario_files / "TestChallenge"
    challenge_path.mkdir()

    mocker.patch("scripts.run_tool.run_tool", return_value=None)  # Mock tool execution
    run_scenario(scenario, challenge_path)

    log_file = challenge_path / "challenge.log"
    assert log_file.exists()
    with open(log_file, "r") as f:
        logs = f.read()
    assert "Task 'Nmap Scan' executed successfully." in logs
    assert "Task 'Gobuster Scan' executed successfully." in logs

def test_run_scenario_task_failure(setup_scenario_files, monkeypatch, mocker):
    """Tests task-level error handling during scenario execution."""
    valid_scenario_file = setup_scenario_files / "valid.json"
    with open(valid_scenario_file, "r") as f:
        scenario = json.load(f)

    challenge_path = setup_scenario_files / "TestChallenge"
    challenge_path.mkdir()

    # Mock tool execution to raise an exception for the first task
    mocker.patch("scripts.run_tool.run_tool", side_effect=[Exception("Nmap failed"), None])

    run_scenario(scenario, challenge_path)

    log_file = challenge_path / "challenge.log"
    assert log_file.exists()
    with open(log_file, "r") as f:
        logs = f.read()
    assert "Task 'Nmap Scan' failed with error: Nmap failed" in logs
    assert "Task 'Gobuster Scan' executed successfully." in logs
