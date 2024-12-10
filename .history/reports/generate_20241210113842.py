import os
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

def generate_hack_the_box_report(challenge_name, audited_by, challenge_dir):
    """
    Generate a Hack The Box challenge report.
    """
    # Jinja2 setup
    templates_dir = 'templates'
    env = Environment(loader=FileSystemLoader(templates_dir))
    report_template = env.get_template('reports/hack-the-box-challenge.html')

    # Prompt for inputs
    challenge_name = input("Enter the challenge name: ")
    audited_by = input("Enter the auditor's name: ")
    challenge_dir = os.path.join("challenges", challenge_name)

    # Ensure challenge directory exists
    if not os.path.exists(challenge_dir):
        print(f"Challenge directory '{challenge_dir}' does not exist.")
        exit(1)

    # Load tool data
    tool_data = load_tool_data(challenge_dir)

    # Context for the report
    context = {
        "challenge_name": challenge_name,
        "audited_by": audited_by,
        "date": datetime.now().strftime("%d %B %Y"),
        "tools": tool_data
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

if __name__ == "__main__":
    

    # Generate the report
    generate_hack_the_box_report(challenge_name, audited_by, challenge_dir)