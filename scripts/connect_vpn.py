import os
import subprocess
from scripts.utils import prompt_user_input, load_config, load_challenge_metadata
from scripts.log_manager import log_action
from exceptions import NoVPNFilesFoundError, VPNConnectionError

def connect_vpn( challenge_path ):
    """
    Connect to the VPN using the specified .ovpn file in a separate process.

    Args:
        challenge_path (str): Path to the challenge directory.

    Raises:
        VPNConnectionError: If the VPN connection fails.
    """
    try:        
        # Load base directory from config and challenge metadata
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
        log_action(challenge_path, f"Attempting to connect to VPN using '{ovpn_file}'")

        # Connect to the VPN in a separate process
        print(f"Connecting to VPN using {ovpn_file} ...")
        process = subprocess.Popen(
            ["sudo", "openvpn", "--config", ovpn_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        log_action(challenge_path, "[CONNECTED] VPN connection successful.")
        print("VPN connection started successfully. Make sure you can ping the virtual machine.")

    except FileNotFoundError:
        raise NoVPNFilesFoundError(challenge_path)
    except subprocess.CalledProcessError as e:
        raise VPNConnectionError(f"[ERROR] Failed to connect to VPN: {e}")
    except Exception as e:
        log_action(challenge_path, f"[ERROR] Unexpected error while connecting to VPN: {e}")
        raise VPNConnectionError(f"[ERROR] Unexpected error: {e}")
