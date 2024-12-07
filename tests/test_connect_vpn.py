import os
import pytest
from scripts.connect_vpn import connect_vpn
from scripts.utils import load_config, log_action

@pytest.fixture
def mock_challenge_directory(tmp_path):
    """
    Creates a mock challenge directory with multiple .ovpn files.
    """
    challenge_name = "TestChallenge"
    challenge_path = tmp_path / challenge_name
    challenge_path.mkdir()

    # Create mock .ovpn files
    vpn_file1 = challenge_path / "vpn1.ovpn"
    vpn_file1.write_text("Mock VPN configuration 1")
    vpn_file1.touch()

    vpn_file2 = challenge_path / "vpn2.ovpn"
    vpn_file2.write_text("Mock VPN configuration 2")
    vpn_file2.touch()

    # Simulate base directory in config
    base_config = {"base_directory": str(tmp_path)}
    return challenge_path, base_config

def test_connect_vpn_newest_file(mocker, mock_challenge_directory):
    """
    Tests that connect_vpn selects the newest .ovpn file in the directory.
    """
    challenge_path, base_config = mock_challenge_directory

    # Mock load_config to return the temporary base directory
    mocker.patch("scripts.connect_vpn.load_config", return_value=base_config)

    # Mock subprocess.Popen
    mock_popen = mocker.patch("subprocess.Popen")
    mock_log_action = mocker.patch("scripts.connect_vpn.log_action")

    # Run connect_vpn
    connect_vpn()

    # Verify the newest file (vpn2.ovpn) was used
    expected_vpn_file = os.path.join(challenge_path, "vpn2.ovpn")
    mock_popen.assert_called_once_with(
        ["sudo", "openvpn", "--config", expected_vpn_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    mock_log_action.assert_called_with(
        str(challenge_path),
        f"Attempting to connect to VPN using '{expected_vpn_file}' for challenge 'Testchallenge'."
    )

def test_connect_vpn_no_files(mocker, tmp_path):
    """
    Tests that connect_vpn raises a FileNotFoundError if no .ovpn files exist.
    """
    challenge_name = "TestChallenge"
    challenge_path = tmp_path / challenge_name
    challenge_path.mkdir()

    # Simulate base directory in config
    base_config = {"base_directory": str(tmp_path)}
    mocker.patch("scripts.connect_vpn.load_config", return_value=base_config)

    # Mock log_action
    mock_log_action = mocker.patch("scripts.connect_vpn.log_action")

    with pytest.raises(FileNotFoundError, match="No .ovpn files found"):
        connect_vpn()

    # Ensure no VPN process was started
    mock_popen = mocker.patch("subprocess.Popen")
    mock_popen.assert_not_called()
    mock_log_action.assert_not_called()
