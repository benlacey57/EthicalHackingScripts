from scripts.setup import create_challenge
from scripts.connect_vpn import connect_vpn
from scripts.scenarios import list_scenarios, run_scenario, validate_scenarios
from scripts.utils import load_config

def main_menu():
    """
    Displays the main menu for the HTB Challenge Tool.
    """
    while True:
        print("\nHTB Challenge Tool")
        print("1. Set up a new challenge")
        print("2. Connect to VPN")
        print("3. Scenarios")
        print("4. Run tools")
        print("5. Generate report")
        print("6. Validate scenario configs")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_challenge()
        elif choice == "2":
            connect_vpn()
        elif choice == "3":
            scenarios_menu()
        elif choice == "4":
            run_tool.run_tools_menu()
        elif choice == "5":
            report.generate_report()
        elif choice == "6":
            validate_scenarios()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
