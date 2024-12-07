import os
import json

def load_config(tool_name):
    """
    Loads the configuration file for a specific tool.
    
    Args:
        tool_name (str): The name of the tool (e.g., 'nmap', 'gobuster').
    
    Returns:
        dict: The configuration data for the tool.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    config_file = os.path.join("config", f"{tool_name}.json")
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file for {tool_name} not found.")
    with open(config_file, "r") as f:
        return json.load(f)

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

def validate_command(tool, preset):
    """
    Validates whether a given tool and preset exist in the configurations.

    Args:
        tool (str): The name of the tool (e.g., 'nmap').
        preset (str): The name of the preset to validate.

    Returns:
        bool: True if the tool and preset are valid, False otherwise.
    """
    try:
        config = load_config(tool)
        for p in config.get("presets", []):
            if p["name"] == preset:
                return True
        return False
    except FileNotFoundError:
        return False

def log_action(challenge_path, message):
    """
    Logs a message to the challenge's log file.

    Args:
        challenge_path (str): The path to the challenge directory.
        message (str): The message to log.
    """
    log_file = os.path.join(challenge_path, "challenge.log")
    os.makedirs(challenge_path, exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"{message}\n")

def prompt_user_input(prompt, default=None):
    """
    Prompts the user for input with an optional default value.

    Args:
        prompt (str): The prompt to display to the user.
        default (str, optional): The default value to return if the user enters nothing.

    Returns:
        str: The user's input, or the default value if no input is provided.
    """
    if default:
        user_input = input(f"{prompt} [{default}]: ")
        return user_input.strip() or default
    return input(f"{prompt}: ").strip()

def check_and_create_directory(directory):
    """
    Checks if a directory exists, and creates it if it does not.

    Args:
        directory (str): The directory path to check or create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def validate_json_keys(data, required_keys):
    """
    Validates that a JSON object contains all required keys.

    Args:
        data (dict): The JSON object to validate.
        required_keys (list): A list of required keys.

    Returns:
        list: A list of missing keys, or an empty list if all keys are present.
    """
    missing_keys = [key for key in required_keys if key not in data]
    return missing_keys

def format_task_summary(tasks):
    """
    Formats a list of tasks into a summary string.

    Args:
        tasks (list): A list of task dictionaries, each with 'name' and 'command'.

    Returns:
        str: A formatted string summarizing the tasks.
    """
    summary = "\nTask Summary:\n"
    for idx, task in enumerate(tasks, start=1):
        summary += f"{idx}. {task['name']} - Command: {task['command']}\n"
    return summary
