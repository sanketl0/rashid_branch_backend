import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
try:
    from django.conf import settings
except ImportError:
    pass


class AutomatedEmail:
    """Class for Email"""

    def __init__(self, sent_from, sent_to):
        """ 
        sent_from: Name of the person who is sending email
        sent_to: Email of the person to whom email will be sent
        """
        self.message = MIMEMultipart("alternative")
        self.message["From"] = self.sent_from = sent_from
        self.sent_to = sent_to
        if isinstance(self.sent_to, (list, tuple)):
            self.message["To"] = ", ".join(self.sent_to)
        elif isinstance(self.sent_to, str):
            self.message["To"] = self.sent_to
        else:
            raise ValueError

        self.user_email = None
        self.password = None

        self.ssl_host = 'email-smtp.us-east-1.amazonaws.com'
        self.ssl_port = 587
        self.is_ssl_set = False

    def add_subject(self, subject):
        """Add the subject to the email"""
        self.message["Subject"] = subject

    def set_login_details(self, user_email, password):
        """ Email will be send by using the following details """
        self.user_email = user_email
        self.password = password

    def set_smtp_ssl(self, ssl_host, ssl_port):
        self.ssl_host = ssl_host
        self.ssl_port = ssl_port
        self.is_ssl_set = True

    def add_alternative_text(self, text):
        """Add alternative text, just in case HTML doesn't gets rendered."""
        part1 = MIMEText(text, "plain")
        self.message.attach(part1)

    def add_html(self, html):
        """ Add HTML to the email"""
        part2 = MIMEText(html, "html")
        self.message.attach(part2)

    def send(self):
        """ Finally login and send the mail"""
        # Create a secure SSL context
        smtp_server =os.environ.get('SMTP_SERVER')
        smtp_port = 587  # For SSL use 465, for TLS use 587
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            print(f"email sent to {self.sent_to}")
            server.sendmail(self.sent_from, self.sent_to, self.message.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(e)
            print(f"Failed to send email. Error: {e}")

class HTMLPage:

    def __init__(self, html_path):
        self.html_path = html_path
        self.text = None

    def read_page(self):
        with open(self.html_path, 'r') as html:
            html_text = html.read()
        self.text = html_text

    def format_page(self, **kwargs):
        if self.text:
            self.text = self.text.format(**kwargs)
        else:
            raise Exception("Call read_page() first")

    def get_text(self):
        return self.text


def send_activation_email(user, user_email, activation_link):
    sent_from = os.environ.get("SMTP_EMAIL")
    sent_to = user_email

    email = AutomatedEmail(sent_from, sent_to)
    # email.set_smtp_ssl(ssl_host="smtp.hostinger.com", ssl_port=465)
    email.add_subject("AutoCount Activation Link")
    # email.set_login_details(user_email=sent_from, password=sent_from_password)

    link = activation_link
    text = f"""
    Hi , This is the alternative text if HTML Doesn't gets rendered.
    Here is your activation link
    {link}
    """
    html_path = os.path.join(settings.BASE_DIR, 'registration','templates', 'activation_email_template.html')
    html = HTMLPage(html_path)
    html.read_page()
    html.format_page(UserName=user, ActivationLink=link)

    email.add_alternative_text(text)
    email.add_html(html.get_text())

    email.send()


def send_forgot_password_link(username, link_with_passcode):
    # Harcoded login details

    sent_from = os.environ.get("SMTP_EMAIL")
    sent_from_password =  "ql@o4_9uRiK"
    sent_to = username

    email = AutomatedEmail(sent_from, sent_to)
    # email.set_smtp_ssl(ssl_host="smtp.hostinger.com", ssl_port=465)
    email.add_subject("AutoCount forgot password link")
    # email.set_login_details(user_email=sent_from, password=sent_from_password)

    text = f"""
    Hi , This is the alternative text if HTML Doesn't gets rendered.
    Here is your activation link
    {link_with_passcode}
    """

    html_path = os.path.join(settings.BASE_DIR, 'registration','templates', 'password_reset_link_email.html')
    html = HTMLPage(html_path)
    html.read_page()
    html.format_page(UserName=username, ActivationLink=link_with_passcode)

    email.add_alternative_text(text)
    email.add_html(html.get_text())

    email.send()
    print(link_with_passcode)