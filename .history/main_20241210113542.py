from scripts.setup import create_challenge
from scripts.connect_vpn import connect_vpn
from scripts.scenarios import list_scenarios, run_scenario, validate_scenarios
from scripts.run_tool import run_tools_menu
from scripts.utils import load_config
import os
import sys
import subprocess

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_and_install_requirements():
    """
    Checks if required dependencies are installed and installs them if not.
    """
    requirements = {
        "nmap": "nmap",
        "openvpn": "openvpn",
        "gobuster": "gobuster",
        "python3": "python3",
        "pip3": "python3-pip"
    }

    print("Checking system requirements...")
    for name, package in requirements.items():
        try:
            # Check if the dependency is installed
            message = f"Checking {name}..."
            subprocess.run(["which", name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{message} [OK] Already Installed.\n")
        except subprocess.CalledProcessError:
            # If not installed, attempt to install it
            print(f"{message} [ERROR] Not Installed. Installing...")
            try:
                subprocess.run(
                    ["sudo", "apt-get", "update"],
                    check=True
                )

                subprocess.run(
                    ["sudo", "apt-get", "install", "-y", package],
                    check=True
                )
                print(f"{name} has been installed successfully.\n")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {name}. Please install it manually: {e}")

    print("System requirement check complete!")

def main_menu():
    """
    Displays the main menu for the Ethical Hacking Tool.
    """
    while True:
        print("\nEthical Hacking Tool")
        print("-" * 25)
        print("1. Check and Install Requirements")
        print("2. Set up a new challenge")
        print("4. Run Scenario")
        print("5. Run tool")
        print("6. Generate report")
        print("7. Validate scenario configs")
        print("-" * 25)
        print("Q. Exit")
        print("")
        choice = input("Enter your choice: ")
        print("")

        if choice == "1":
            check_and_install_requirements()
        elif choice == "2":
            from scripts.setup import create_challenge
            from scripts.connect_vpn import connect_vpn

            challenge = create_challenge()
            print("")
            print("")
            print("*** Please move your .ovpn file into the challenge directory ***")
            print("")
            input("Press Enter to continue...")

            if challenge:
                connect_vpn( challenge_path=challenge[1] )
                
        elif choice == "3":
            from scripts.scenarios import list_scenarios
            list_scenarios()
        elif choice == "4":
            from scripts.run_tool import run_tool
            run_tool()
        elif choice == "5":
            from scripts.report import generate_report
            generate_report()
        elif choice == "6":
            from scripts.scenarios import validate_scenarios
            validate_scenarios()
        elif choice == "q" or choice == "Q":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
