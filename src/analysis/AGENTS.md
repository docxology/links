# `src/analysis/` agent notes

## Modules by Stage

| File | Stage | Key Functions / Contracts | Notes |
|------|-------|---------------------------|-------|
| `extract_concepts.py` | 3 | `extract_concepts()`, `save_extracted_concepts()` | Structured `categories` per document; feeds `organize_extractions` |
| `organize_extractions.py` | 4 | `create_site_specific_structure()`, `create_compiled_structure()` | Produces `output/site_specific/` and `output/compiled/`; returns path dict |
| `generate_essays.py` | 5 | `generate_category_essay()`, `validate_essay_quality()` | Reads compiled JSON; writes `*_essay.md`; source attribution and quality checks |
| `generate_essay_images.py` | 6 | `_parse_two_prompt_strings()`, `extract_image_prompts_from_essay()` | Strict JSON array of two strings from `GPT_MODEL`; `ESSAY_IMAGE_MODEL` (default `dall-e-3`); raises on parse or API failure |
| `generate_platform.py` | 7 | `generate_platform()`, `_text_from_extracted_document()` | Supports both legacy string and structured categories; writes `political_platform.json` |
| `render_markdown.py` | 8 | `render_markdown()`, `render_html()`, `main()` | Returns `(markdown_path, html_path)` tuple |
| `generate_images.py` | 9 | `generate_image_prompts()`, `generate_images()` | Uses `IMAGE_MODEL`; platform-themed images |

## Contracts and Invariants

- `extract_concepts` JSON (`output/extracted_concepts.json`) is the canonical source for downstream stages.
- `generate_platform.prepare_prompt` / `_text_from_extracted_document` handles both legacy and structured `categories`.
- `generate_essay_images` **never** falls back to generic prompts on failure—raises `ValueError` for bad JSON or `RuntimeError` for image API issues.
- All `main()` functions return dicts or paths for orchestration logging (or `None` which is normalized in `pipeline_orchestration.py`).
- Real OpenAI client (v1) with `OPENAI_API_KEY`; `httpx.Client` for timeouts.

## Testing

- Unit: `tests/unit/test_analysis_*.py` (including `test_analysis_generate_essay_images_parse.py` for prompt parser).
- Integration: `tests/integration/test_pipeline.py` uses injected `PipelineStages`.
- Live: `tests/live/test_openai.py` (opt-in with `@pytest.mark.live_openai`).

See [`../AGENTS.md`](../AGENTS.md) and root [`README.md`](../../README.md) for full pipeline context. Do not edit generated output directories directly.

