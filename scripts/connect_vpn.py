import os
import subprocess
from scripts.utils import prompt_user_input, load_challenge_metadata
from scripts.log_manager import log_action

def connect_to_vpn():
    """
    Connects to the VPN using the .ovpn file located in the challenge directory.
    
    Prompts the user for the challenge name and ensures the .ovpn file exists.
    Logs the connection process.
    """
    try:
        # Prompt user for challenge name
        challenge_name = prompt_user_input("Enter the challenge name").capitalize()
        
        # Load challenge metadata and directory
        base_path = os.path.expanduser(load_config("base")["base_directory"])
        challenge_path = os.path.join(base_path, challenge_name)
        metadata = load_challenge_metadata(challenge_path)

        # Check for the .ovpn file
        ovpn_file = os.path.join(challenge_path, f"{challenge_name}.ovpn")
        if not os.path.exists(ovpn_file):
            raise FileNotFoundError(f"No .ovpn file found for challenge '{challenge_name}' at {ovpn_file}.")

        # Log the connection attempt
        log_action(challenge_path, f"Attempting to connect to VPN for challenge '{challenge_name}'.")

        # Connect to the VPN
        print(f"Connecting to VPN using {ovpn_file}...")
        subprocess.run(["sudo", "openvpn", "--config", ovpn_file], check=True)

        # Log the successful connection
        log_action(challenge_path, "VPN connection established successfully.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        log_action(challenge_path, f"VPN connection failed: {e}")
        print(f"Error: Failed to connect to VPN. Check your configuration and try again.")
    except Exception as e:
        print(f"Unexpected error: {e}")
