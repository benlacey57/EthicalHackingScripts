import os
from datetime import datetime
from scripts.utils import load_challenge_metadata, read_log

def generate_report():
    """
    Generates a consolidated report for a challenge.

    Combines log entries and tool outputs into a single Markdown report file.
    Prompts the user for the challenge name and saves the report in the challenge directory.
    """
    try:
        # Prompt user for the challenge name
        challenge_name = input("Enter the challenge name: ").capitalize()
        base_path = os.path.expanduser(load_config("base")["base_directory"])
        challenge_path = os.path.join(base_path, challenge_name)

        # Validate challenge metadata and directory
        metadata = load_challenge_metadata(challenge_path)

        # Prepare report content
        report_content = []
        report_content.append(f"# Report for Challenge: {metadata['name']}\n")
        report_content.append(f"**IP Address:** {metadata['ip']}\n")
        report_content.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        report_content.append("## Logs\n")

        # Add log entries
        log_file_content = read_log(challenge_path)
        if log_file_content:
            report_content.append("```\n" + log_file_content + "\n```\n")
        else:
            report_content.append("_No log entries available._\n\n")

        # Add tool outputs
        report_content.append("## Tool Outputs\n")
        for file in os.listdir(challenge_path):
            if file.endswith(".txt"):
                file_path = os.path.join(challenge_path, file)
                with open(file_path, "r") as f:
                    tool_output = f.read()
                report_content.append(f"### {file}\n")
                report_content.append("```\n" + tool_output + "\n```\n")

        # Save the report
        report_file = os.path.join(challenge_path, "report.md")
        with open(report_file, "w") as f:
            f.write("\n".join(report_content))

        print(f"Report generated successfully: {report_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
