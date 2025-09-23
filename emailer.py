# to handle sending emails over a secure connection
import smtplib
import ssl
# to construct properly formatted email messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# to build date-specific filenames
import datetime
# to load environment variables from a local .env file (keeps credentials out of code)
from dotenv import load_dotenv
# for filesystem operations
import os
# to work with tabular job data
import pandas as pd

from scraper.config import EMAIL_RECIPIENT

# load .env variables
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")         # my Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")     # my Gmail App Password


def send_job_email():
    """
    Reads today's CSV of scraped jobs and emails it to the configured recipient.
    """
    today = datetime.date.today().isoformat()
    filepath = f"data/jobs_{today}.csv"

    # verify that a CSV file exists for today before proceeding
    if not os.path.exists(filepath):
        print(f"No CSV file found for {today}, skipping email.")
        return

    # load job postings into a DataFrame
    df = pd.read_csv(filepath)

    # build email body
    if df.empty:
        body = "No new jobs found today."
    else:
        # each job is listed with its title and link
        body = "\n\n".join([f"{row['title']}\n{row['link']}" for _, row in df.iterrows()])

    # create email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT
    msg["Subject"] = f"Daily Job Report - {today}"
    msg.attach(MIMEText(body, "plain"))

    # use secure SSL context (macOS certificates handled by default)
    context = ssl.create_default_context()

    try:
        # connect to Gmail's SMTP server securely
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        print(f"Email sent to {EMAIL_RECIPIENT} with {len(df)} jobs.")
    except smtplib.SMTPAuthenticationError:
        # authentication errors typically mean incorrect App Password setup
        print("SMTP Authentication failed. Make sure you are using a Gmail App Password.")
    except Exception as e:
        # catch-all for other unexpected errors
        print(f"An error occurred while sending email: {e}")


# allow script to be run independently for testing
if __name__ == "__main__":
    send_job_email()
