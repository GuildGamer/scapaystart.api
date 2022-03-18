import smtplib, ssl
from decouple import config

from .Google import Create_Service
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()


def send_email(recepient, name) -> None:
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    message = MIMEMultipart("alternative")
    message["Subject"] = "A Scapay Welcome"
    # message["From"] = "scapayteam@gmail.com"
    message["To"] = recepient

    # Create the plain-text and HTML version of your message
    # text = f"""\

    # """
    html = f"""\
    <html>
    <body style="margin: auto; text-align: center; background-color: white; transition: 0.3s; padding: 5px 10px; color: #2d3092;">
        <p> Hi {name},</p>
        <p> Welcome to Scapay. We will be sending updates and news about Scapay to you. We hope you're as excited as we are for the journey ahead.</p>
       <img src="https://scapaystatic.fra1.digitaloceanspaces.com/Scapay.jpg">
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # message.attach(part1)
    message.attach(part2)

    raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message = (
        service.users()
        .messages()
        .send(
            userId="me",
            body={"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()},
        )
        .execute()
    )
    print(message)
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    # with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     server.login("scapayteam@gmail.com", password)
    # server.sendmail("scapayteam@gmail.com", recepient, message.as_string())
