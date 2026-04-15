# `tests/unit/` agent notes

## Purpose

Fast tests for single modules: `organize_links`, `scrape_sites`, `extract_concepts`, `generate_platform`, `render_markdown`, `generate_images`, `generate_essay_images` (prompt JSON parsing), `config`, `logger`.

## Conventions

- Prefer real file paths via `tmp_path` where I/O is tested
- Mock `openai` client methods when testing LLM wrappers without billing

## Running

```bash
uv run pytest tests/unit -q
```
