class VPNError(Exception):
    """Base class for VPN-related exceptions."""
    pass

class NoVPNFilesFoundError(VPNError):
    """Raised when no .ovpn files are found in the directory."""
    def __init__(self, directory):
        super().__init__(f"No .ovpn files found in the directory '{directory}'.")

class VPNConnectionError(VPNError):
    """Raised when the VPN connection fails."""
    def __init__(self, message):
        super().__init__(f"VPN connection error: {message}")
