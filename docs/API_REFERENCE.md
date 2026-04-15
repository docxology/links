# API Reference

## `src.main`

Entry point: `python -m src.main`. Delegates to `parse_pipeline_argv(sys.argv[1:])` and `run_pipeline(**kwargs)` (see `src/pipeline_cli.py`, `src/pipeline_orchestration.py`).

## `src.pipeline_cli`

| Function | Description |
|----------|-------------|
| `build_parser()` | `ArgumentParser` with all `--skip-*` and `--only-*` flags |
| `apply_only_flags(args)` | Mutates `args` so a single `--only-*` stage runs |
| `parse_pipeline_argv(argv)` | Parse argv without program name → dict of `skip_*` keys for `run_pipeline` |

## `src.pipeline_orchestration`

### `PipelineStages`

Dataclass of nine callables defaulting to each stage’s `main()`. Pass a custom instance to tests to avoid real work.

### `run_pipeline(...)`

```python
run_pipeline(
    skip_organize=False,
    skip_scrape=False,
    skip_extract=False,
    skip_organize_extractions=False,
    skip_essays=False,
    skip_essay_images=False,
    skip_analyze=False,
    skip_render=False,
    skip_images=False,
    stages: PipelineStages | None = None,
)
```

Runs stages in order unless the corresponding `skip_*` is `True`. **`stages`** defaults to production `PipelineStages()`.

**CLI mapping**

| Flag | Effect |
|------|--------|
| `--skip-organize` | Skip stage 1 |
| `--skip-scrape` | Skip stage 2 |
| `--skip-extract` | Skip stage 3 |
| `--skip-organize-extractions` | Skip stage 4 |
| `--skip-essays` | Skip stage 5 |
| `--skip-essay-images` | Skip stage 6 |
| `--skip-analyze` | Skip stage 7 |
| `--skip-render` | Skip stage 8 |
| `--skip-images` | Skip stage 9 |
| `--only-*` | Sets skips so only that stage runs; multiple `--only-*` apply in **fixed script order** (later handler wins, e.g. `--only-analyze` after `--only-extract` runs analyze only) |

---

## `src.utils.config`

Paths and settings (loaded from environment via `python-dotenv`):

| Name | Source |
|------|--------|
| `BASE_DIR` | Project root |
| `DATA_DIR`, `OUTPUT_DIR`, `CACHE_DIR`, `LOGS_DIR` | Subdirectories under `BASE_DIR` |
| `RAW_LINKS_PATH` | `bestofnow_urls.json` |
| `TAGS_JSON_PATH` | `bestofnow_tags.json` |
| `ORGANIZED_LINKS_PATH` | `data/organized_links.json` |
| `SCRAPED_DATA_PATH` | `data/scraped_data.json` |
| `EXTRACTED_CONCEPTS_PATH` | `output/extracted_concepts.json` |
| `PLATFORM_OUTPUT_PATH` | `output/political_platform.json` |
| `OPENAI_API_KEY` | API key |
| `GPT_MODEL` | Chat model (default `gpt-4`) |
| `IMAGE_MODEL` | Platform images in `generate_images.py` (default `gpt-image-1`) |
| `ESSAY_IMAGE_MODEL` | Essay images in `generate_essay_images.py` (default `dall-e-3`) |
| `REQUEST_TIMEOUT` | `int(os.getenv("TIMEOUT", 30))` |
| `MAX_LINKS` | Default `40` |
| `MAX_CONCURRENT_REQUESTS` | Constant `5` |

`validate_files()` and `validate_api_key()` enforce inputs when called.

---

## `src.data.organize_links`

| Function | Description |
|----------|-------------|
| `load_raw_links(file_path)` | Load JSON list of links; trim to `MAX_LINKS` |
| `categorize_links(links_data)` | Keyword buckets: `political`, `economic`, `social`, `technological`, `other` |
| `save_organized_links(organized_links, output_path)` | Write JSON |
| `main()` | Load → categorize → save to `ORGANIZED_LINKS_PATH` |

---

## `src.scrapers.scrape_sites`

| Function | Description |
|----------|-------------|
| `load_organized_links(file_path)` | Load categorized JSON |
| `scrape_url(url)` | GET with cache, return `status`, `content`, `source` |
| `scrape_links(organized_links)` | Per-category scrape; caps each category at 20 links in code |
| `extract_meaningful_content(soup)` | Title, paragraphs, headings, list items, metadata |
| `save_scraped_data(scraped_data, output_path)` | JSON + `*_text_extract.txt` |
| `main()` | Load organized → scrape → save |

---

## `src.analysis.extract_concepts`

Extracts per document a structured `categories` object: `principles`, `policies`, `values`, `goals` (each a list of items with `title`, `content`, `explanation`, …).

| Function | Description |
|----------|-------------|
| `load_scraped_data(file_path)` | Load scraped JSON |
| `extract_concepts_from_document(document)` | One LLM call; returns JSON-shaped extraction or error/skip |
| `extract_concepts(scraped_data)` | All documents |
| `save_extracted_concepts(extracted_data, output_path)` | JSON + `*_text.txt` |
| `main()` | Load → extract → save |

---

## `src.analysis.organize_extractions`

| Function | Description |
|----------|-------------|
| `create_site_specific_structure(extracted_data, output_dir)` | `output/site_specific/<category>/<safe_url>.json` |
| `create_compiled_structure(extracted_data, output_dir)` | `output/compiled/` JSON + `*_summary.txt` |
| `main()` | Load `EXTRACTED_CONCEPTS_PATH` → both trees; returns dict with paths |

---

## `src.analysis.generate_essays`

| Function | Description |
|----------|-------------|
| `load_compiled_data(compiled_dir)` | Read `principles.json`, `policies.json`, `values.json`, `goals.json` |
| `generate_essay(category, items)` | LLM essay with attribution rules |
| `generate_category_essay(...)` | Write `output/essays/{category}_essay.md` |
| `validate_essay_quality(essay_content, category)` | Heuristic checks + logging |
| `main()` | Generate essays from `output/compiled` |

---

## `src.analysis.generate_essay_images`

Chat prompts use **`GPT_MODEL`**. **`ESSAY_IMAGE_MODEL`** (default `dall-e-3`) is passed to `client.images.generate`. Prompts must parse as a JSON array of exactly two non-empty strings or `extract_image_prompts_from_essay` raises `ValueError`.

| Function | Description |
|----------|-------------|
| `extract_image_prompts_from_essay(essay_content, category)` | Chat completion → two string prompts |
| `generate_image(prompt, category, image_number, output_dir)` | One image file; raises on API/download failure |
| `generate_images_for_essay(essay_file, category, output_dir)` | Two images per essay |
| `main()` | Glob `output/essays/*_essay.md` → `output/essay_images/` |

---

## `src.analysis.generate_platform`

| Function | Description |
|----------|-------------|
| `load_extracted_concepts(file_path)` | Load JSON |
| `prepare_prompt` / `generate_section` | Per-category platform text from `concepts` strings on documents |
| `generate_platform(extracted_data)` | All categories + `executive_summary` |
| `save_platform(platform, output_path)` | Write JSON |
| `main()` | Load → generate → save |

---

## `src.analysis.render_markdown`

| Function | Description |
|----------|-------------|
| `load_platform_data`, `render_markdown`, `render_html` | Platform JSON → strings |
| `save_markdown`, `save_html` | Write files |
| `main()` | Load → render MD + HTML → **returns** `(MARKDOWN_OUTPUT_PATH, HTML_OUTPUT_PATH)` |

Constants: `MARKDOWN_OUTPUT_PATH`, `HTML_OUTPUT_PATH` under `output/`.

---

## `src.analysis.generate_images`

Platform manifesto images: **`gpt-image-1`** in `client.images.generate`.

| Function | Description |
|----------|-------------|
| `load_platform_data`, `generate_image_prompts`, `generate_images` | Prompts from platform JSON |
| `main()` | Returns `IMAGES_OUTPUT_DIR` (`output/platform_images/`) |

---

## `src.utils.logger`

| Function | Description |
|----------|-------------|
| `get_logger(name, log_file=None)` | Console + optional file under `LOGS_DIR` |
| `log_with_emoji(logger, level, emoji_key, message)` | Uses `EMOJI` map (unknown keys → empty prefix) |
| `ColoredFormatter` | ANSI colors when stdout is a TTY |

---

## Data shapes (summary)

**Organized links** — dict of category → list of link objects.

**Scraped document** — `url`, `title`, `content` (dict with `paragraphs`, `headings`, `lists`, …), `status`.

**Extracted document (success)** — `url`, `title`, `categories` (four keys), `raw_response`, `status`.

**Platform JSON** — `executive_summary`, `political`, `economic`, `social`, `technological`, `other` (string sections).

---

## Dependencies

`requirements.txt` / `pyproject.toml`: `openai`, `httpx`, `requests`, `beautifulsoup4`, `python-dotenv`, `tqdm`, `pyyaml`, `colorama`. Dev: `pytest`, `pytest-cov` (optional group in `pyproject.toml`).
