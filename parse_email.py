from email import message, parser, policy, contentmanager, header
from pathlib import Path
from html.parser import HTMLParser
import html as html_lib
from ui_design import ToplevelWindow


class StripHTML(HTMLParser):
    """
    deprecated
    Strip HTML tags into a single string
    """
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return "".join(self.text).strip()

def strip_html(html):
    """
    Deprecated
    function to return stripped html
    """
    stripper = StripHTML()
    stripper.feed(html)
    return stripper.get_text()


def parse_email(file):
    with open(file, "rb") as f:
        eml_data = parser.BytesParser(policy=policy.default).parse(f)

    get_plain_body = eml_data.get_body(preferencelist=("plain", ))
    get_html_body = eml_data.get_body(preferencelist=("html", ))

    html_body = get_html_body.get_content() if get_html_body else None
    plain_body = get_plain_body.get_content() if get_plain_body else None

    if not html_body and plain_body:
        html_body = f"<pre>{html_lib.escape(plain_body)}</pre>"

    if not html_body:
        html_body = "<p><em>No body exists.</em></p>"

    attachments = []
    for attachment in eml_data.walk():
        filename = attachment.get_filename()
        if filename is None:
            continue
        payload = attachment.get_payload(decode=True)
        filesize = len(payload) if payload else 0
        attachments.append((filename, filesize))

    return {
        "subject": str(eml_data["Subject"] or ""),
        "from": str(eml_data["From"] or ""),
        "to": str(eml_data["To"] or ""),
        "date": str(eml_data["Date"] or ""),
        "body_html": html_body,
        "body_plain": plain_body or "",
        "attachments": attachments,
    }
