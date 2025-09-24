# to schedule jobs at specific times/days
import schedule
# to pause between schedule checks
import time
# to generate timestamps for logging
import datetime

# import main workflow (scraping + emailing)
from main import main


def job():
    """
    Wrapper job that runs the main workflow:
    - Scrapes job postings
    - Saves them to a CSV file
    - Emails the results
    """
    print(f"[{datetime.datetime.now()}] Running scheduled job...")
    main()  # main() already scrapes and sends the email


def run_scheduler():
    """
    Sets up a scheduler that runs the job every Friday at 9:00 AM.
    Keeps the process alive and checks periodically for scheduled jobs.
    """
    # schedule the job for every Friday at 09:00
    schedule.every().friday.at("09:00").do(job)
    print("Scheduler started. Waiting for next Friday 09:00...")

    # infinite loop to keep the scheduler running
    while True:
        # check if any scheduled jobs need to run
        schedule.run_pending()
        # sleep for 60 seconds between checks
        time.sleep(60)


# allow script to be run independently
if __name__ == "__main__":
    run_scheduler()
