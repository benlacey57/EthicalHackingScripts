import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def generate_report(tool_name, output_file, raw_output, extra_context=None):
    """
    Generates an HTML report for a specific tool using Jinja2 templates.

    Args:
        tool_name (str): The name of the tool (e.g., 'nmap').
        output_file (str): Path to save the generated report.
        raw_output (str): Raw output from the tool to include in the report.
        extra_context (dict): Additional context to pass to the template.
    """
    # Load definitions
    definitions_file = os.path.join("reports", "templates", "definitions.json")
    with open(definitions_file, "r") as f:
        definitions = json.load(f)

    # Get tool-specific details
    tool_info = definitions.get(tool_name, {})
    tool_title = tool_info.get("title", "Tool Report")
    tool_description = tool_info.get("description", "No description available.")

    # Load Jinja2 environment
    env = Environment(loader=FileSystemLoader("reports/templates"))
    template = env.get_template(f"tools/{tool_name}.html")

    # Render template
    rendered_html = template.render(
        title=tool_title,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tool_title=tool_title,
        tool_description=tool_description,
        tool_output=raw_output,
        **(extra_context or {})
    )

    # Save the report
    with open(output_file, "w") as f:
        f.write(rendered_html)
    print(f"Report generated: {output_file}")

    