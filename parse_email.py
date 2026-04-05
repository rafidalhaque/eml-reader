from email import message, parser, policy, contentmanager, header
from pathlib import Path
from html.parser import HTMLParser

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

class StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return "".join(self.text).strip()

def strip_html(html):
    stripper = StripHTML()
    stripper.feed(html)
    return stripper.get_text()
