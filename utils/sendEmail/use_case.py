
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from datetime import date
from dotenv import load_dotenv
import json
import ssl
import os

# Load environment variables from the .env file
load_dotenv()

# SMTP server configuration
__SMTP_SERVER = os.getenv("SMTP_SERVER")
__PORT = int(os.getenv("PORT"))
__SENDER_EMAIL = os.getenv("SENDER_EMAIL")
__PASSWORD = os.getenv("PASSWORD")

# Parse the email lists from the environment variables.
# The variables should be JSON-formatted strings.
try:
    __SUPORTE_EMAIL = json.loads(os.getenv("SUPORTE_EMAIL"))
except Exception as e:
    print("Error parsing SUPORTE_EMAIL, using raw value instead.", e)
    __SUPORTE_EMAIL = os.getenv("SUPORTE_EMAIL")

try:
    __SUCCESS_EMAIL = json.loads(os.getenv("SUCCESS_EMAIL"))
except Exception as e:
    print("Error parsing SUCCESS_EMAIL, using raw value instead.", e)
    __SUCCESS_EMAIL = os.getenv("SUCCESS_EMAIL")

# Get today's
today = date.today().strftime("%d/%m/%Y")

def send_mail_atualization(result):

    # Determine recipient(s) based on the result value
    if result == 'sucess_login':
        receiver_email = __SUCCESS_EMAIL
    else:
        receiver_email = __SUPORTE_EMAIL

    print(f"Sending email to: {receiver_email}")

    smtp_server = __SMTP_SERVER
    port = __PORT
    sender_email = __SENDER_EMAIL
    password = __PASSWORD

    # Create an SSL context for a secure connection
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server and log in
        server = SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)

        # Create the email message container (multipart/related)
        message = MIMEMultipart('related')
        message["Subject"] = f"Extranet atualization - {today}"
        message["From"] = sender_email

        # Set the "To" header: if receiver_email is a list, join the addresses; if a string, use directly.
        if isinstance(receiver_email, list):
            message["To"] = ", ".join(receiver_email)
        else:
            message["To"] = receiver_email

        # Build the HTML body of the email based on the result
        html = "<html><body>"
        if result == 'sucess_login':
            html += (
                "Dear all, <br><br>"
                "The Extranet update has been successfully completed!<br><br>"
                "</body></html>"
            )
        else:
            html += (
                "Dear all, <br><br>"
                "An issue occurred during the Extranet update. Please contact the Support team.<br><br>"
                "</body></html>"
            )

        # Attach the HTML body to the message
        part2 = MIMEText(html, "html")
        message.attach(part2)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
               
    except Exception as e:
        print("An error occurred:", e)
    finally:
        server.quit()
        