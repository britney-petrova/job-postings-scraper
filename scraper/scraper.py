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

    # create a list that will contain the filtered jobs
    jobs = []

    # each section with class "jobs" contains job listings
    sections = soup.find_all("section", class_="jobs")

    for section in sections:
        # job postings are inside <li> tags with class "feature"
        listings = section.find_all("li", class_="feature")

        for job in listings:
            anchor = job.find("a", href=True)
            if not anchor:
                continue  # skip if no link found (malformed listing)

            # extract company name, job title, and job link
            company = job.find("span", class_="company")
            title = job.find("span", class_="title")
            link = BASE_URL + anchor["href"]

            # add job to the list of filtered jobs
            jobs.append({
                # return "N/A" if company or job title is missing
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "link": link
            })

    return jobs
