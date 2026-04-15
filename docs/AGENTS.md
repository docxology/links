# `docs/` agent notes

## Purpose

Technical and user-facing documentation for the nine-stage links analysis pipeline. All files are Markdown and should be kept in sync with code changes in `src/`.

See [`docs/README.md`](README.md) for reading order.

## Contents

| File | Purpose |
|------|---------|
| `README.md` | Hub page with reading order and brief descriptions of each doc |
| `API_REFERENCE.md` | Module functions, CLI flags (`parse_pipeline_argv`, `run_pipeline`), data shapes, dependencies |
| `ARCHITECTURE.md` | Pipeline stages, data flow (mermaid), trust boundaries, image generation paths, error handling |
| `USER_GUIDE.md` | Operator instructions, CLI examples, outputs, troubleshooting, environment variables |
| `DEVELOPMENT.md` | `uv sync`, testing commands, contributing checklist, optional tools |
| `TESTING.md` | Test layout, markers (`live_openai`), `pyproject.toml` config, how to run subsets |
| `SUMMARY.md` | One-page project overview and code map |
| `CHANGELOG.md` | Version history following Keep a Changelog |
| `cursor_setup.md` | Cursor IDE setup with project-specific notes (`.cursorrules`, AGENTS convention) |
| `REAL_OPENAI_REFACTOR.md` | Historical implementation checklist for OpenAI, `uv`, no-mocks refactor (see ARCHITECTURE.md for current state) |

## Rules

- Keep docs consistent with `src/pipeline_orchestration.py` stage order, `PipelineStages`, `src/pipeline_cli.py` flags, and `src/utils/config.py` (`OPENAI_API_KEY`, `GPT_MODEL`, `ESSAY_IMAGE_MODEL`, `IMAGE_MODEL`, `REQUEST_TIMEOUT`).
- Prefer concrete paths, commands (`uv sync --all-extras`, `uv run pytest`), and code citations over marketing language.
- Update root [`README.md`](../README.md), stage tables, and cross-links when adding stages or changing behavior.
- Use understated "show not tell" style per [`.cursorrules`](../.cursorrules).
- Avoid editing generated artifact directories (`output/`, `cached_data/`) documentation in detail—describe at parent level only.

## See also

- Root [`AGENTS.md`](../AGENTS.md) for repo conventions.
- [`diagram.md`](../diagram.md) for Mermaid visuals.

