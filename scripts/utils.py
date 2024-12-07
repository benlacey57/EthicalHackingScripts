import os
import json
from datetime import datetime


def load_challenge_metadata(challenge_path):
    """
    Loads the metadata file for a specific challenge.

    Args:
        challenge_path (str): The path to the challenge directory.

    Returns:
        dict: The metadata for the challenge.

    Raises:
        FileNotFoundError: If the metadata file does not exist.
    """
    metadata_file = os.path.join(challenge_path, "metadata.json")
    if not os.path.exists(metadata_file):
        raise FileNotFoundError("Metadata file not found in challenge directory.")
    with open(metadata_file, "r") as f:
        return json.load(f)


def save_challenge_metadata(challenge_path, metadata):
    """
    Saves the metadata file for a specific challenge.

    Args:
        challenge_path (str): The path to the challenge directory.
        metadata (dict): The metadata to save.

    Returns:
        None

    Raises:
        Exception: If the metadata file cannot be written.
    """
    metadata_file = os.path.join(challenge_path, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)


def update_challenge_metadata(challenge_path, updates):
    """
    Updates the metadata file for a specific challenge with provided changes.

    Args:
        challenge_path (str): The path to the challenge directory.
        updates (dict): Key-value pairs to update in the metadata.

    Returns:
        None
    """
    metadata = load_challenge_metadata(challenge_path)

    for key, value in updates.items():
        if isinstance(value, list) and key in metadata:
            metadata[key].extend(value)
        elif isinstance(value, dict) and key in metadata:
            metadata[key].update(value)
        else:
            metadata[key] = value

    save_challenge_metadata(challenge_path, metadata)


def add_flag(challenge_path, flag):
    """
    Adds a flag to the metadata file with a timestamp.

    Args:
        challenge_path (str): The path to the challenge directory.
        flag (str): The flag to add.
    """
    update_challenge_metadata(challenge_path, {
        "flags_found": [{"flag": flag, "timestamp": datetime.now().isoformat()}]
    })


def start_challenge(challenge_path):
    """
    Sets the start timestamp for the challenge in the metadata file.

    Args:
        challenge_path (str): The path to the challenge directory.
    """
    update_challenge_metadata(challenge_path, {"start_timestamp": datetime.now().isoformat()})


def end_challenge(challenge_path):
    """
    Sets the end timestamp for the challenge in the metadata file.

    Args:
        challenge_path (str): The path to the challenge directory.
    """
    update_challenge_metadata(challenge_path, {"end_timestamp": datetime.now().isoformat()})



def add_attack_vectors(challenge_path, service, version, vectors):
    """
    Adds attack vectors to the metadata file for a specific service and version.

    Args:
        challenge_path (str): The path to the challenge directory.
        service (str): The service name (e.g., "http").
        version (str): The version of the service (e.g., "Apache/2.4.41").
        vectors (list): A list of attack vectors.
    """
    update_challenge_metadata(challenge_path, {
        "attack_vectors": [{"service": service, "version": version, "vectors": vectors}]
    })


def log_action(challenge_path, message, context=None):
    """
    Logs a message to the challenge's log file with optional context.

    Args:
        challenge_path (str): The path to the challenge directory.
        message (str): The message to log.
        context (dict, optional): Additional context to include in the log.

    Raises:
        Exception: If logging fails.
    """
    log_file = os.path.join(challenge_path, "challenge.log")
    os.makedirs(challenge_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context_str = ""
    if context:
        context_str = " ".join([f"[{k}: {v}]" for k, v in context.items()])
    log_message = f"[{timestamp}] {context_str} {message}\n"
    with open(log_file, "a") as f:
        f.write(log_message)