# the job-scraping function from scraper module
from scraper.scraper import scrape_category
# the target category URL from config file
from scraper.config import CATEGORY_URL

# pd to work with tabular job data
import pandas as pd
# datetime to generate date-stamped filenames
import datetime
# os for filesystem operations
import os


def main():
    """
    Main entry point of the script:
    - Scrapes job postings from the target We Work Remotely category
    - Saves the results as a date-stamped CSV file in the 'data' directory
    """
    print("Scraping We Work Remotely (Full-Stack category)...")

    # scrape jobs from configured category URL
    jobs = scrape_category(CATEGORY_URL)

    # if no jobs were found, exit early
    if not jobs:
        print("No jobs found.")
        return

    # convert the scraped list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(jobs)

    # generate a date string (YYYY-MM-DD) for the filename
    today = datetime.date.today().isoformat()

    # ensure the 'data' directory exists (create if necessary)
    os.makedirs("data", exist_ok=True)

    # build the output filepath with today's date
    filepath = f"data/jobs_{today}.csv"

    # save DataFrame as a CSV file without the index column
    df.to_csv(filepath, index=False)

    # log success message with the number of jobs saved
    print(f"Saved {len(df)} jobs to {filepath}")


# run main() only if this script is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
