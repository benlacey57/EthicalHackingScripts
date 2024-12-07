import os
import json
import subprocess
from datetime import datetime

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

def search_vulnerabilities_kali(service, version):
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