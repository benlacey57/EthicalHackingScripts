import os
import json
import pytest
from scripts.setup import create_challenge
from scripts.connect_vpn import connect_to_vpn
from scripts.run_tool import run_tool
from scripts.utils import load_config

@pytest.fixture
def setup_integration_environment(tmp_path):
    """Sets up a complete integration environment."""
    # Mock base config
    base_config = {"base_directory": str(tmp_path)}
    with open("config/base.json", "w") as f:
        json.dump(base_config, f)

    # Mock scenario
    scenario = {
        "name": "Recon",
        "description": "Performs reconnaissance tasks.",
        "tasks": [
            {"name": "Nmap Scan", "command": "nmap stealth"},
            {"name": "Gobuster Scan", "command": "gobuster directory"}
        ]
    }
    scenarios_dir = tmp_path / "scenarios"
    scenarios_dir.mkdir()
    with open(scenarios_dir / "recon.json", "w") as f:
        json.dump(scenario, f)

    # Mock challenge
    challenge_path = tmp_path / "TestChallenge"
    challenge_path.mkdir()
    with open(challenge_path / "metadata.json", "w") as f:
        json.dump({"name": "TestChallenge", "ip": "127.0.0.1"}, f)

    return tmp_path, challenge_path

def test_integration_run_scenario(setup_integration_environment, mocker):
    """Tests running a scenario end-to-end."""
    base_path, challenge_path = setup_integration_environment

    mocker.patch("scripts.run_tool.run_tool", return_value=None)  # Mock tool execution
    scenario_file = os.path.join(base_path, "scenarios", "recon.json")
    with open(scenario_file, "r") as f:
        scenario = json.load(f)

    run_scenario(scenario, challenge_path)

    # Verify log file
    log_file = challenge_path / "challenge.log"
    assert log_file.exists()
    with open(log_file, "r") as f:
        logs = f.read()
    assert "Task 'Nmap Scan' executed successfully." in logs
    assert "Task 'Gobuster Scan' executed successfully." in logs
