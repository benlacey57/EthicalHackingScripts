from scripts import setup, connect_vpn, run_tool, report
from scripts import scenarios
from scripts import utils
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def main_menu():
    """
    Main menu for the HTB Challenge Tool.
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
            setup.create_challenge()
        elif choice == "2":
            connect_vpn.connect_to_vpn()
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

def scenarios_menu():
    """
    Displays the scenarios menu, listing available scenarios
    and allowing the user to select one to execute.
    """
    scenarios = list_scenarios()

    if not scenarios:
        print("\nNo scenarios available.")
        return

    print("\nAvailable Scenarios:")
    for idx, scenario in enumerate(scenarios, start=1):
        print(f"{idx}. {scenario['name']} - {scenario['description']}")

    choice = input("\nSelect a scenario to run (number): ")

    try:
        scenario = scenarios[int(choice) - 1]
        challenge_name = input("Enter the challenge name: ").capitalize()
        base_path = load_config("base")["base_directory"]
        challenge_path = os.path.join(os.path.expanduser(base_path), challenge_name)

        # Show a summary of the scenario tasks
        print("\nScenario Summary:")
        for task in scenario["tasks"]:
            print(f"- {task['name']}: {task['command']}")

        confirm = input("\nProceed with this scenario? (y/n): ").lower()
        if confirm == "y":
            run_scenario(scenario, challenge_path)
        else:
            print("Scenario execution canceled.")
    except (IndexError, ValueError):
        print("Invalid choice. Returning to menu.")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main_menu()
