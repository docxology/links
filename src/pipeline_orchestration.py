"""
Composable pipeline execution: inject PipelineStages for testing without unittest.mock.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable

from src.data.organize_links import main as organize_links_main
from src.scrapers.scrape_sites import main as scrape_sites_main
from src.analysis.extract_concepts import main as extract_concepts_main
from src.analysis.organize_extractions import main as organize_extractions_main
from src.analysis.generate_essays import main as generate_essays_main
from src.analysis.generate_essay_images import main as generate_essay_images_main
from src.analysis.generate_platform import main as generate_platform_main
from src.analysis.render_markdown import main as render_markdown_main
from src.analysis.generate_images import main as generate_images_main
from src.utils.logger import get_logger, log_with_emoji
from src.utils.config import PLATFORM_OUTPUT_PATH, EXTRACTED_CONCEPTS_PATH

logger = get_logger("main", "pipeline.log")


@dataclass
class PipelineStages:
    """Nine stage entry points (default: production mains)."""

    organize: Callable[[], Any] = organize_links_main
    scrape: Callable[[], Any] = scrape_sites_main
    extract: Callable[[], Any] = extract_concepts_main
    organize_extractions: Callable[[], Any] = organize_extractions_main
    essays: Callable[[], Any] = generate_essays_main
    essay_images: Callable[[], Any] = generate_essay_images_main
    analyze: Callable[[], Any] = generate_platform_main
    render: Callable[[], Any] = render_markdown_main
    images: Callable[[], Any] = generate_images_main


def run_pipeline(
    skip_organize: bool = False,
    skip_scrape: bool = False,
    skip_extract: bool = False,
    skip_organize_extractions: bool = False,
    skip_essays: bool = False,
    skip_essay_images: bool = False,
    skip_analyze: bool = False,
    skip_render: bool = False,
    skip_images: bool = False,
    stages: PipelineStages | None = None,
) -> None:
    """
    Run pipeline stages. Pass ``stages`` with test callables to avoid heavy work in tests.
    """
    stages = stages or PipelineStages()
    start_time = time.time()

    log_with_emoji(logger, "INFO", "START", "Starting pipeline")

    if not skip_organize:
        log_with_emoji(logger, "INFO", "PROCESSING", "Stage 1: Organizing links and tags")
        stages.organize()
        log_with_emoji(logger, "INFO", "COMPLETE", "Stage 1 completed")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 1: Organizing links and tags")

    if not skip_scrape:
        log_with_emoji(logger, "INFO", "SCRAPING", "Stage 2: Scraping websites")
        stages.scrape()
        log_with_emoji(logger, "INFO", "COMPLETE", "Stage 2 completed")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 2: Scraping websites")

    if not skip_extract:
        log_with_emoji(logger, "INFO", "EXTRACTING", "Stage 3: Extracting Principles, Policies, Values, Goals")
        stages.extract()
        log_with_emoji(logger, "INFO", "COMPLETE", f"Stage 3 completed. Categories saved to {EXTRACTED_CONCEPTS_PATH}")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 3: Extracting Principles, Policies, Values, Goals")

    if not skip_organize_extractions:
        log_with_emoji(logger, "INFO", "ORGANIZING", "Stage 4: Organizing extractions into site-specific and compiled formats")
        organize_result = stages.organize_extractions() or {}
        log_with_emoji(
            logger,
            "INFO",
            "COMPLETE",
            f"Stage 4 completed. Site-specific: {organize_result.get('site_specific_dir', 'N/A')}, Compiled: {organize_result.get('compiled_dir', 'N/A')}",
        )
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 4: Organizing extractions")

    if not skip_essays:
        log_with_emoji(logger, "INFO", "WRITING", "Stage 5: Generating overview essays")
        essays_result = stages.essays() or {}
        log_with_emoji(logger, "INFO", "COMPLETE", f"Stage 5 completed. Essays saved to {essays_result.get('essays_dir', 'N/A')}")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 5: Generating essays")

    if not skip_essay_images:
        log_with_emoji(logger, "INFO", "GENERATING", "Stage 6: Generating images from essays")
        images_result = stages.essay_images() or {}
        log_with_emoji(logger, "INFO", "COMPLETE", f"Stage 6 completed. Images saved to {images_result.get('images_dir', 'N/A')}")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 6: Generating essay images")

    if not skip_analyze:
        log_with_emoji(logger, "INFO", "ANALYZING", "Stage 7: Generating political platform")
        stages.analyze()
        log_with_emoji(logger, "INFO", "COMPLETE", f"Stage 7 completed. Platform saved to {PLATFORM_OUTPUT_PATH}")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 7: Generating political platform")

    if not skip_render:
        log_with_emoji(logger, "INFO", "RENDERING", "Stage 8: Rendering platform as Markdown")
        render_out = stages.render()
        if isinstance(render_out, tuple):
            markdown_path, html_path = render_out[0], render_out[1]
            log_with_emoji(
                logger,
                "INFO",
                "COMPLETE",
                f"Stage 8 completed. Markdown: {markdown_path}, HTML: {html_path}",
            )
        else:
            log_with_emoji(logger, "INFO", "COMPLETE", f"Stage 8 completed. Markdown saved to {render_out}")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 8: Rendering platform as Markdown")

    if not skip_images:
        log_with_emoji(logger, "INFO", "GENERATING", "Stage 9: Generating images from platform")
        images_dir = stages.images()
        log_with_emoji(logger, "INFO", "COMPLETE", f"Stage 9 completed. Images saved to {images_dir}")
    else:
        log_with_emoji(logger, "INFO", "SKIPPED", "Skipping Stage 9: Generating images from platform")

    duration = time.time() - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        time_str = f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"
    elif minutes > 0:
        time_str = f"{int(minutes)}m {seconds:.2f}s"
    else:
        time_str = f"{seconds:.2f}s"

    log_with_emoji(logger, "INFO", "COMPLETE", f"Pipeline completed in {time_str}")
