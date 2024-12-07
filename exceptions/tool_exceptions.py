class ToolError(Exception):
    """Base class for tool-related exceptions."""
    pass

class ConfigFileNotFoundError(ToolError):
    """Raised when the configuration file for a tool is not found."""
    def __init__(self, tool_name):
        super().__init__(f"Configuration file for tool '{tool_name}' not found.")

class InvalidPresetError(ToolError):
    """Raised when an invalid preset is selected."""
    def __init__(self, preset, tool_name):
        super().__init__(f"Preset '{preset}' is not valid for tool '{tool_name}'.")

class ToolExecutionError(ToolError):
    """Raised when a tool execution fails."""
    def __init__(self, tool_name, message):
        super().__init__(f"Error executing tool '{tool_name}': {message}")
