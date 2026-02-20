# Quotes to Scrape – Web Scraping Assessment

**Betternship – Python Web Scraping Task**

---

## Overview

This project scrapes quote and author data from:
[https://quotes.toscrape.com](https://quotes.toscrape.com)

The scraper:

- Crawls all paginated quote pages
- Visits each author profile page
- Extracts structured fields
- Logs development progress and crawl activity

Implemented in **Python** using **Scrapy**.

---

## Data Fields

**Quote Pages:** quote text, author name, tags

**Author Pages:** full name, date of birth, place of birth

---

## Technical Approach

### Framework Choice: Scrapy

- Built-in pagination & crawling
- Async request handling
- Request → response → callback workflow
- Logging & duplicate filtering

### Pagination & Author Navigation

- Recursively followed "Next" page links with `response.follow()`
- Passed quote data via `meta` to author pages
- Merged author data in `parse_author()`
- Used `dont_filter=True` to handle duplicate URLs

### Logging

- Append-mode logs with timestamps (`scraping_progress.log`)
- Tracked page visits, quote discovery, author processing

---

## Challenges & Solutions

### 1️⃣ Spider Returning Zero Pages

- **Cause:** Network issue
- **Fix:** Ensure internet connection before running the spider

### 2️⃣ 308 Redirects & HTTP vs HTTPS

- **Cause:** Inconsistent caching & redirects
- **Fix:** Temporarily tested with HTTP, finalized with HTTPS

### 3️⃣ robots.txt Confusion

- **Cause:** workstation not connected to internet
- **Fix:** Set `ROBOTSTXT_OBEY = True` (safe for this sandbox)

### 4️⃣ Incomplete Results

- **Cause:** Scrapy's default duplicate request filtering
- **Fix:** `dont_filter=True` ensures all quote-author relationships are processed

---

## Output

Final dataset: **`quotes_clean.csv`**

Each record contains:

```json
{
  "quote_text": "...",
  "author_name": "...",
  "tags": [...],
  "author_full_name": "...",
  "date_of_birth": "...",
  "place_of_birth": "..."
}
```

---

## Improvements (If More Time)

- Cache author data instead of using `dont_filter=True`
- Implement validation pipelines
- Structured logging & unit tests
- Docker containerization for reproducibility

---

## How to Run

From the project root (where `scrapy.cfg` is located):

```bash
scrapy crawl quotesclean
```

---

## Assumptions

- Site structure remains consistent
- No authentication or CAPTCHA required
- Publicly accessible sandbox site

---

## Project Structure

```
quotes_project/
│
├── quotes_project/
│   ├── spiders/
│   │   ├── quotefirstpag.py
│   │   └── quotesclean.py
│
├── scraping_progress.log
├── quotes.json
├── README.md
├── requirements.txt
└── scrapy.cfg
```
