import os
from smtplib import SMTP
from email.message import EmailMessage


class NotificationManager:
    def __init__(self):
        self.myemail = os.environ["EMAIL"]
        self.password = os.environ["EMAIL_PASSWORD"]

    def send_emails(self, emails, message_body):
        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(
                user=self.myemail,
                password=self.password
            )

            for email in emails:
                msg = EmailMessage()
                msg["Subject"] = "Flight Notification"
                msg["From"] = self.myemail
                msg["To"] = email
                msg.set_content(message_body)

                connection.send_message(msg)
                print(f"Email sent successfully to {email}.")
