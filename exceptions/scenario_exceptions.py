class ScenarioError(Exception):
    """Base class for scenario-related exceptions."""
    pass

class ScenarioFileNotFoundError(ScenarioError):
    """Raised when a scenario JSON file is not found."""
    def __init__(self, file_path):
        super().__init__(f"Scenario file '{file_path}' not found.")

class InvalidScenarioStructureError(ScenarioError):
    """Raised when the scenario structure is invalid."""
    def __init__(self, scenario_name, missing_keys):
        super().__init__(f"Scenario '{scenario_name}' is missing required keys: {missing_keys}")

class ScenarioExecutionError(ScenarioError):
    """Raised when a scenario task fails."""
    def __init__(self, task_name, error_message):
        super().__init__(f"Error executing task '{task_name}': {error_message}")
