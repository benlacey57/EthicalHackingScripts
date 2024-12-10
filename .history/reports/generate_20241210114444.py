import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pdfkit

def load_tool_data(challenge_dir):
    """
    Load tool output files from the challenge directory.
    Each file is named after a tool (e.g., nmap.txt, nikto.txt).
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
    """
    with open('glossary.json', 'r') as f:
        glossary = json.load(f)
    return glossary

def search_glossary(keyword, glossary):
    """
    Search the glossary for terms or tools that match a keyword.
    """
    matches = {
        "terms": {k: v for k, v in glossary.get("terms", {}).items() if keyword.lower() in k.lower()},
        "tools": {k: v for k, v in glossary.get("tools", {}).items() if keyword.lower() in k.lower()}
    }
    return matches

def nmap_to_table(output):
    """
    Parse Nmap output to a list of lists for the table template.
    """
    rows = []
    for line in output.splitlines():
        if "open" in line or "closed" in line:
            parts = line.split()
            if len(parts) >= 4:  # Ensure we have enough columns
                port, service, version, status = parts[0], parts[1], " ".join(parts[2:-1]), parts[-1]
                rows.append([port, service, version, status])
    return rows

def generate_htb_report():
    """
    Main function to generate a Hack The Box report.
    """
    # Prompt for input
    challenge_name = input("Enter the challenge name: ")
    audited_by = input("Enter the auditor's name: ")
    challenge_dir = os.path.join("challenges", challenge_name)

    # Ensure challenge directory exists
    if not os.path.exists(challenge_dir):
        print(f"Challenge directory '{challenge_dir}' does not exist.")
        exit(1)

    # Jinja2 setup
    templates_dir = 'templates'
    env = Environment(loader=FileSystemLoader(templates_dir))
    report_template = env.get_template('reports/hack-the-box-challenge.html')

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

    # Render the HTML
    report_html = report_template.render(context)

    # Save the HTML report
    report_path = os.path.join(challenge_dir, f"{challenge_name}_report.html")
    with open(report_path, "w") as f:
        f.write(report_html)

    # Convert to PDF
    pdf_path = os.path.join(challenge_dir, f"{challenge_name}_report.pdf")
    pdfkit.from_file(report_path, pdf_path)

    print(f"Report generated: {pdf_path}")