from email import message, parser, policy, contentmanager, header
from pathlib import Path

project_root = Path(__file__).parent

def parse_email(file):
    with open(file, "rb") as f:
        eml_data = parser.BytesParser(policy=policy.default).parse(f)

    body = eml_data.get_body(preferencelist=("plain", "html"))

    return {
        "subject": eml_data["Subject"],
        "from": eml_data["From"],
        "to": eml_data["To"],
        "date": eml_data["Date"],
        "body": body.get_content() if body else "No body exists"
    }