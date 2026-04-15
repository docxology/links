# src/analysis/

LLM-powered stages 3–9 of the pipeline.

## Modules by Stage

| Stage | Module | Responsibility |
|-------|--------|----------------|
| 3 | `extract_concepts.py` | Per-document structured extraction of principles, policies, values, goals |
| 4 | `organize_extractions.py` | Site-specific JSON trees and compiled aggregates |
| 5 | `generate_essays.py` | Category overview essays from compiled data |
| 6 | `generate_essay_images.py` | Prompt generation (`GPT_MODEL`) and image creation (`ESSAY_IMAGE_MODEL`) |
| 7 | `generate_platform.py` | Political platform synthesis from extractions |
| 8 | `render_markdown.py` | Markdown + HTML output from platform JSON |
| 9 | `generate_images.py` | Platform-themed images (`IMAGE_MODEL`) |

See [`pipeline_orchestration.py`](../pipeline_orchestration.py) for how these are wired into `run_pipeline()` and [`../AGENTS.md`](../AGENTS.md) for repo-level notes.

All modules use real OpenAI calls (no mocks in orchestration tests) and are covered by unit and integration tests in [`../../tests/`](../../tests/).

Outputs land under `../.. /output/`.
