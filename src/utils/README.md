# src/utils/

Shared utilities.

## Modules

- `config.py` — paths, environment (`OPENAI_API_KEY`, `GPT_MODEL`, `ESSAY_IMAGE_MODEL`, `IMAGE_MODEL`, `REQUEST_TIMEOUT`), directory creation, validation.
- `logger.py` — structured logging with emojis and colored console output.
- `demo_logger.py` — demo only.

Used by all stages. See [`config.py`](config.py) for env vars and [`logger.py`](logger.py) for `get_logger` and `log_with_emoji`.

Tested in `tests/unit/test_utils_*.py`.

See root [`../../README.md`](../../README.md).
