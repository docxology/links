# Development

## Environment

```bash
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync --all-extras         # install from pyproject.toml + dev (pytest)
# or: uv pip install -r requirements.txt && uv pip install pytest pytest-cov
```

Optional: `black`, `ruff` or `flake8`, `mypy` — not pinned in this repo; add locally as needed.

Project conventions: see [`.cursorrules`](../.cursorrules) at the repository root.

## Running tests

```bash
uv run pytest
uv run pytest tests/unit -q
uv run pytest tests/integration -q
uv run pytest --cov=src --cov-report=html
```

## Layout

- `src/` — application code (`main.py` → `pipeline_cli.py` / `pipeline_orchestration.py` → stage modules)
- `tests/unit/` — per-module tests
- `tests/integration/` — pipeline wiring and optional on-disk fixtures
- `tests/fixtures/` — JSON samples where used

## OpenAI client

Use the `openai` v1 client: `OpenAI(api_key=..., http_client=httpx.Client(timeout=...))` as in `extract_concepts.py`, `generate_platform.py`, etc.

## Docs and diagrams

- User-facing: [USER_GUIDE.md](USER_GUIDE.md), [README.md](../README.md)
- Diagrams: [diagram.md](../diagram.md)

## Continuous integration

No workflow is checked into this repository yet. To add CI, create `.github/workflows/` and run `uv run pytest` there.

## Contributing

1. Branch from `main`
2. Add or update tests for behavior changes
3. Run `uv run pytest`
4. Update relevant docs (`README.md`, `docs/*.md`)
