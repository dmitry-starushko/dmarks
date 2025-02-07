from django.core.mail import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings
import os


def send_email(send_to, subject, body, attachment_path=None):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=send_to
    )

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            mime_obj = MIMEBase('application', 'octet-stream')
            mime_obj.set_payload(f.read())
            encoders.encode_base64(mime_obj)
            mime_obj.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
            email.attach(mime_obj)

    try:
        email.send()
    except Exception as e:
        print(e)
