# Project summary

## Purpose

End-to-end pipeline that turns curated URL lists into structured political philosophy (principles, policies, values, goals), essays, images, a synthesized platform, and rendered Markdown/HTML.

**Nine stages**, real OpenAI calls, composable orchestration with `PipelineStages` for testing without mocks, `uv` for dependency management.

## Code map

| Area | Role |
|------|------|
| [`README.md`](../README.md) | Primary GitHub overview |
| [`src/main.py`](../src/main.py) | CLI entry |
| [`src/pipeline_cli.py`](../src/pipeline_cli.py) | Argument parsing (`--skip-*`, `--only-*`) |
| [`src/pipeline_orchestration.py`](../src/pipeline_orchestration.py) | `PipelineStages` dataclass and `run_pipeline` |
| [`src/data/`](../src/data/) | Stage 1: link loading and categorization |
| [`src/scrapers/`](../src/scrapers/) | Stage 2: HTTP + cache + parsing |
| [`src/analysis/`](../src/analysis/) | Stages 3-9: extraction, organization, essays, images, platform, render |
| [`src/utils/`](../src/utils/) | `config.py`, `logger.py` |
| [`tests/`](../tests/) | Unit, integration, live OpenAI tests |
| [`docs/`](./) | Comprehensive documentation (see [`docs/README.md`](README.md)) |
| `output/`, `data/`, `cached_data/`, `logs/` | Generated artifacts (see their READMEs) |

## Operations

- **Setup**: `uv sync --all-extras`; copy `.env.example` to `.env` with `OPENAI_API_KEY`
- **Run**: `uv run python -m src.main` or with `--only-extract`, `--skip-scrape`, etc.
- **Test**: `uv run pytest` (default); `uv run pytest tests/live -m live_openai` for real API
- **Docs**: Start with root [`README.md`](../README.md), then [`docs/README.md`](README.md)

## Version

See [`CHANGELOG.md`](CHANGELOG.md). Current version in `pyproject.toml` is 1.1.0.

This file serves as the 5-minute overview. For details see the linked documents.

