# Ethical Hacking Scripts
Ethical Hacking scripts using Python and json config files to register options and command presets.

# HTB Challenge Tool

The **HTB Challenge Tool** is a Python-based utility designed to streamline the workflow for Hack The Box (HTB) challenges. It automates repetitive tasks, organizes outputs, and integrates common tools with customizable configurations for efficiency. This tool is modular, easy to maintain, and adheres to DRY and SOLID principles.

---

## Features

1. **Challenge Setup**:
   - Automatically create directories for each challenge.
   - Stores challenge metadata, including the name and IP address.

2. **Tool Integration with Presets**:
   - Supports tools like **Nmap**, **Gobuster**, **Nikto**, and more.
   - Preset configurations allow users to select pre-defined scan types (e.g., `stealth`, `fast`).
   - Flexible JSON configuration for tool customization.

3. **VPN Connectivity**:
   - Automatically connect to the HTB VPN using `.ovpn` files.

4. **Logging**:
   - Logs all actions (e.g., commands executed, errors) in a unified log file for each challenge.

5. **Report Generation**:
   - Consolidates results from all tools into a structured report in Markdown format.

6. **Error Handling**:
   - Validates directories, configurations, and tool installations.
   - Provides meaningful feedback for troubleshooting.

7. **Extensible Design**:
   - Easily add new tools and presets by editing JSON files without modifying code.
   
---

## Installation

This script is intended to be run inside Parrot or Kali Linux installations where most of the tools are already installed.

### Prerequisites

- Python 3.8 or higher
- Linux-based environment (recommended)
- Python venv (Virtual Environment Manager)
- Required tools installed on the system:
  - **Nmap**
  - **Gobuster**
  - **Nikto**
  - **OpenVPN**

### Setup

1. Clone the repository:
   ```bash
   git@github.com:benlacey57/EthicalHackingScripts.git
   cd htb_tool```

2. Install Python venv:
   ```bash
   sudo apt-get install -y python3.12-venv
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
    
4. Install Python dependencies in the virtual environment:
```bash
pip install -r requirements.txt
```

3. Ensure tools like nmap, gobuster, and nikto are installed and accessible in your $PATH.

4. Run the script:
```bash
python3 main.py
```

## Usage
### 1. Main Menu

When you run the tool, you will see the following options:

HTB Challenge Tool
1. Set up a new challenge
2. Connect to VPN
3. Run tools
4. Generate report
5. Exit

### 2. Challenge Setup

Description: Creates a directory for the challenge and stores metadata (e.g., name, IP address).

Steps:

- Select option 1 from the main menu.
- Enter the challenge name and IP address when prompted.
- The tool will create a directory structure like:

~/HTB/ChallengeName/
├── ChallengeName.ovpn
├── challenge.log
└── metadata.json

### 3. Connect to VPN

Description: Connects to the HTB VPN using the .ovpn file in the challenge directory.

Steps:

- Select option 2 from the main menu.
- Enter the challenge name.
- Ensure the .ovpn file is in the challenge directory.
- The tool will use openvpn to establish the connection.

### 4. Run Tools

Description: Executes integrated tools with configurable presets.

Steps:

- Select option 3 from the main menu.
- Choose the tool (e.g., nmap, gobuster).
- Select a preset for the tool.

**Example Preset Menu for Nmap:**
1. normal - Perform a normal scan of the most common 1000 ports with service detection.
2. quick - Perform a quick scan of the most common 100 ports.
3. stealth - Perform a stealthy SYN scan of all 65535 TCP ports with service detection.
4. fast-stealth - Perform a faster stealth scan using timing optimization and skipping DNS resolution.

**Output:** Results are saved in the challenge directory (e.g., nmap.txt, gobuster.txt).

### 5. Generate Report

Description: Consolidates tool outputs and logs into a Markdown report.

Steps:

- Select option 4 from the main menu.
- The report will be saved as report.md in the challenge directory.

## Configuration

Tool configurations are stored in the config/ directory as JSON files.

**Example: nmap.json**
```json
{
  "output_file": "nmap.txt",
  "presets": [
    {
      "name": "normal",
      "description": "Perform a normal scan of the most common 1000 ports with service detection.",
      "command": "-sS -sV"
    },
    {
      "name": "quick",
      "description": "Perform a quick scan of the most common 100 ports.",
      "command": "-F"
    },
    {
      "name": "stealth",
      "description": "Perform a stealthy SYN scan of all 65535 TCP ports with service detection.",
      "command": "-sS -sV -p-"
    },
    {
      "name": "fast-stealth",
      "description": "Perform a faster stealth scan using timing optimization and skipping DNS resolution.",
      "command": "-sS -T4 --min-rate=5000 --max-retries=1 -n"
    }
  ]
}
```

## Testing

The tool includes unit and integration tests located in the tests/ directory.

Run All Tests: pytest tests/

Run a Specific Test: pytest tests/test_setup.py

## Extending the Tools
### Adding a New Tool

- Create a new JSON file in config/ with the tool’s presets.
- Modify run_tool.py to dynamically load the tool from its JSON configuration.

**Example: Adding WPScan**

Create config/wpscan.json:

```json
{
  "output_file": "wpscan.txt",
  "presets": [
    {
      "name": "basic-scan",
      "description": "Perform a basic WordPress scan.",
      "command": "--url http://{ip}/"
    },
    {
      "name": "enumerate-users",
      "description": "Enumerate WordPress users.",
      "command": "--url http://{ip}/ --enumerate u"
    }
  ]
}
```

## FAQs
### What happens if the .ovpn file is missing?

The VPN connection will fail. Ensure the .ovpn file is placed in the challenge directory before attempting to connect.

### Can I add my own wordlists for tools like Gobuster?

Yes! Modify the corresponding command in the JSON configuration to use your custom wordlists.

### How do I reset the tool?

Simply delete the base directory and revert the configuration files in config/.
