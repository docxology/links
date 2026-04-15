# src/scrapers/

Stage 2: web scraping with caching.

## Primary Module

[`scrape_sites.py`](scrape_sites.py) — loads organized links, fetches pages (with `cached_data/` cache), extracts meaningful content using BeautifulSoup, writes `data/scraped_data.json` and text extracts.

Uses `REQUEST_TIMEOUT` and `MAX_CONCURRENT_REQUESTS` (hard-coded 5) from [`../utils/config.py`](../utils/config.py).

See root [`../../README.md`](../../README.md) for pipeline context and [`../AGENTS.md`](../AGENTS.md) for technical details.

Tested in unit and integration suites. Use `--skip-scrape` to reuse cached data.
