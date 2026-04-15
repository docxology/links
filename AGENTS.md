# Repository agent notes

## Role

Python pipeline: URLs → scrape → LLM extraction → aggregates → essays → essay images → political platform → Markdown/HTML → platform images.

## Entry points

- `uv run python -m src.main` — full or selective pipeline (`--skip-*`, `--only-*`; parsing in `src/pipeline_cli.py`, execution in `src/pipeline_orchestration.py`)
- `uv run pytest` — default suite (excludes `live_openai`; see `docs/TESTING.md`)

## Configuration

- `src/utils/config.py` — paths and env; **`TIMEOUT`** sets HTTP timeout (loaded as `REQUEST_TIMEOUT`)
- `.env.example` — template; never commit real keys

## Documentation

- `README.md` — setup and stage table
- `docs/` — guides and API reference
- `diagram.md` — Mermaid diagrams

## Conventions

- Follow [`.cursorrules`](.cursorrules).
- Use `uv` for install and test commands.
