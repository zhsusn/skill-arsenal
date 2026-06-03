# Portal Scraper Guides

> Copy-paste templates for each supported job board.

## Indeed

### Python + Playwright

```python
from playwright.sync_api import sync_playwright
import json

def scrape_indeed(query, location, pages=3):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()
        for i in range(pages):
            start = i * 10
            url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={start}"
            page.goto(url)
            page.wait_for_selector(".jobTitle", timeout=10000)
            cards = page.query_selector_all(".slider_container .slider_item")
            for card in cards:
                title_el = card.query_selector("h2 a")
                title = title_el.inner_text() if title_el else ""
                company_el = card.query_selector("[data-testid='company-name']")
                company = company_el.inner_text() if company_el else ""
                jobs.append({"title": title, "company": company, "source": "indeed"})
        browser.close()
    return jobs
```

## BOSS直聘

### Python + requests (fast)

```python
import requests, time, random

COOKIE = "your_login_cookie_here"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": COOKIE,
    "Referer": "https://www.zhipin.com/"
}

def scrape_boss(keyword, city_code, max_pages=3):
    jobs = []
    for page in range(1, max_pages + 1):
        params = {"scene": 1, "query": keyword, "city": city_code, "page": page, "pageSize": 30}
        resp = requests.get("https://www.zhipin.com/wapi/zpgeek/search/joblist.json",
                           headers=HEADERS, params=params)
        data = resp.json().get("zpData", {}).get("jobList", [])
        if not data:
            break
        for job in data:
            jobs.append({
                "title": job.get("jobName"),
                "company": job.get("brandName"),
                "salary": job.get("salaryDesc"),
                "location": job.get("cityName"),
                "id": job.get("encryptJobId"),
                "source": "boss"
            })
        time.sleep(random.uniform(1, 2))
    return jobs
```

## LinkedIn (via Apify)

```python
import requests

APIFY_TOKEN = "your_apify_token"

def scrape_linkedin_apify(search_terms, location, max_results=50):
    url = f"https://api.apify.com/v2/acts/gauravsaran~linkedin-indeed-glassdoor-job-scraper/run-sync-get-dataset-items"
    payload = {
        "searchTerms": search_terms,
        "location": location,
        "maxResults": max_results,
        "sites": ["linkedin"]
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers,
                         params={"token": APIFY_TOKEN})
    return resp.json()
```

## RapidAPI (Multi-platform)

```python
import requests

RAPIDAPI_KEY = "your_key"

def rapidapi_jobs(query, location):
    url = "https://jobs-search-realtime-data-api.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jobs-search-realtime-data-api.p.rapidapi.com"
    }
    params = {"query": query, "location": location, "page": 1}
    resp = requests.get(url, headers=headers, params=params)
    return resp.json()
```
