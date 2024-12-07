import os
import json
import pytest
from scripts.setup import create_challenge
from scripts.connect_vpn import connect_to_vpn
from scripts.run_tool import run_tool
from scripts.utils import load_config

@pytest.fixture
def setup_environment(tmp_path):
    config = {"base_directory": str(tmp_path)}
    with open("config/base.json", "w") as f:
        json.dump(config, f)
    return tmp_path

def test_full_workflow(setup_environment, monkeypatch, mocker):
    # Step 1: Set up the challenge
    monkeypatch.setattr("builtins.input", lambda x: "TestChallenge" if "name" in x else "127.0.0.1")
    create_challenge()

    challenge_path = setup_environment / "Testchallenge"
    assert os.path.exists(challenge_path)

    # Step 2: Add VPN file
    ovpn_file = challenge_path / "TestChallenge.ovpn"
    ovpn_file.write_text("dummy vpn config")
    
    # Step 3: Connect to VPN
    monkeypatch.setattr("builtins.input", lambda x: "TestChallenge")
    mocker.patch("subprocess.run", return_value=None)
    connect_to_vpn()

    # Step 4: Run Nmap tool
    mocker.patch("subprocess.run", return_value=None)
    run_tool("nmap")

    # Verify Nmap output
    nmap_file = challenge_path / "nmap.txt"
    assert nmap_file.exists()

    # Verify logs
    log_file = challenge_path / "challenge.log"
    assert log_file.exists()
    with open(log_file, "r") as f:
        logs = f.read()
        assert "Running Nmap" in logs
        assert "Connecting to VPN" in logs
