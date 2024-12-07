import os
import json
from scripts import run_tool
from scripts import utils
from scripts.exceptions import ScenarioFileNotFoundError, InvalidScenarioStructureError, ScenarioExecutionError

def list_scenarios():
    """Lists all available scenarios."""
    scenario_folder = "scenarios"
    scenarios = []
    for file in os.listdir(scenario_folder):
        if file.endswith(".json"):
            with open(os.path.join(scenario_folder, file), "r") as f:
                try:
                    data = json.load(f)
                    scenarios.append({
                        "name": data.get("name", "Unnamed Scenario"),
                        "description": data.get("description", "No description available."),
                        "file": file
                    })
                except json.JSONDecodeError:
                    scenarios.append({"name": "Invalid Scenario", "description": "Error reading JSON.", "file": file})
    return scenarios

def validate_scenarios():
    """Validates all scenario JSON files."""
    scenario_folder = "scenarios"
    report = []

    for file in os.listdir(scenario_folder):
        if file.endswith(".json"):
            issues = []
            scenario_file = os.path.join(scenario_folder, file)

            try:
                with open(scenario_file, "r") as f:
                    data = json.load(f)

                # Check required keys
                for key in ["name", "description", "tasks"]:
                    if key not in data:
                        issues.append(f"Missing key: {key}")

                # Check tasks
                for task in data.get("tasks", []):
                    if "name" not in task or "command" not in task:
                        issues.append(f"Task missing required keys: {task}")
                    else:
                        # Validate command
                        tool, preset = task["command"].split()
                        if not validate_command(tool, preset):
                            issues.append(f"Invalid command: {task['command']}")

            except json.JSONDecodeError:
                issues.append("Invalid JSON format.")

            report.append({"file": file, "issues": issues})

    # Generate report
    print("\nScenario Validation Report:")
    for entry in report:
        print(f"\nFile: {entry['file']}")
        if entry["issues"]:
            for issue in entry["issues"]:
                print(f"- {issue}")
        else:
            print("No issues found.")
            
def load_scenario(scenario_name):
    """Loads a scenario JSON file."""
    scenario_file = os.path.join("scenarios", f"{scenario_name}.json")
    if not os.path.exists(scenario_file):
        raise FileNotFoundError(f"Scenario '{scenario_name}' not found.")
    with open(scenario_file, "r") as f:
        return json.load(f)

def run_scenario(scenario_name, challenge_path):
    """Executes all tasks in the given scenario."""
    try:
        scenario = load_scenario(scenario_name)
        
        # Validate scenario structure
        required_keys = ["name", "tasks"]
        missing_keys = [key for key in required_keys if key not in scenario]
        if missing_keys:
            raise InvalidScenarioStructureError(scenario["name"], missing_keys)
            
        print(f"\nRunning Scenario: {scenario['name']}")
        print(scenario["description"])
        
        """Executes all tasks in the given scenario."""
        for task in scenario["tasks"]:
            try:
                print(f"\nExecuting Task: {task['name']}")
                tool, preset = task["command"].split()
                run_tool(tool, preset, challenge_path)
                log_action(challenge_path, f"Task '{task['name']}' executed successfully.")
            except Exception as e:
                print(f"Error executing task '{task['name']}': {e}")
                log_action(challenge_path, f"Task '{task['name']}' failed with error: {e}")
        print("\n")
        print("\nScenario completed successfully.")
    except Exception as e:
        raise ScenarioExecutionError(task["name"], str(e))
