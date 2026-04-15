# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versions are semantic when tagged in git.

## [Unreleased]

### Added
- Folder-level `README.md` and expanded `AGENTS.md` across `src/`, `tests/`, `docs/`, and artifact directories (`data/`, `output/`, etc.).
- `docs/README.md` as documentation hub with recommended reading order.
- Comprehensive updates to all `docs/*.md` for consistency with current orchestration (`pipeline_cli.py`, `PipelineStages`), environment variables (`ESSAY_IMAGE_MODEL`), real-data testing, and GitHub-facing root `README.md`.
- `pyproject.toml` with optional dev extras; `httpx` dependency; `tests/live/` for opt-in OpenAI smoke tests (`live_openai` marker).

### Changed
- Documentation aligned with nine-stage pipeline, `TIMEOUT` / `REQUEST_TIMEOUT`, strict JSON prompt parsing in essay images (no fallbacks), and `uv sync --all-extras` workflow.
- CLI split: `src/pipeline_cli.py`, `src/pipeline_orchestration.py`; `OPENAI_API_KEY` only.
- Expanded root `README.md` as primary overview; all docs now cross-link and avoid drift.

See [`REAL_OPENAI_REFACTOR.md`](REAL_OPENAI_REFACTOR.md) for historical context of the 2026 refactor.

## [1.1.0] - 2026-04-15

### Added
- Stages 4–6: `organize_extractions`, `generate_essays`, `generate_essay_images` with outputs under `output/site_specific`, `output/compiled`, `output/essays`, `output/essay_images`.
- CLI flags: `--skip-organize-extractions`, `--skip-essays`, `--skip-essay-images`, `--only-organize-extractions`, `--only-essays`, `--only-essay-images`.
- Expanded `run_pipeline(...)` signature with the new skip parameters.

### Changed
- Concept extraction now emits structured `principles` / `policies` / `values` / `goals` per document (not a single `concepts` string) for the aggregation stages.
- Docs and README describe dual image paths: DALL·E 3 (essay images) vs GPT-Image-1 (platform images in `generate_images.py`).

## [1.0.1] - 2024-01-15

### Changed
- Platform image generation uses GPT-Image-1 in `generate_images.py`.

## [1.0.0] - 2024-01-01

### Added
- Initial six-stage pipeline: organize → scrape → extract → platform → render → platform images.
- OpenAI v1 client, caching, multi-format outputs.

### Breaking
- Migration from OpenAI Python SDK v0.x patterns to v1 `OpenAI` client.

---

## Migration notes

**Environment**: Use `TIMEOUT` in `.env` for HTTP timeout (read as `REQUEST_TIMEOUT` in code).

**Concepts schema**: Downstream code expecting only string `concepts` per document must be updated for the four-category structure produced by `extract_concepts.py`.
