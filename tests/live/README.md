# tests/live/

Opt-in tests that exercise the real OpenAI API.

Run with:

```bash
uv run pytest tests/live -m live_openai
```

Requires `OPENAI_API_KEY`. Excluded from default `uv run pytest` by `pyproject.toml`.

See [`../TESTING.md`](../TESTING.md).
