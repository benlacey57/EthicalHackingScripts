import os
import subprocess
from scripts.utils import prompt_user_input, load_config, load_challenge_metadata
from scripts.log_manager import log_action
from scripts.exceptions import NoVPNFilesFoundError, VPNConnectionError

def connect_vpn():
    """
    Connect to the VPN using the specified .ovpn file in a separate process.

    Args:
        challenge_path (str): Path to the challenge directory.
        ovpn_file (str): Path to the .ovpn file to use.

    Raises:
        VPNConnectionError: If the VPN connection fails.
    """
    try:
        # Prompt user for challenge name
        challenge_name = prompt_user_input("Enter the challenge name").capitalize()

        # Load base directory from config and challenge metadata
        base_path = os.path.expanduser(load_config("base")["base_directory"])
        challenge_path = os.path.join(base_path, challenge_name)
        metadata = load_challenge_metadata(challenge_path)

        # Find the newest .ovpn file in the challenge directory
        ovpn_files = [
            os.path.join(challenge_path, f) for f in os.listdir(challenge_path) if f.endswith(".ovpn")
        ]
        if not ovpn_files:
            raise NoVPNFilesFoundError(challenge_path)
        
        # Select the newest file based on modification time
        ovpn_file = max(ovpn_files, key=os.path.getmtime)

        # Log the connection attempt
        log_action(challenge_path, f"Attempting to connect to VPN using '{ovpn_file}' for challenge '{challenge_name}'.")

        # Connect to the VPN in a separate process
        print(f"Connecting to VPN using {ovpn_file} ...")
        process = subprocess.Popen(
            ["sudo", "openvpn", "--config", ovpn_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        log_action(challenge_path, "VPN connection process started successfully.")
        print("VPN connection started successfully. Make sure you can ping the virtual machine.")

    except FileNotFoundError:
        raise NoVPNFilesFoundError(challenge_path)
    except subprocess.CalledProcessError as e:
        raise VPNConnectionError(f"Failed to connect to VPN: {e}")
    except Exception as e:
        log_action(challenge_path, f"Unexpected error while connecting to VPN: {e}")
        raise VPNConnectionError(f"Unexpected error: {e}")
