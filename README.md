# 👩‍💻 Job Postings Scraper

Tired of searching for jobs manually? This scraper automates the process by gathering IT job listings from We Work Remotely, filtering them by the full-stack category, saving them to a CSV, and delivering the results straight to your inbox at 9:00 every Friday.

---

## 🔍 Features

- Scrapes job titles and links from We Work Remotely
- Filters postings by the full-stack category
- Saves results to timestamped `.csv` files for easy tracking
- Sends job lists via email on a weekly schedule
- Flexible scheduling using `schedule` (Python) or system tools (cron, Task Scheduler)

---

## 📂 Project Structure

- **`main.py`** → Orchestrates the whole workflow (scrape → filter → save → email)  
- **`scraper.py`** → Fetches job postings from WWR and applies category filter 
- **`emailer.py`** → Handles SMTP setup and sends out the CSV file with job listings  
- **`scheduler.py`** → Automates the job run on a weekly basis  

---

## ⚙️ Installation

Clone the repository:
   ```bash
   git clone https://github.com/britney-petrova/job-postings-scraper.git
   cd job-postings-scraper
