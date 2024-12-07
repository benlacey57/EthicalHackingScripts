def validate_command(tool, preset):
    """Validates that the given tool and preset exist."""
    try:
        config = load_config(tool)
        for p in config.get("presets", []):
            if p["name"] == preset:
                return True
        return False
    except FileNotFoundError:
        return False
