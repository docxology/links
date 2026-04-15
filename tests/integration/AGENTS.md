# `tests/integration/` agent notes

## Purpose

Exercise `main()` functions with `unittest.mock.patch` on dependencies. CLI argv mapping is in `tests/test_pipeline_cli.py`; full pipeline order with injected `PipelineStages` is in `tests/test_main.py` and `test_pipeline_flow` here.

## Optional real files

Some tests may skip if `data/` or `output/` artifacts are missing — see `test_pipeline.py` markers and skip conditions.

## Running

```bash
uv run pytest tests/integration -q
```
