# `src/utils/` agent notes

## Modules

### `config.py`

- `load_dotenv()` at module import
- Creates `data/`, `output/`, `cached_data/`, `logs/` on import if missing
- Environment: `OPENAI_API_KEY`, `GPT_MODEL` (default `gpt-4`), `IMAGE_MODEL`, `ESSAY_IMAGE_MODEL` (default `dall-e-3`), `TIMEOUT` (mapped to `REQUEST_TIMEOUT`), `MAX_LINKS` (default 40), `LOG_LEVEL`
- `validate_files()`, `validate_api_key()` for production use
- `MAX_CONCURRENT_REQUESTS = 5` (hard-coded)

### `logger.py`

- `get_logger(name, log_file=None)` — returns logger with console handler and optional file handler in `LOGS_DIR`
- `log_with_emoji(logger, level, emoji_key, message)` — structured logging with emoji prefix from internal map
- `ColoredFormatter` for TTY-aware ANSI colors

### `demo_logger.py`

Demo utility only; used by root `demo_logging.py`.

## Tests

- `tests/unit/test_utils_config.py`
- `tests/unit/test_utils_logger.py`

See [`../AGENTS.md`](../AGENTS.md) for import conventions and root documentation. Central place for all configuration and logging—update here first when adding env vars or logging changes.

