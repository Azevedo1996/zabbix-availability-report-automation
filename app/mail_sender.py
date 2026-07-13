from email.message import EmailMessage
from pathlib import Path


def build_message(mail_from, mail_to, mail_cc, subject, body, attachment):
    message = EmailMessage()
    message["From"] = mail_from
    message["To"] = mail_to
    if mail_cc:
        message["Cc"] = mail_cc
    message["Subject"] = subject
    message.set_content(body)

    attachment = Path(attachment)
    message.add_attachment(
        attachment.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=attachment.name,
    )
    return message


def save_eml(message, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(bytes(message))
    return output_path
