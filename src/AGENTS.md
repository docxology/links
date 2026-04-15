# `src/` agent notes

## Layout

| Path | Responsibility |
|------|----------------|
| `main.py` | CLI entry: `parse_pipeline_argv` + `run_pipeline` |
| `pipeline_cli.py` | `build_parser`, `apply_only_flags`, `parse_pipeline_argv` |
| `pipeline_orchestration.py` | `PipelineStages`, `run_pipeline` |
| `data/organize_links.py` | Load URLs, categorize, write organized JSON |
| `scrapers/scrape_sites.py` | Fetch, cache, parse HTML |
| `analysis/` | LLM extraction, aggregation, essays, platform, render, images |
| `utils/config.py` | Paths, env |
| `utils/logger.py` | Logging helpers |

## Imports

Packages use `src.` prefix (e.g. `from src.utils.config import ...`). Running as `python -m src.main` sets up the package context.

## Changing behavior

- Add a stage: implement `main()` in a module; wire it in `src/pipeline_orchestration.py` (`PipelineStages` + `run_pipeline`); add flags in `src/pipeline_cli.py` (`build_parser`, `apply_only_flags`, `parse_pipeline_argv`); update docs and tests.
