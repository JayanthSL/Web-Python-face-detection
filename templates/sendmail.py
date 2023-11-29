import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

port = 587
EMAIL_SERVER = "outlook.com"  
current_dir = Path(__file__).resolve().parent if "file_" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
sender_password = os.getenv("PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

def send_email(subject, receiver_email, message, attachment_path=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Attendance", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(message)

    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            msg.add_attachment(
                attachment.read(),
                maintype='application',
                subtype='octet-stream',
                filename=os.path.basename(attachment_path)
            )

    with smtplib.SMTP(EMAIL_SERVER, port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
   
    subject = "Attendance Report"
    message = """
    Hello ,
    Find your Attendance Report below here..
    Best regards,
    Your Name
    """
    attachment_path = 'Attendance.csv'  
    send_email(subject, receiver_email, message, attachment_path)

   
