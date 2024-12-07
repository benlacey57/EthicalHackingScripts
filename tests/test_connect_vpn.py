import os
import pytest
from scripts.connect_vpn import connect_to_vpn
from scripts.log_manager import log_action

@pytest.fixture
def vpn_file(tmp_path):
    challenge_name = "TestChallenge"
    challenge_path = tmp_path / challenge_name
    challenge_path.mkdir()
    ovpn_file = challenge_path / f"{challenge_name}.ovpn"
    ovpn_file.write_text("dummy vpn config")
    return challenge_path

def test_connect_vpn_file_not_found(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: "NonexistentChallenge")
    with pytest.raises(SystemExit):
        connect_to_vpn()

def test_connect_vpn_success(vpn_file, monkeypatch, mocker):
    monkeypatch.setattr("builtins.input", lambda x: "TestChallenge")
    mocker.patch("subprocess.run", return_value=None)  # Mock openvpn execution
    connect_to_vpn()

    log_file = vpn_file / "challenge.log"
    assert log_file.exists()
    with open(log_file, "r") as f:
        assert "Connecting to VPN" in f.read()
