# Quotes to Scrape – Web Scraping Assessment

**Betternship – Python Web Scraping Task**

---

## Overview

This project scrapes quote and author data from:
[https://quotes.toscrape.com/](https://quotes.toscrape.com/)

The scraper:

- Crawls all paginated quote pages
- Visits each author profile page
- Extracts required structured fields
- Logs development progress and crawl activity

The project was implemented using **Python** and **Scrapy**.

---

## Required Data Fields

### From Quote Pages

- Quote text
- Author name
- Tags

### From Author Pages

- Author full name
- Date of birth
- Place of birth

---

## Technical Approach

### Framework Choice

I used **Scrapy** because:

- Built-in support for pagination and crawling
- Asynchronous request handling
- Structured request → response → callback workflow
- Built-in logging and duplicate request filtering

### Pagination Handling

Pagination was handled by:

- Extracting the **"Next"** button link
- Using `response.follow()` recursively
- Stopping when no next page exists

This ensured all quote pages were captured.

### Author Page Navigation

Each quote links to an author profile page.

To merge quote and author data:

- Passed quote data through the **meta** dictionary
- Followed the author link using `response.follow()`
- Combined author data with quote data in `parse_author`

This ensured each output record contains both quote and author metadata.

---

## Challenges Encountered

### 1️⃣ Spider Returning Zero Pages

Initially, the spider returned:

```
Crawled 0 pages
Scraped 0 items
```

**Root cause:** Internet connectivity issue.
Once network connectivity was restored, crawling worked normally.

> **Lesson:** Always verify network availability when debugging scraping failures.

---

### 2️⃣ 304 / 308 Redirect & HTTP vs HTTPS Confusion

- Encountered `304 Not Modified` responses
- Redirect behavior between HTTP and HTTPS caused inconsistent crawling

Initially, using HTTPS returned unexpected responses. Switching temporarily to:

```python
start_urls = ["http://quotes.toscrape.com/"]
```

helped isolate the issue. Ultimately, using:

```python
start_urls = ["https://quotes.toscrape.com/"]
```

with correct settings resolved the issue.

> **Lesson:** Understand Scrapy's handling of redirects, caching, and status codes.

---

### 3️⃣ robots.txt Confusion

With:

```python
ROBOTSTXT_OBEY = True
```

the spider appeared to behave inconsistently because the site's `robots.txt` returned a `404`.

**Solution:**

```python
ROBOTSTXT_OBEY = False
```

For this sandbox site, it was safe to disable robots.txt enforcement.

---

### 4️⃣ Incomplete Results Due to Duplicate Filtering

Some author pages were not revisited due to Scrapy's default duplicate request filtering.

**Solution:**

```python
response.follow(author_link, callback=self.parse_author, meta=meta, dont_filter=True)
```

This ensured:

- Every quote-author relationship was processed
- Author data was correctly attached to each quote
- No records were dropped due to duplicate URL filtering

---

### 5️⃣ Development Logging

Implemented logging to document development and provide traceability:

- Logs written in append mode
- Each run recorded with timestamps
- Logged: page visits, quote discovery, author processing
- Log file: `scraping_progress.log`

This allows reviewers to inspect crawl behavior and verify development steps.

---

## Output

The final dataset is exported as: **`quotes_clean.csv`**

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

## Improvements (If Given More Time)

- Deduplicate author requests intelligently
- Normalize dates into ISO format
- Implement Item Pipelines for validation and cleaning
- Add structured logging configuration
- Add unit tests for XPath extraction
- Containerize using Docker for reproducibility

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
