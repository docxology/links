# output/

Generated artifacts from the pipeline stages.

## Structure

- `extracted_concepts.json` — stage 3 LLM extractions
- `site_specific/` — per-URL/category JSON (stage 4)
- `compiled/` — aggregated principles/policies/values/goals (stage 4)
- `essays/` — category overview Markdown (stage 5)
- `essay_images/` — images from essays (stage 6, `generation_summary.json`)
- `political_platform.json` — synthesized platform (stage 7)
- `political_platform.md` / `.html` — rendered output (stage 8)
- `platform_images/` — images from platform (stage 9)

These are **generated**. Rerun relevant stages or use `--skip-*` flags to reuse. Do not edit manually.

See root [`../README.md`](../README.md) for pipeline and [`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) for data flow.
