import os
from datetime import datetime

def log_action(challenge_path, message):
    """
    Logs a message to the challenge's log file.

    Args:
        challenge_path (str): The path to the challenge directory.
        message (str): The message to log.
    """
    try:
        log_file = os.path.join(challenge_path, "challenge.log")
        os.makedirs(challenge_path, exist_ok=True)

        # Format log message with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        # Write log entry to the file
        with open(log_file, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error logging action: {e}")

def read_log(challenge_path):
    """
    Reads and returns the content of the challenge's log file.

    Args:
        challenge_path (str): The path to the challenge directory.

    Returns:
        str: The content of the log file.

    Raises:
        FileNotFoundError: If the log file does not exist.
    """
    log_file = os.path.join(challenge_path, "challenge.log")
    if not os.path.exists(log_file):
        raise FileNotFoundError(f"Log file not found in challenge directory '{challenge_path}'.")

    with open(log_file, "r") as f:
        return f.read()

def clear_log(challenge_path):
    """
    Clears the content of the challenge's log file.

    Args:
        challenge_path (str): The path to the challenge directory.
    """
    log_file = os.path.join(challenge_path, "challenge.log")
    if os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.truncate()
        print(f"Log file '{log_file}' cleared.")
    else:
        print(f"No log file to clear in '{challenge_path}'.")
