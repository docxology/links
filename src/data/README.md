# src/data/

Stage 1 of the pipeline: loading and categorizing input links.

## Primary Module

[`organize_links.py`](organize_links.py) — reads `bestofnow_urls.json`, applies keyword categorization into political/economic/social/technological/other buckets, writes `data/organized_links.json`.

See [`../pipeline_orchestration.py`](../pipeline_orchestration.py) for how it is called and [`../../README.md`](../../README.md) for full pipeline.

Configuration from [`../utils/config.py`](../utils/config.py): `RAW_LINKS_PATH`, `TAGS_JSON_PATH`, `MAX_LINKS`.

Tested in [`../../tests/unit/test_data_organize_links.py`](../../tests/unit/test_data_organize_links.py) and integration tests.

Do not edit generated JSON files manually—rerun the stage or use `--skip-organize`.
