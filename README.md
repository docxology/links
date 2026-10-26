# Links Analysis Pipeline

End-to-end pipeline: organize URLs, scrape pages, extract structured principles/policies/values/goals with an LLM, aggregate and write overview essays, generate essay images, synthesize a political platform, render Markdown and HTML, and generate platform images.

## Requirements

- Python 3.12+ (see `pyproject.toml` / `requirements.txt`)
- [uv](https://github.com/astral-sh/uv) for environments and commands
- `OPENAI_API_KEY` for LLM and image APIs

## Setup

```bash
git clone <repository-url>
cd links

uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

uv sync --all-extras
# or: uv pip install -r requirements.txt

cp .env.example .env
# Set OPENAI_API_KEY and optional variables (see below)
```

Required inputs in the project root:

- `bestofnow_urls.json` — list of link objects (`url`, `title`, `description`, `tags`, …)
- `bestofnow_tags.json` — tag metadata (validated when using helpers that require it)

## Environment variables

| Variable | Role |
|----------|------|
| `OPENAI_API_KEY` | Required for OpenAI chat and image calls |
| `LOG_LEVEL` | Logging level (default: `INFO`) |
| `MAX_LINKS` | Cap on URLs loaded from `bestofnow_urls.json` (default: `40`) |
| `GPT_MODEL` | Chat model (default: `gpt-4`) |
| `TIMEOUT` | HTTP timeout for scraping, in seconds (exposed in code as `REQUEST_TIMEOUT`, default `30`) |
| `IMAGE_MODEL` | Declared in `src/utils/config.py`; `generate_images.py` currently hardcodes `gpt-image-1` |
| `ESSAY_IMAGE_MODEL` | Essay images in `generate_essay_images.py` (default: `dall-e-3`) |

`MAX_CONCURRENT_REQUESTS` is fixed at `5` in `src/utils/config.py` (not read from the environment).

## Pipeline (nine stages)

Orchestration: `src/main.py` → `src/pipeline_cli.py` (`parse_pipeline_argv`) → `src/pipeline_orchestration.py` (`run_pipeline`).

| Stage | Module | Purpose |
|-------|--------|---------|
| 1 | `src/data/organize_links.py` | Load URLs, categorize by keywords, write `data/organized_links.json` |
| 2 | `src/scrapers/scrape_sites.py` | Scrape pages with cache under `cached_data/`, write `data/scraped_data.json` |
| 3 | `src/analysis/extract_concepts.py` | Per-document JSON: principles, policies, values, goals → `output/extracted_concepts.json` |
| 4 | `src/analysis/organize_extractions.py` | `output/site_specific/`, `output/compiled/` |
| 5 | `src/analysis/generate_essays.py` | `output/essays/*_essay.md` from compiled data |
| 6 | `src/analysis/generate_essay_images.py` | `output/essay_images/` (default `ESSAY_IMAGE_MODEL` = `dall-e-3`) |
| 7 | `src/analysis/generate_platform.py` | `output/political_platform.json` |
| 8 | `src/analysis/render_markdown.py` | `output/political_platform.md`, `output/political_platform.html` |
| 9 | `src/analysis/generate_images.py` | `output/platform_images/` (GPT-Image-1) |

## Usage

```bash
# Full pipeline
uv run python -m src.main

# One stage only (others skipped)
uv run python -m src.main --only-organize
uv run python -m src.main --only-scrape
uv run python -m src.main --only-extract
uv run python -m src.main --only-organize-extractions
uv run python -m src.main --only-essays
uv run python -m src.main --only-essay-images
uv run python -m src.main --only-analyze
uv run python -m src.main --only-render
uv run python -m src.main --only-images

# Skip stages
uv run python -m src.main --skip-scrape --skip-images
```

If multiple `--only-*` flags are passed, **each flag handler runs in a fixed script order** (organize → scrape → extract → organize-extractions → essays → essay-images → analyze → render → images). A later handler in that sequence overrides earlier ones, so e.g. `--only-extract --only-analyze` runs **analyze** only.

## Logging demo

```bash
uv run python demo_logging.py
```

## Tests

```bash
uv run pytest
```

See [docs/TESTING.md](docs/TESTING.md).

## Documentation

Comprehensive docs live in [`docs/`](docs/) with hub at [`docs/README.md`](docs/README.md) (recommended reading order: USER_GUIDE → ARCHITECTURE → API_REFERENCE → TESTING → DEVELOPMENT).

Folder-level `README.md` and `AGENTS.md` exist in `src/`, `tests/`, `docs/`, `data/`, `output/`, etc. for context-specific guidance.

| Doc | Content |
|-----|---------|
| [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) | Operator usage, outputs, troubleshooting |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Pipeline flow (mermaid), data shapes, error handling |
| [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) | Functions, CLI flags, contracts |
| [`docs/TESTING.md`](docs/TESTING.md) | Test layout, markers, TDD policy |
| [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) | `uv`, contributing, workflow |
| [`docs/SUMMARY.md`](docs/SUMMARY.md) | 5-minute overview |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Version history |
| [`docs/cursor_setup.md`](docs/cursor_setup.md) | IDE notes |
| [`diagram.md`](diagram.md) | Additional Mermaid diagrams |
| [`docs/REAL_OPENAI_REFACTOR.md`](docs/REAL_OPENAI_REFACTOR.md) | Historical refactor checklist |

See folder `README.md` files (e.g. [`src/README.md`](src/README.md), [`tests/README.md`](tests/README.md), [`output/README.md`](output/README.md)) for local context.

## Contributing

1. Follow [`.cursorrules`](.cursorrules) (TDD, real data, modular code, understated docs).
2. Add tests for new behavior (update `test_pipeline_cli.py`, `test_main.py`, or module tests).
3. Expand relevant `AGENTS.md` and `README.md` in affected folders.
4. Update [`docs/CHANGELOG.md`](docs/CHANGELOG.md), this `README.md`, and [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md).
5. Run `uv run pytest` and `uv sync --all-extras`.
6. Submit PR.

See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for details.

## Layout

```
├── src/                 # Application code (main, pipeline_*.py, analysis/, data/, scrapers/, utils/)
├── tests/               # pytest suite (unit, integration, live/)
├── data/                # Organized links JSON
├── output/              # All generated artifacts (see output/README.md)
├── cached_data/         # Scrape cache
├── logs/                # Stage and pipeline logs
├── docs/                # Comprehensive documentation (see docs/README.md)
├── bestofnow_urls.json
├── bestofnow_tags.json
├── requirements.txt
├── pyproject.toml
├── .env.example
├── AGENTS.md
└── README.md
```
