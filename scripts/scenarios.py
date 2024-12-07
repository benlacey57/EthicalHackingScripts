import os
import json
from scripts.run_tool import run_tool
from scripts.utils import load_config

def list_scenarios():
    """Lists all available scenarios in the scenarios folder."""
    scenario_folder = "scenarios"
    return [file.split(".")[0] for file in os.listdir(scenario_folder) if file.endswith(".json")]

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
        print(f"\nRunning Scenario: {scenario['name']}")
        print(scenario["description"])

        for task in scenario["tasks"]:
            print(f"\nExecuting Task: {task['name']}")
            tool, preset = task["command"].split()
            run_tool(tool, preset, challenge_path)
        
        print("\nScenario completed successfully.")
    except Exception as e:
        print(f"Error running scenario: {e}")
