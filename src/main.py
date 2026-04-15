"""
CLI entry: parse argv and run the pipeline.

Stage logic lives in ``src.pipeline_orchestration``; parsing in ``src.pipeline_cli``.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.pipeline_cli import parse_pipeline_argv
from src.pipeline_orchestration import run_pipeline
from src.utils.logger import get_logger, log_with_emoji

logger = get_logger("main", "pipeline.log")


def main() -> None:
    """Parse ``sys.argv`` and run the pipeline."""
    kwargs = parse_pipeline_argv(sys.argv[1:])
    try:
        run_pipeline(**kwargs)
    except Exception as e:
        log_with_emoji(logger, "ERROR", "ERROR", f"Error in pipeline: {str(e)}")
        raise


if __name__ == "__main__":
    main()
