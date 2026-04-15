# `src/scrapers/` agent notes

## Module

[`scrape_sites.py`](scrape_sites.py):

- `load_organized_links()` — from `ORGANIZED_LINKS_PATH`
- `scrape_url(url)` — GET with disk cache in `cached_data/`, timeout from `REQUEST_TIMEOUT`
- `scrape_links(organized_links)` — concurrent (limited concurrency), per-category cap (20 in code)
- `extract_meaningful_content(soup)` — headings, paragraphs, lists, metadata using BeautifulSoup
- `main()` — orchestrates load → scrape → save to `SCRAPED_DATA_PATH` + text extract files

## Contracts

- Input from stage 1 (`data/organized_links.json`).
- Output shape: dict of category → list of document dicts (`url`, `title`, `status`, `content`).
- Cache keys are host/path based; stale cache can be cleared manually or by deleting `cached_data/`.

## Configuration

`SCRAPED_DATA_PATH`, `CACHE_DIR`, `REQUEST_TIMEOUT`, `MAX_CONCURRENT_REQUESTS=5` from [`../utils/config.py`](../utils/config.py).

## Tests

- Unit: [`../../tests/unit/test_scrapers_scrape_sites.py`](../../tests/unit/test_scrapers_scrape_sites.py)
- Integration: `tests/integration/test_pipeline.py`

See [`../AGENTS.md`](../AGENTS.md) and root pipeline docs. Do not edit cached or scraped JSON manually—rerun with `--skip-scrape` or clear cache.

