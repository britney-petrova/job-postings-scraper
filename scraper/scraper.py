# requests to send HTTP requests
import requests
# bs4 to pull data from HTML and XML files
from bs4 import BeautifulSoup

# HTTP request headers to mimic a real browser and avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# base domain for We Work Remotely (WWR)
BASE_URL = "https://weworkremotely.com"


def scrape_category(category_url):
    """
    Scrape job postings from a specific We Work Remotely category page.

    Args:
        category_url (str): Full URL of the WWR category page
                                (e.g. "https://weworkremotely.com/categories/remote-full-stack-programming-jobs").

    Returns:
        list[dict]: A list of job postings. Each job is represented as a dictionary with keys:
                    - 'title'   (str): Job title
                    - 'company' (str): Company name
                    - 'link'    (str): Full URL to the job posting
    """
    # send GET request to category page
    response = requests.get(category_url, headers=HEADERS)
    response.raise_for_status()  # raise an exception if the request failed

    # parse the HTML response with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # find all job postings directly
    listings = soup.select("li.feature a[href^='/remote-jobs/']")

    # create a list that will contain the filtered jobs
    jobs = []

    # loop through all <a> tags inside <li class="feature"> elements
    # that link to individual remote job postings
    for anchor in soup.select("li.feature a[href^='/remote-jobs/']"):
        # extract the company name if present
        company = anchor.find("span", class_="company")
        # extract the job title if present
        title = anchor.find("span", class_="title")

        # append the job posting to the jobs list as a dictionary
        jobs.append({
            "title": title.text.strip() if title else "N/A",  # job title (fallback "N/A")
            "company": company.text.strip() if company else "N/A",  # company name (fallback "N/A")
            "link": BASE_URL + anchor["href"]  # job posting URL
        })

    return jobs
