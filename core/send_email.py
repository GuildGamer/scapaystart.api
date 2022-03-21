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
    <body style="margin: auto; text-align: center; background-color: #FFFFFF; transition: 0.3s; padding: 5px 10px; color: #2d3092;">
        <p style="color: #2d3092;"> Hi {name},</p>
        <p style="color: #2d3092;"> Welcome to Scapay. We will be sending updates and news about Scapay to you. We hope you are as excited as we are for the journey ahead.</p>
       <img src="https://scapaystatic.fra1.digitaloceanspaces.com/welcome%20email.jpg">
       <p style="color: #2d3092;">
       <h3>What is Scapay?</h3>
       Scapay is a crypto currency liquidity solution that allows businesses receive payment in regular/fiat currency while allowing its customers spend their stable cryto coins.
       <p style="color: #2d3092;">follow our social media pages for more news on Scapay.</p>
       </p>
       <p>
       <a href="https://www.instagram.com/scapayofficial/"><img style="height: 24px;width: 24px;" src="https://scapaystatic.fra1.digitaloceanspaces.com/instagram.gif" alt="instagram"></a>
       <a href="https://twitter.com/scapayteam?t=A99rA5J6VEhuQonLpbxxXA&s=08"><img style="height: 24px;width: 24px;" src="https://scapaystatic.fra1.digitaloceanspaces.com/twitter.png" alt="twitter"></a>
       <a href="https://fb.me/scapayofficial"><img style="height: 24px;width: 24px;" src="https://scapaystatic.fra1.digitaloceanspaces.com/twitter.gif" alt="facebook"></a>
       </p>
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


def notification_email(recepient, name, waitlist_len) -> None:
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    message = MIMEMultipart("alternative")
    message["Subject"] = "The Waitlist Just Grew"
    # message["From"] = "scapayteam@gmail.com"
    message["To"] = recepient

    # Create the plain-text and HTML version of your message
    # text = f"""\

    # """
    html = f"""<p style="margin: auto; text-align: center; background-color: #FFFFFF; transition: 0.3s; padding: 5px 10px; color: #2d3092;"><b>{name}</b> joined the scapay waistlist! There are now <b>{waitlist_len}</b> people on the waitlist.</p>"""

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part1 = MIMEText(html, "html")

    # message.attach(part1)
    message.attach(part1)

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
