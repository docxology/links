# `src/data/` agent notes

## Module

[`organize_links.py`](organize_links.py):

- `load_raw_links(file_path)` — JSON array of link objects; respects `MAX_LINKS`
- `categorize_links(links_data)` — keyword-based bucketing into `political`, `economic`, `social`, `technological`, `other`
- `save_organized_links()`, `main()` — writes `ORGANIZED_LINKS_PATH` (`data/organized_links.json`)

## Contracts

- Input: `bestofnow_urls.json` and `bestofnow_tags.json` (validated by `config.validate_files()` when used).
- Output shape: dict of category → list of link dicts with `url`, `title`, `tags`, etc.
- Feeds stage 2 (`scrape_sites.py`).

## Configuration

Uses `RAW_LINKS_PATH`, `TAGS_JSON_PATH`, `ORGANIZED_LINKS_PATH`, `MAX_LINKS` from [`../utils/config.py`](../utils/config.py).

## Tests

- Unit: [`../../tests/unit/test_data_organize_links.py`](../../tests/unit/test_data_organize_links.py)
- Integration: part of `tests/integration/test_pipeline.py`

See [`../AGENTS.md`](../AGENTS.md) and root [`../../README.md`](../../README.md). Generated JSON should not be edited manually.

