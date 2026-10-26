# User Guide

## What it does

1. Reads URL lists and groups them by keyword categories.
2. Scrapes page text (with disk cache to avoid repeat downloads).
3. Extracts **principles**, **policies**, **values**, and **goals** per page via an LLM.
4. Writes per-site and compiled aggregates for downstream writing.
5. Generates long-form essays per aggregate category.
6. Optionally generates images per essay (DALL·E 3).
7. Synthesizes a full political platform JSON from extracted concepts.
8. Renders Markdown and static HTML for the platform.
9. Generates platform-themed images (GPT-Image-1).

## Prerequisites

- Python 3.12+, `uv`, OpenAI API key with billing appropriate for chat + image usage
- `bestofnow_urls.json` and `bestofnow_tags.json` in the repo root (see `src/utils/config.validate_files()` when you add validation to your entry path)

## Install and run

```bash
uv venv && source .venv/bin/activate
uv sync --all-extras
# or: uv pip install -r requirements.txt
cp .env.example .env
# set OPENAI_API_KEY

uv run python -m src.main
```

## Environment

| Variable | Notes |
|----------|------|
| `OPENAI_API_KEY` | Required |
| `TIMEOUT` | Scraping timeout (seconds); not the name `REQUEST_TIMEOUT` in `.env` |
| `MAX_LINKS` | Limits rows read from the URL list |
| `GPT_MODEL` | Chat completions for extraction, platform, essays, essay-image prompts |
| `IMAGE_MODEL` | Declared in `src/utils/config.py`; `generate_images.py` currently hardcodes `gpt-image-1` |
| `ESSAY_IMAGE_MODEL` | Essay images (`generate_essay_images.py`; default `dall-e-3`) |
| `LOG_LEVEL` | e.g. `DEBUG` for verbose logs |

## Outputs (under `output/`)

| Path | Description |
|------|-------------|
| `extracted_concepts.json` | Per-site extractions |
| `extracted_concepts_text.txt` | Human-readable mirror |
| `site_specific/` | Per URL / category JSON |
| `compiled/` | Aggregated JSON + summaries |
| `essays/` | `*_essay.md` |
| `essay_images/` | PNGs + `generation_summary.json` |
| `political_platform.json` | Platform sections + executive summary |
| `political_platform.md` / `.html` | Rendered platform |
| `platform_images/` | Platform image set |

Logs: `logs/` and stage-specific files referenced in `get_logger(...)`.

## CLI shortcuts

```bash
uv run python -m src.main --skip-scrape          # reuse cached/scraped data
uv run python -m src.main --skip-images        # skip platform images (stage 9)
uv run python -m src.main --skip-essay-images  # skip stage 6
uv run python -m src.main --only-extract       # only stage 3
```

If you pass more than one `--only-*` flag, handlers run in a **fixed script order**; a later stage (e.g. `--only-analyze`) overrides an earlier one (e.g. `--only-extract`).

## Troubleshooting

- **Missing input files**: ensure `bestofnow_urls.json` / `bestofnow_tags.json` paths match `src/utils/config.py`.
- **429 / billing errors**: reduce `MAX_LINKS`, skip essay or image stages, or check OpenAI quota.
- **Stale scrape**: delete `cached_data/` for that host or use `--skip-scrape` only when `data/scraped_data.json` is already valid.

## Further reading

- [API_REFERENCE.md](API_REFERENCE.md) — functions and flags
- [TESTING.md](TESTING.md) — running tests with `uv run pytest`
