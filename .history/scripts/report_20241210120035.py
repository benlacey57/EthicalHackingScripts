import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pdfkit


def load_config(config_name):
    """
    Load the specified configuration file. If no base directory is found,
    fallback to a default 'challenges' folder in the script root.

    Args:
        config_name (str): The name of the configuration file (without extension).

    Returns:
        str: The base directory for storing challenge data.
    """
    config_path = os.path.join('config', f'{config_name}.json')
    try:
        # Attempt to load the configuration file
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty config
        config = {}

    # Define the default challenges folder in the script root
    default_challenges_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'challenges'))
    os.makedirs(default_challenges_path, exist_ok=True)  # Ensure the folder exists

    # Return the configured base directory or fallback to the default
    return config.get('base_directory', default_challenges_path)


def load_tool_data(challenge_dir):
    """
    Load tool output files from the challenge directory.

    Args:
        challenge_dir (str): The directory containing challenge tool output files.

    Returns:
        dict: A dictionary mapping tool names to their respective output data.
    """
    tool_data = {}
    for filename in os.listdir(challenge_dir):
        if filename.endswith(".txt"):
            tool_name = os.path.splitext(filename)[0]
            with open(os.path.join(challenge_dir, filename), "r") as f:
                tool_data[tool_name] = f.read()
    return tool_data


def load_glossary():
    """
    Load the glossary data from the JSON file.

    Returns:
        dict: A dictionary containing terms and tools for glossary reference.
    """
    try:
        with open('glossary.json', 'r') as f:
            glossary = json.load(f)
    except FileNotFoundError:
        glossary = {"terms": {}, "tools": {}}
    return glossary


def search_glossary(keyword, glossary):
    """
    Search the glossary for terms or tools that match a keyword.

    Args:
        keyword (str): The keyword to search for.
        glossary (dict): The glossary dictionary containing terms and tools.

    Returns:
        dict: A dictionary containing matching terms and tools.
    """
    matches = {
        "terms": {k: v for k, v in glossary.get("terms", {}).items() if keyword.lower() in k.lower()},
        "tools": {k: v for k, v in glossary.get("tools", {}).items() if keyword.lower() in k.lower()}
    }
    return matches


def nmap_to_table(output):
    """
    Parse Nmap output to a list of lists for the table template.

    Args:
        output (str): The raw Nmap output.

    Returns:
        list: A list of lists containing parsed Nmap data.
    """
    rows = []
    for line in output.splitlines():
        if "open" in line or "closed" in line:
            parts = line.split()
            if len(parts) >= 4:  # Ensure we have enough columns
                port, service, version, status = parts[0], parts[1], " ".join(parts[2:-1]), parts[-1]
                rows.append([port, service, version, status])
    return rows


def generate_report(challenge_name, audited_by, challenge_dir, report_template):
    """
    Generate an HTML and PDF report based on the provided template.

    Args:
        challenge_name (str): The name of the challenge.
        audited_by (str): The name of the auditor.
        challenge_dir (str): The directory for the challenge.
        report_template (Template): The Jinja2 template for rendering the report.

    Returns:
        None
    """
    # Load tool data and glossary
    tool_data = load_tool_data(challenge_dir)
    glossary = load_glossary()

    # Context for the report
    context = {
        "challenge_name": challenge_name,
        "audited_by": audited_by,
        "date": datetime.now().strftime("%d %B %Y"),
        "tools": tool_data,
        "glossary": glossary
    }

    # Render the HTML report
    report_html = report_template.render(context)

    # Save the HTML report
    report_path = os.path.join(challenge_dir, f"{challenge_name}_report.html")
    with open(report_path, "w") as f:
        f.write(report_html)

    # Convert to PDF
    pdf_path = os.path.join(challenge_dir, f"{challenge_name}_report.pdf")
    pdfkit.from_file(report_path, pdf_path)

    print(f"Report generated: {pdf_path}")


def generate_htb_report():
    """
    Main function to prompt the user and generate a Hack The Box challenge report.

    Returns:
        None
    """
    # Prompt for input
    challenge_name = input("Enter the challenge name: ")
    audited_by = input("Enter the auditor's name: ")

    # Determine the base directory (with fallback)
    base_directory = load_config("base")
    challenge_dir = os.path.join(base_directory, challenge_name)

    # Ensure challenge directory exists
    if not os.path.exists(challenge_dir):
        os.makedirs(challenge_dir)
        print(f"Created challenge directory: {challenge_dir}")

    # Jinja2 setup
    templates_dir = 'templates'
    env = Environment(loader=FileSystemLoader(templates_dir))
    report_template = env.get_template('reports/hack-the-box-challenge.html')

    # Generate the report
    generate_report(challenge_name, audited_by, challenge_dir, report_template)