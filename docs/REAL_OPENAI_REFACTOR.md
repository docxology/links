# REAL_OPENAI_REFACTOR.md (Historical)

**This document records the refactor completed in 2026. See canonical documentation in:**

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`API_REFERENCE.md`](API_REFERENCE.md)
- [`TESTING.md`](TESTING.md)
- Root [`README.md`](../README.md)

The changes (uv, OPENAI_API_KEY only, PipelineStages for no-mock testing, strict JSON in generate_essay_images, live tests, pyproject.toml) are now live and documented above. This file is kept for audit.

This document describes changes to satisfy: **uv** for tooling, **real OpenAI** verification, **no unittest mocks** for orchestration/CLI, **no silent fallbacks** in essay image prompt parsing, and **composable** pipeline execution.

## 1. `pyproject.toml` (uv)

Create at repo root:

```toml
[project]
name = "links-pipeline"
version = "1.1.0"
requires-python = ">=3.12"
dependencies = [
    "beautifulsoup4==4.12.2",
    "requests==2.31.0",
    "openai==1.6.0",
    "python-dotenv==1.0.0",
    "tqdm==4.66.1",
    "pyyaml==6.0.1",
    "colorama==0.4.6",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=4"]

[tool.pytest.ini_options]
markers = [
    "live_openai: calls OpenAI API (requires OPENAI_API_KEY)",
]
testpaths = ["tests"]
```

Commands:

```bash
uv sync
uv sync --extra dev
uv run pytest
```

Keep `requirements.txt` in sync or remove it and document `uv sync` only.

## 2. Split CLI (`src/pipeline_cli.py`)

Move `build_parser`, `apply_only_flags`, and `parse_pipeline_argv(argv) -> dict` out of `src/main.py` so tests assert **pure parsing** with **no `patch("run_pipeline")`**.

`main()` becomes:

```python
from src.pipeline_cli import parse_pipeline_argv
kwargs = parse_pipeline_argv(sys.argv[1:])
run_pipeline(**kwargs)
```

## 3. Injectable pipeline stages (`src/pipeline_orchestration.py`)

Define a `@dataclass` with nine callables defaulting to the real `*_main` imports. `run_pipeline(..., stages: PipelineStages | None = None)` invokes `stages.organize()` etc.

Tests pass **plain functions** that append to a list (no `unittest.mock`):

```python
called = []
def fake_org():
    called.append("organize")
run_pipeline(..., stages=PipelineStages(organize=fake_org, ...))
```

## 4. `generate_essay_images.py` — remove fallbacks

- Use `GPT_MODEL` from config for chat (replace hardcoded `gpt-4`).
- `extract_image_prompts_from_essay`: require a JSON array of two strings; on parse failure **raise `ValueError`** with the model raw text (no generic string fallbacks, no bare `except`).
- `generate_image`: on failure **raise** (do not return `""`).
- Import `OPENAI_API_KEY` only (drop `OPENAI_KEY` alias usage across `src/`).

## 5. Config (`src/utils/config.py`)

- Remove `OPENAI_KEY`; update all modules to `OPENAI_API_KEY`.
- Optional: `PIPELINE_ROOT` env to override `BASE_DIR` for isolated tests (reload-heavy); **prefer** optional path arguments on each `main()` (e.g. `organize_links.main(raw_path=..., out_path=...)`) to avoid reload.

## 6. Tests

| Area | Approach |
|------|----------|
| CLI | `parse_pipeline_argv([...])` dict equality — **no mocks** |
| Orchestration | `PipelineStages` with recording callables — **no mocks** |
| Pure functions | `categorize_links`, `render_markdown`, `extract_meaningful_content(BeautifulSoup(html))` — **real data** |
| File I/O | `tmp_path` and real `open()` — **no mock_open** |
| OpenAI | `tests/live/test_openai.py` with `@pytest.mark.live_openai` and `pytest.skipif(not os.getenv("OPENAI_API_KEY"), ...)` — one `chat.completions.create` smoke test; optional one image test behind env `RUN_IMAGE_SMOKE=1` |

Default CI: `uv run pytest -m "not live_openai"` to avoid billing.

Local verification with your real key:

```bash
export OPENAI_API_KEY=...   # or rely on .env
uv run pytest -m live_openai -v
```

## 7. Documentation

Update `README.md`, `docs/DEVELOPMENT.md`, `docs/TESTING.md`:

- `uv sync` / `uv run`
- Marker `live_openai` and when to run it
- Remove claims of “no external calls” in tests if live tests are added

## 8. Order of work

1. Add `pyproject.toml`; `uv sync` validates lockfile.
2. Add `pipeline_cli.py`; slim `main.py`.
3. Add `pipeline_orchestration.py` + injectable `run_pipeline`.
4. Harden `generate_essay_images.py`; unify `OPENAI_API_KEY`.
5. Rewrite `tests/test_main.py` → `tests/test_pipeline_cli.py` (no mocks).
6. Rewrite stage-order test using `PipelineStages`.
7. Add `tests/live/test_openai.py`.
8. Incrementally replace `mock_open` / `patch` in unit tests with `tmp_path` + real HTML/JSON.

---

**Note:** Edits to `.py` and `pyproject.toml` require **Agent mode** in Cursor. If mode stays Plan-only, apply this spec locally or switch mode and re-run the agent.
