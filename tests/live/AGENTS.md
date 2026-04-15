# `tests/live/` agent notes

Opt-in OpenAI API checks. Marked `live_openai`; excluded from default `uv run pytest` (`addopts` in `pyproject.toml`).

```bash
uv run pytest tests/live -m live_openai
```

Requires `OPENAI_API_KEY` and network.
