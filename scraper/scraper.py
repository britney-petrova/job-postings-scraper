# to send HTTP requests
import requests
# to pull data from HTML and XML files
from bs4 import BeautifulSoup
# for cleaning up URL slugs
import re

# HTTP request headers to mimic a real browser and avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# base domain for We Work Remotely (WWR)
BASE_URL = "https://weworkremotely.com"


def format_title_from_url(url: str) -> str:
    """
    Derive a readable job title from the job posting URL slug.

    Args:
        url (str): The job posting URL (relative, e.g. "/remote-jobs/company-job-title")

    Returns:
        str: A formatted job title (e.g. "Company Job Title")
    """
    # take last part of URL
    slug = url.rstrip("/").split("/")[-1]
    # remove leading numbers if present
    slug = re.sub(r"^\d+-", "", slug)
    # replace dashes with spaces, capitalize
    return slug.replace("-", " ").title()


def scrape_category(category_url):
    """
    Scrape job postings from a specific We Work Remotely category page.

    Args:
        category_url (str): Full URL of the WWR category page.

    Returns:
        list[dict]: A list of job postings. Each job is represented as a dictionary with keys:
                    - 'title' (str): Job title derived from the URL
                    - 'link'  (str): Full URL to the job posting
    """
    # send GET request to category page
    response = requests.get(category_url, headers=HEADERS)
    # raise an exception if the request failed
    response.raise_for_status()

    # parse the HTML response with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # empty list to hold all scraped job postings
    jobs = []

    # job listings are grouped inside <section class="jobs">
    # each job is represented as an <li> element (with or without the "feature" class)
    listings = soup.select("section.jobs li")

    # iterate through every <li> job listing previously extracted
    for li in listings:
        # find the job posting link (<a>) whose href begins with "/remote-jobs/"
        anchor = li.select_one("a[href^='/remote-jobs/']")
        # skip this <li> if no valid job link is found
        if not anchor:
            continue

        # extract the relative job URL (remove any tracking query parameters after '?')
        relative_url = anchor["href"].split("?")[0]

        # build the full absolute URL by combining BASE_URL with the relative path
        full_url = BASE_URL + relative_url

        # append the job entry to the jobs list
        # title is derived from the URL itself using a helper function
        jobs.append({
            # readable title parsed from URL
            "title": format_title_from_url(relative_url),
            # absolute job posting URL
            "link": full_url
        })

    return jobs
