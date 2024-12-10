import os
import json
from scripts.log_manager import log_action
from scripts.utils import prompt_user_input, check_and_create_directory, load_config

def create_challenge():
    """
    Creates a new challenge directory with metadata.

    Prompts the user for a challenge name and IP address, then creates
    the necessary folder structure and metadata file.

    Returns:
        list: The challenge name and path if successful.
    """
    try:
        # Load base directory from config
        base_config = load_config("base")
        base_path = os.path.expanduser(base_config.get("base_directory", "~/HTB"))

        # Prompt for challenge name and IP address
        challenge_name = prompt_user_input("Enter the challenge name")

        # Validate inputs
        if not challenge_name:
            raise ValueError("Challenge name cannot be empty.")

        # Define the challenge directory path
        challenge_path = os.path.join(base_path, challenge_name)

        # Create the directory structure
        check_and_create_directory(challenge_path)

        # Create metadata file
        metadata = {"name": challenge_name, "ip": "", "flags": []}
        metadata_file = os.path.join(challenge_path, "metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        # Notify the user
        print(f"Challenge '{challenge_name}' created successfully at {challenge_path}.")
        log_action(challenge_path, f"Challenge created: {metadata}")

        return [challenge_name, challenge_path]
    
    except Exception as e:
        print(f"Error creating challenge: {e}")

def validate_challenge_directory(challenge_name):
    """
    Validates the existence of a challenge directory and its metadata.

    Args:
        challenge_name (str): The name of the challenge.

    Returns:
        str: The path to the challenge directory if valid.

    Raises:
        FileNotFoundError: If the challenge directory or metadata file is missing.
    """
    base_config = load_config("base")
    base_path = os.path.expanduser(base_config.get("base_directory", "~/HTB"))
    challenge_path = os.path.join(base_path, challenge_name)

    if not os.path.exists(challenge_path):
        raise FileNotFoundError(f"Challenge directory '{challenge_name}' does not exist.")

    metadata_file = os.path.join(challenge_path, "metadata.json")
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"Metadata file missing in challenge directory '{challenge_name}'.")

    return challenge_path
