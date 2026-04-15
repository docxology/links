# Testing

## Commands

```bash
uv run pytest
uv run pytest -v
uv run pytest tests/unit/test_utils_config.py
uv run pytest -k "extract"
uv run pytest --cov=src --cov-report=html
```

## Layout

```
tests/
├── conftest.py           # Shared fixtures
├── fixtures/             # JSON samples
├── test_pipeline_cli.py  # ``parse_pipeline_argv`` (argparse → skip kwargs)
├── test_main.py          # ``main`` wiring + ``run_pipeline`` with injected stages
├── live/
│   └── test_openai.py    # ``@pytest.mark.live_openai`` (optional; not in default run)
├── unit/
│   ├── test_analysis_*.py
│   ├── test_data_organize_links.py
│   ├── test_scrapers_scrape_sites.py
│   ├── test_utils_config.py
│   └── test_utils_logger.py
└── integration/
    └── test_pipeline.py  # Stage mains with patches; optional repo file checks
```

## What is tested

- **Unit**: config paths, logger behavior, parsing helpers, markdown rendering, etc.
- **`test_pipeline_cli.py`**: argv → `run_pipeline` kwargs for all nine skip flags and `--only-*` behavior.
- **`test_main.py`**: `main()` passes `sys.argv[1:]` into `parse_pipeline_argv` and `run_pipeline`; full pipeline order with `PipelineStages` injected (no `unittest.mock` on stages).
- **Integration**: `main()` of each stage with `unittest.mock.patch` on file I/O or heavy dependencies — no network in the default suite.

Tests that require committed files under `data/` and `output/` may be skipped when those files are absent or empty; see markers and `pytest.skip` in `tests/integration/test_pipeline.py`.

## Policy on external APIs

Default `uv run pytest` excludes `@pytest.mark.live_openai` (see `addopts` in `pyproject.toml`). Live checks: `uv run pytest tests/live -m live_openai` with `OPENAI_API_KEY` set.

Follows TDD and "real data, no mocks" from `.cursorrules`: unit tests use real fixtures where possible; orchestration tests inject `PipelineStages` rather than patching stage mains.

## Coverage

Coverage is not enforced by CI in-repo; use `--cov=src` locally if you need a report. Aim for high coverage on config, parsing, and core logic.

See [`tests/README.md`](../tests/README.md) and folder-level AGENTS.md for per-area details.

