
import os
import subprocess
from scripts.utils import load_config, validate_command, prompt_user_input
from scripts.log_manager import log_action
from scripts.exceptions import ConfigFileNotFoundError, InvalidPresetError, ToolExecutionError

def run_tool(tool_name, preset, challenge_path):
    """
    Executes a tool with a specified preset for a given challenge.

    Args:
        tool_name (str): The name of the tool to run (e.g., 'nmap').
        preset (str): The name of the preset to use (e.g., 'stealth').
        challenge_path (str): The path to the challenge directory.

    Raises:
        FileNotFoundError: If the tool's config file or output file is missing.
        ValueError: If the preset is invalid.
    """
    try:
        # Load tool configuration
        config = load_config(tool_name)
        if not config:
            raise ConfigFileNotFoundError(tool_name)
            
        output_file = config.get("output_file", f"{tool_name}.txt")

        # Validate the preset
        preset_config = next((p for p in config.get("presets", []) if p["name"] == preset), None)
        if not preset_config:
            raise InvalidPresetError(preset, tool_name)

        # Construct the command
        command = preset_config["command"]
        output_path = os.path.join(challenge_path, output_file)
        full_command = f"{tool_name} {command} -o {output_path}"

        # Log the tool execution
        log_action(challenge_path, f"Running tool '{tool_name}' with preset '{preset}': {full_command}")

        # Execute the tool
        print(f"Executing: {full_command}")
        subprocess.run(full_command.split(), check=True)

        # Log success
        log_action(challenge_path, f"Tool '{tool_name}' completed successfully. Output saved to {output_path}.")
        print(f"Output saved to: {output_path}")

    except FileNotFoundError as e:
        log_action(challenge_path, f"Error: {e}")
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        raise ToolExecutionError(tool_name, str(e))
    except Exception as e:
        log_action(challenge_path, f"Unexpected error while running tool '{tool_name}': {e}")
        print(f"Unexpected error: {e}")

def run_tools_menu():
    """
    Displays a menu for running tools with available presets.
    """
    try:
        # Prompt user for tool and preset selection
        tool_name = prompt_user_input("Enter the tool name (e.g., nmap, gobuster)").lower()
        config = load_config(tool_name)

        print("\nAvailable Presets:")
        for idx, preset in enumerate(config.get("presets", []), start=1):
            print(f"{idx}. {preset['name']} - {preset['description']}")

        preset_choice = input("\nSelect a preset (number): ")
        try:
            preset = config["presets"][int(preset_choice) - 1]["name"]
        except (IndexError, ValueError):
            print("Invalid choice. Returning to menu.")
            return

        # Prompt for challenge name
        challenge_name = prompt_user_input("Enter the challenge name").capitalize()
        base_path = load_config("base")["base_directory"]
        challenge_path = os.path.join(os.path.expanduser(base_path), challenge_name)

        # Run the selected tool with the preset
        run_tool(tool_name, preset, challenge_path)
    except FileNotFoundError:
        print(f"Error: Configuration for tool '{tool_name}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")
