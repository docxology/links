# tests/

pytest suite for the links analysis pipeline.

## Layout

- `conftest.py` — fixtures (`sample_urls`, `sample_scraped_data`, `sample_platform`)
- `test_pipeline_cli.py` — pure argument parsing tests
- `test_main.py` — `main()` wiring and `run_pipeline` with injectable `PipelineStages` (no mocks on stages)
- `live/` — opt-in OpenAI smoke tests (`@pytest.mark.live_openai`)
- `unit/` — per-module tests (real data where possible)
- `integration/` — stage `main()` with patches on I/O and heavy deps
- `fixtures/` — sample JSON for tests

Default run: `uv run pytest` (excludes live tests via `pyproject.toml` `addopts`).

See [`../docs/TESTING.md`](../docs/TESTING.md) for details and [`../README.md`](../README.md) for project context.

All tests prefer real methods over mocks per [`.cursorrules`](../.cursorrules).
