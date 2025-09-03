# requests to send HTTP requests
import requests
# bs4 to pull data from HTML and XML files
from bs4 import BeautifulSoup

# HTTP request headers to mimic a real browser and avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# base domain for We Work Remotely
BASE_URL = "https://weworkremotely.com"
