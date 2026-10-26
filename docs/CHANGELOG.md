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
- Dependency refresh in `pyproject.toml` / `requirements.txt` with regenerated `uv.lock`: `openai` 1.6.0 → 1.109.1, `requests` 2.31.0 → 2.34.2, `beautifulsoup4` 4.12.2 → 4.15.0, `python-dotenv` 1.0.0 → 1.2.4, `tqdm` 4.66.1 → 4.70.1, `pyyaml` 6.0.1 → 6.0.3, `httpx>=0.28.1`; dev extras `pytest>=9.1`, `pytest-cov>=7.1`.
- Docs describing `IMAGE_MODEL` corrected: `generate_images.py` hardcodes `gpt-image-1` and does not read the env var. Cursor guide links to `https://docs.cursor.com`.

### Removed
- Abandoned root scripts `run_extraction_pipeline.py` (superseded by `uv run python -m src.main` with `--skip-*` flags) and `validate_pipeline.py` (source-string checks superseded by the test suite).
- Tracked `__pycache__/*.pyc` bytecode (stale CPython 3.10/3.12/3.13 artifacts) and the local `.env`, both now covered by a new `.gitignore` (use `.env.example` as the template).

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
