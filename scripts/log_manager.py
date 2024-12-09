import os
from datetime import datetime

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
