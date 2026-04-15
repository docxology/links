# src/

Core Python package for the links analysis pipeline.

The entry point is [`main.py`](main.py), which uses [`pipeline_cli.py`](pipeline_cli.py) for argument parsing and [`pipeline_orchestration.py`](pipeline_orchestration.py) for composable stage execution via `PipelineStages` and `run_pipeline(...)`.

## Subpackages

- [`analysis/`](analysis/) — LLM extraction, essays, platform synthesis, rendering, image generation (stages 3-9)
- [`data/`](data/) — link organization (stage 1)
- [`scrapers/`](scrapers/) — web scraping and caching (stage 2)
- [`utils/`](utils/) — shared configuration, logging, and helpers

See [`../README.md`](../README.md) for full pipeline overview and usage, and [`AGENTS.md`](AGENTS.md) for technical details.

Run with:

```bash
uv run python -m src.main
uv run python -m src.main --only-extract
```

All modules follow the conventions in [`.cursorrules`](../.cursorrules) and are tested in [`../tests/`](../tests/).
