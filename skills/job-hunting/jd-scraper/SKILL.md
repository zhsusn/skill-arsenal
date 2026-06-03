---
name: jd-scraper
description: 当用户需要抓取招聘网站的职位描述（JD）时触发。支持 Indeed、Glassdoor、LinkedIn、BOSS直聘、猎聘、拉勾等平台，提供浏览器自动化、API聚合、反爬策略和数据标准化方案。适用于批量收集JD用于简历定制、求职分析或建立个人职位库。
---

# JD Scraper

## Purpose

Guide users through scraping job descriptions from major job boards. Covers browser automation, third-party APIs, anti-detection strategies, and data normalization. Outputs structured job data ready for downstream analysis or resume tailoring.

## Supported Portals

| Platform | Method | Difficulty | Login Required | Rate Limit |
|----------|--------|------------|----------------|------------|
| **Indeed** | Playwright / RapidAPI | ⭐⭐ Easy | No (public listings) | ~12% block with stealth |
| **Glassdoor** | Playwright + session | ⭐⭐⭐ Medium | Yes (for salaries/reviews) | ~15% block with stealth |
| **LinkedIn** | Phantombuster / Bright Data | ⭐⭐⭐⭐ Hard | Yes (high ban risk for DIY) | ~20% block; DIY not recommended |
| **BOSS直聘** | requests + Cookie / Puppeteer | ⭐⭐ Easy-Medium | Yes (Cookie required) | Aggressive captcha; 1-2s delay |
| **猎聘** | Puppeteer / Playwright | ⭐⭐⭐ Medium | Optional | Rotating proxy recommended |
| **拉勾** | Puppeteer / Playwright | ⭐⭐⭐ Medium | No | Moderate anti-bot |
| **Google for Jobs** | Indirect (aggregates above) | ⭐⭐⭐ Medium | No | Same as underlying source |

## Workflow

### Step 1: Define Scope

Ask the user:

1. **Which platforms?** (single or multiple)
2. **Search criteria:**
   - Keywords / job titles
   - Locations (city codes for BOSS, geo strings for Indeed)
   - Remote policy filters
   - Experience level
   - Date range (last 24h / 7d / 30d)
3. **Volume expectation:**
   - Quick scan (~10-50 listings)
   - Batch collection (~100-500 listings)
   - Continuous monitoring (scheduled polling)
4. **Output target:**
   - Markdown table for quick review
   - JSON / CSV for analysis pipeline
   - Direct input to `job-description-analyzer` skill

### Step 2: Select Strategy

**For one-time / low volume (< 50):**
- Recommend Chrome extension (Clura) or manual Playwright script.
- Lowest setup, ~4-5% block rate.

**For batch / medium volume (50-500):**
- Use Playwright + stealth plugins + residential proxies.
- Implement request jitter (1-3s random delays).

**For continuous / high volume (500+):**
- Recommend commercial scraping API (Scrapfly, Bright Data, Apify).
- Or RapidAPI Jobs Search for multi-platform aggregation.

**For China domestic platforms (BOSS/猎聘/拉勾):**
- BOSS: requests + login Cookie is fastest; Puppeteer fallback for captcha.
- 猎聘/拉勾: Puppeteer/Playwright with proxy rotation.

### Step 3: Generate Scraper Code

Provide platform-specific Python or Node.js code based on user selection. See `references/portal-guides.md` for copy-paste templates.

### Step 4: Normalize & Deduplicate

Standardize raw HTML into structured records:

```json
{
  "id": "normalized_hash",
  "source": "indeed|glassdoor|linkedin|boss|liepin|lagou",
  "title": "Job Title",
  "company": "Company Name",
  "location": "City, State / 城市",
  "salary_range": "$100K-$150K / 20K-35K·13薪",
  "employment_type": "Full-time|Contract|Intern",
  "remote_policy": "On-site|Hybrid|Remote",
  "posting_date": "2026-05-20",
  "description_raw": "Full JD text...",
  "requirements": ["Req 1", "Req 2"],
  "responsibilities": ["Resp 1", "Resp 2"],
  "skills_extracted": ["Python", "SQL", "AWS"],
  "apply_url": "https://...",
  "company_size": "100-499",
  "industry": "SaaS / 互联网",
  "scraped_at": "2026-06-02T08:00:00Z"
}
```

**Deduplication rules:**
- Primary key: `sha256(company + title + location)`
- Secondary check: fuzzy match on title + company name
- Update strategy: keep latest `posting_date` or `scraped_at`

### Step 5: Output & Handoff

- Save to `data/jobs_YYYY-MM-DD.json` or `.csv`
- Optionally invoke `job-description-analyzer` skill on collected JDs
- Summarize: total fetched, by source, duplicates dropped, errors encountered

## Portal-Specific Quick Reference

### Indeed (US/Global)

**Playwright (Python):**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # stealth works better non-headless
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
    )
    page = context.new_page()
    page.goto("https://www.indeed.com/jobs?q=Data+Engineer&l=San+Francisco%2C+CA")
    # Extract .jobTitle, .companyName, .jobMetaDataGroup, etc.
```

**Key points:**
- No login needed for basic listings
- URL pattern: `https://www.indeed.com/jobs?q={query}&l={location}&start={page*10}`
- Pagination via `start` parameter

### BOSS直聘 (China)

**requests approach (fastest):**
```python
import requests

headers = {
    "User-Agent": "Mozilla/5.0 ...",
    "Cookie": "lastCity=101010100; wt2=...; zp_at=...",  # login required
    "Referer": "https://www.zhipin.com/"
}
params = {
    "scene": 1,
    "query": "数据工程师",
    "city": "101010100",  # Beijing
    "page": 1,
    "pageSize": 30
}
resp = requests.get(
    "https://www.zhipin.com/wapi/zpgeek/search/joblist.json",
    headers=headers, params=params
)
jobs = resp.json()["zpData"]["jobList"]
```

**Key points:**
- Cookie must include `wt2` and `zp_at` (obtain after login)
- Detail page: `https://www.zhipin.com/job_detail/{encryptJobId}.html`
- Captcha triggers after ~50-100 rapid requests; add 1-2s delay
- City codes: Beijing=101010100, Shanghai=101020100, Shenzhen=101280600

### LinkedIn

**⚠️ Warning:** DIY scraping with Playwright/Selenium carries high account ban risk.

**Safer options:**
1. **Phantombuster** (pre-built LinkedIn scraper, cloud-run)
2. **Bright Data** / **Scrapfly** (managed proxy + unlocker)
3. **Apify Actor** (`gauravsaran/linkedin-indeed-glassdoor-job-scraper`)
4. **RapidAPI Jobs Search** (abstracts LinkedIn behind API)

If user insists on DIY: use throwaway account, residential proxy, human-like delays (5-15s), and accept ban risk.

### Glassdoor

- Login required for full JD and salary data
- CSRF token rotation complicates raw requests
- Playwright with `storage_state` persistence recommended
- Consider Bright Data / Scrapfly for production use

## Anti-Detection Checklist

- [ ] **Use real browser profile** (not headless, or stealth plugins like `puppeteer-extra-plugin-stealth`)
- [ ] **Rotate User-Agent** per session
- [ ] **Residential / mobile proxies** for high volume (avoid datacenter IP blocks)
- [ ] **Random delays** between requests (1-3s for BOSS, 3-8s for LinkedIn)
- [ ] **Session persistence** (save cookies, localStorage) to avoid re-login
- [ ] **Mouse movement simulation** for Puppeteer/Playwright on strict sites
- [ ] **Request fingerprint randomization** (viewport, fonts, WebGL)
- [ ] **Monitor block signals**: captcha pages, HTTP 403/429, redirect to login

## Data Processing Utilities

### JD Text Cleaning

1. Remove HTML tags (`BeautifulSoup` or regex)
2. Normalize whitespace (collapse multiple newlines/spaces)
3. Extract structured sections:
   - Split by common headers: "Requirements", "Responsibilities", "Qualifications", "About", "Benefits"
   - Use regex or LLM-based sectioning for messy JDs
4. Language detection (en/zh) for mixed platforms

### Skill Extraction

```python
# Simple keyword matching
TECH_KEYWORDS = ["Python", "SQL", "AWS", "Spark", "Hadoop", "Kafka", "Docker", "Kubernetes"]
# Or use LLM: "Extract required technical skills from the following JD..."
```

## Output Format

When delivering scraped results:

```markdown
# JD Scraping Report

## Query Parameters
- Platforms: Indeed, BOSS直聘
- Keywords: "Data Engineer", "数据工程师"
- Locations: San Francisco, CA / 北京
- Date range: Last 7 days

## Summary
| Metric | Count |
|--------|-------|
| Total fetched | 247 |
| Unique after dedup | 231 |
| Errors / blocks | 16 |
| By source | Indeed: 142, BOSS: 89 |

## Sample Records
| Title | Company | Location | Salary | Source |
|-------|---------|----------|--------|--------|
| ... | ... | ... | ... | ... |

## Files Generated
- `data/jobs_2026-06-02.json`
- `data/jobs_2026-06-02.csv`

## Next Steps
1. Run `job-description-analyzer` on collected JDs
2. Run `resume-tailor` for high-match positions
```

## Gotchas

- **Legal gray area**: Scraping publicly visible data is generally legal (hiQ v. LinkedIn), but violating a platform's ToS carries civil risk. Never resell scraped data or spam ATS systems.
- **LinkedIn bans accounts, not just IPs**: A banned LinkedIn account is hard to recover. Use commercial services or throwaway accounts for DIY.
- **BOSS直聘验证码**: After ~50 rapid requests, BOSS serves slider captchas. Slow down or switch to Puppeteer with captcha-solving service.
- **Cookie expiration**: BOSS `zp_at` and LinkedIn `li_at` cookies expire; refresh manually or automate login flow with 2FA handling.
- **Salary data is often hidden**: Many platforms (especially in China) show "薪资面议" or vague ranges. Extract what's available but don't hallucinate missing numbers.
- **Duplicate postings**: The same role may be posted by the company and by multiple recruiters. Deduplication is essential before analysis.
- **GDPR / privacy**: If storing JDs containing personal recruiter contact info, consider data retention policies.
