import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from weasyprint import HTML

def load_sample_data():
    """
    Load sample tool output data for generating the report.
    """
    return {
        "title": "Ethical Hacking Report",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "audited_by": input("Enter the auditor's name: "),
        "website": input("Enter the audited website: "),
        "introduction": "This report summarises the findings from the penetration test conducted on the target system.",
        "summary_findings": [
            {"title": "Open Ports", "description": "10 open ports detected.", "chart": None},
            {"title": "Vulnerable Forms", "description": "2 XSS vulnerabilities detected.", "chart": None},
            {"title": "Directory Enumeration", "description": "Sensitive directories found.", "chart": None}
        ],
        "tools": [
            {
                "name": "nmap",
                "title": "Nmap Scan",
                "description": "Nmap was used to identify open ports and running services.",
                "template": "tools/nmap.html",
                "rows": [
                    {"port": "80", "status": "open", "service": "http", "version": "Apache 2.4.46"},
                    {"port": "443", "status": "open", "service": "https", "version": "nginx 1.18.0"}
                ]
            },
            {
                "name": "nikto",
                "title": "Nikto Web Server Scan",
                "description": "Nikto identified potential misconfigurations and vulnerabilities.",
                "template": "tools/nikto.html",
                "rows": [
                    {"finding": "Server leaks information via ETag headers.", "severity": "medium"},
                    {"finding": "Outdated Apache version detected.", "severity": "high"}
                ]
            },
            {
                "name": "gobuster",
                "title": "Directory Enumeration",
                "description": "Gobuster discovered hidden directories and files.",
                "template": "tools/gobuster.html",
                "rows": [
                    {"directory": "/admin", "status": "403 Forbidden"},
                    {"directory": "/backup", "status": "200 OK"}
                ]
            }
        ],
        "services": [
            {
                "name": "Web Application Security",
                "description": "Comprehensive security assessments for web applications.",
                "image": "images/web_security.png",
                "link": "https://mediawolf.co.uk?utm_source=report&utm_medium=pdf&utm_campaign=security_audit"
            },
            {
                "name": "Network Security",
                "description": "In-depth analysis of network configurations and security.",
                "image": "images/network_security.png",
                "link": "https://mediawolf.co.uk?utm_source=report&utm_medium=pdf&utm_campaign=network_security"
            }
        ]
    }

def render_report(data, output_dir="reports/InspectorGadget"):
    """
    Render the report as HTML and PDF.

    Args:
        data (dict): The data for rendering the report.
        output_dir (str): The directory to save the rendered report.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load Jinja2 environment
    env = Environment(loader=FileSystemLoader("reports/templates"))
    template = env.get_template("base.html")

    # Render HTML
    html_content = template.render(data)
    html_file = os.path.join(output_dir, "report.html")
    with open(html_file, "w") as f:
        f.write(html_content)
    print(f"HTML report generated: {html_file}")

    # Render PDF
    pdf_file = os.path.join(output_dir, "report.pdf")
    HTML(string=html_content).write_pdf(pdf_file)
    print(f"PDF report generated: {pdf_file}")

if __name__ == "__main__":
    sample_data = load_sample_data()
    render_report(sample_data)