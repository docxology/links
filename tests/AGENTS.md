# `tests/` agent notes

## Commands

```bash
uv run pytest
uv run pytest tests/unit
uv run pytest tests/integration
```

## Layout

- `conftest.py` — shared fixtures (`sample_urls`, `sample_scraped_data`, etc.)
- `test_pipeline_cli.py` — `parse_pipeline_argv`
- `test_main.py` — `main` wiring; `run_pipeline` with injected `PipelineStages`
- `live/` — `pytest.mark.live_openai` (excluded from default run via `pyproject.toml`)
- `unit/` — isolated module tests
- `integration/` — `main()` wiring with mocks; optional checks against repo `data/` / `output/` files

## Policy

Default `pytest` omits `live_openai`. Patch network and API boundaries in integration tests.
