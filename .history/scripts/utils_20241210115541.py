import os
import json
import subprocess

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

    try:
        with open(config_file, "r") as f:
            

def check_and_create_directory(directory_path):
    """
    Checks if a directory exists and creates it if it doesn't.
    
    Args:
        directory_path (str): The path of the directory to check or create.
    
    Returns:
        bool: True if the directory exists or is created successfully, False otherwise.
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        else:
            print(f"Directory already exists: {directory_path}")
        return True
    except OSError as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False

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

def search_vulnerabilities(service, version):
    """
    Searches for vulnerabilities using the local vulnerability database (searchsploit).

    Args:
        service (str): The name of the service (e.g., 'http').
        version (str): The version of the service (e.g., 'Apache/2.4.41').

    Returns:
        list: A list of vulnerabilities, each containing name, summary, and link.

    Raises:
        Exception: If the search fails or no vulnerabilities are found.
    """
    try:
        query = f"{service} {version}"
        result = subprocess.run(
            ["searchsploit", query, "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Searchsploit error: {result.stderr.strip()}")

        data = json.loads(result.stdout)
        vulnerabilities = []
        for exploit in data.get("RESULTS_EXPLOIT", []):
            vulnerabilities.append({
                "name": exploit.get("Title", "Unknown"),
                "summary": exploit.get("Description", "No description available."),
                "link": f"https://www.exploit-db.com/exploits/{exploit.get('EDB-ID', 'Unknown')}"
            })

        if not vulnerabilities:
            raise Exception("No vulnerabilities found for the given query.")

        return vulnerabilities

    except Exception as e:
        raise Exception(f"Error searching vulnerabilities: {e}")

def validate_command(tool_name, preset, config):
    """
    Validates that the given tool and preset exist in the provided configuration.

    Args:
        tool_name (str): The name of the tool to validate (e.g., 'nmap').
        preset (str): The name of the preset to validate (e.g., 'quick').
        config (dict): The configuration dictionary containing tool details.

    Returns:
        bool: True if the tool and preset are valid, False otherwise.

    Raises:
        KeyError: If the tool is not found in the configuration.
        ValueError: If the preset is invalid for the given tool.
    """
    try:
        # Check if the tool exists in the config
        if tool_name not in config:
            raise KeyError(f"Tool '{tool_name}' not found in configuration.")

        # Check if the preset exists for the tool
        presets = [p["name"] for p in config[tool_name].get("presets", [])]
        if preset not in presets:
            raise ValueError(f"Preset '{preset}' is not valid for tool '{tool_name}'.")

        return True
    except KeyError as e:
        print(f"Validation Error: {e}")
        return False
    except ValueError as e:
        print(f"Validation Error: {e}")
        return False

def prompt_user_input(prompt):
    """
    Prompts the user for input with a given prompt message.
    
    Args:
        prompt (str): The message to display to the user.
        
    Returns:
        str: The user's input.
    """
    try:
        return input(f"{prompt}: ").strip()
    except KeyboardInterrupt:
        print("\nInput cancelled by user.")
        return None
