"""
Main script to run the entire pipeline.

This script runs all stages of the pipeline:
1. Organize links and tags
2. Scrape websites
3. Extract concepts
4. Generate political platform
5. Render platform as Markdown
6. Generate images from platform
"""

import sys
import argparse
import time
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.data.organize_links import main as organize_links_main
from src.scrapers.scrape_sites import main as scrape_sites_main
from src.analysis.extract_concepts import main as extract_concepts_main
from src.analysis.generate_platform import main as generate_platform_main
from src.analysis.render_markdown import main as render_markdown_main
from src.analysis.generate_images import main as generate_images_main
from src.utils.logger import get_logger, log_with_emoji
from src.utils.config import PLATFORM_OUTPUT_PATH, EXTRACTED_CONCEPTS_PATH

# Set up logger
logger = get_logger("main", "pipeline.log")

def run_pipeline(skip_organize=False, skip_scrape=False, skip_extract=False, skip_analyze=False, skip_render=False, skip_images=False):
    """
    Run the entire pipeline or specific stages.
    
    Args:
        skip_organize (bool, optional): Skip the organize links stage. Defaults to False.
        skip_scrape (bool, optional): Skip the scrape websites stage. Defaults to False.
        skip_extract (bool, optional): Skip the concept extraction stage. Defaults to False.
        skip_analyze (bool, optional): Skip the generate platform stage. Defaults to False.
        skip_render (bool, optional): Skip the Markdown rendering stage. Defaults to False.
        skip_images (bool, optional): Skip the image generation stage. Defaults to False.
    """
    start_time = time.time()
    
    log_with_emoji(logger, 'INFO', 'START', "Starting pipeline")
    
    # Stage 1: Organize links and tags
    if not skip_organize:
        log_with_emoji(logger, 'INFO', 'PROCESSING', "Stage 1: Organizing links and tags")
        organize_links_main()
        log_with_emoji(logger, 'INFO', 'COMPLETE', "Stage 1 completed")
    else:
        log_with_emoji(logger, 'INFO', 'SKIPPED', "Skipping Stage 1: Organizing links and tags")
    
    # Stage 2: Scrape websites
    if not skip_scrape:
        log_with_emoji(logger, 'INFO', 'SCRAPING', "Stage 2: Scraping websites")
        scrape_sites_main()
        log_with_emoji(logger, 'INFO', 'COMPLETE', "Stage 2 completed")
    else:
        log_with_emoji(logger, 'INFO', 'SKIPPED', "Skipping Stage 2: Scraping websites")
    
    # Stage 3: Extract concepts
    if not skip_extract:
        log_with_emoji(logger, 'INFO', 'EXTRACTING', "Stage 3: Extracting concepts")
        extract_concepts_main()
        log_with_emoji(logger, 'INFO', 'COMPLETE', f"Stage 3 completed. Concepts saved to {EXTRACTED_CONCEPTS_PATH}")
    else:
        log_with_emoji(logger, 'INFO', 'SKIPPED', "Skipping Stage 3: Extracting concepts")
    
    # Stage 4: Generate political platform
    if not skip_analyze:
        log_with_emoji(logger, 'INFO', 'ANALYZING', "Stage 4: Generating political platform")
        generate_platform_main()
        log_with_emoji(logger, 'INFO', 'COMPLETE', f"Stage 4 completed. Platform saved to {PLATFORM_OUTPUT_PATH}")
    else:
        log_with_emoji(logger, 'INFO', 'SKIPPED', "Skipping Stage 4: Generating political platform")
    
    # Stage 5: Render platform as Markdown
    if not skip_render:
        log_with_emoji(logger, 'INFO', 'RENDERING', "Stage 5: Rendering platform as Markdown")
        markdown_path = render_markdown_main()
        log_with_emoji(logger, 'INFO', 'COMPLETE', f"Stage 5 completed. Markdown saved to {markdown_path}")
    else:
        log_with_emoji(logger, 'INFO', 'SKIPPED', "Skipping Stage 5: Rendering platform as Markdown")
    
    # Stage 6: Generate images from platform
    if not skip_images:
        log_with_emoji(logger, 'INFO', 'GENERATING', "Stage 6: Generating images from platform")
        images_dir = generate_images_main()
        log_with_emoji(logger, 'INFO', 'COMPLETE', f"Stage 6 completed. Images saved to {images_dir}")
    else:
        log_with_emoji(logger, 'INFO', 'SKIPPED', "Skipping Stage 6: Generating images from platform")
    
    end_time = time.time()
    duration = end_time - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        time_str = f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"
    elif minutes > 0:
        time_str = f"{int(minutes)}m {seconds:.2f}s"
    else:
        time_str = f"{seconds:.2f}s"
    
    log_with_emoji(logger, 'INFO', 'COMPLETE', f"Pipeline completed in {time_str}")

def main():
    """
    Main function to parse arguments and run the pipeline.
    """
    parser = argparse.ArgumentParser(description="Run the links analysis pipeline")
    parser.add_argument("--skip-organize", action="store_true", help="Skip the organize links stage")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip the scrape websites stage")
    parser.add_argument("--skip-extract", action="store_true", help="Skip the concept extraction stage")
    parser.add_argument("--skip-analyze", action="store_true", help="Skip the generate platform stage")
    parser.add_argument("--skip-render", action="store_true", help="Skip the Markdown rendering stage")
    parser.add_argument("--skip-images", action="store_true", help="Skip the image generation stage")
    parser.add_argument("--only-organize", action="store_true", help="Run only the organize links stage")
    parser.add_argument("--only-scrape", action="store_true", help="Run only the scrape websites stage")
    parser.add_argument("--only-extract", action="store_true", help="Run only the concept extraction stage")
    parser.add_argument("--only-analyze", action="store_true", help="Run only the generate platform stage")
    parser.add_argument("--only-render", action="store_true", help="Run only the Markdown rendering stage")
    parser.add_argument("--only-images", action="store_true", help="Run only the image generation stage")
    
    args = parser.parse_args()
    
    # Handle "only" flags
    if args.only_organize:
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
    if args.only_scrape:
        args.skip_organize = True
        args.skip_extract = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
    if args.only_extract:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_analyze = True
        args.skip_render = True
        args.skip_images = True
    if args.only_analyze:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_render = True
        args.skip_images = True
    if args.only_render:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_analyze = True
        args.skip_images = True
    if args.only_images:
        args.skip_organize = True
        args.skip_scrape = True
        args.skip_extract = True
        args.skip_analyze = True
        args.skip_render = True
    
    try:
        run_pipeline(
            skip_organize=args.skip_organize,
            skip_scrape=args.skip_scrape,
            skip_extract=args.skip_extract,
            skip_analyze=args.skip_analyze,
            skip_render=args.skip_render,
            skip_images=args.skip_images
        )
    except Exception as e:
        log_with_emoji(logger, 'ERROR', 'ERROR', f"Error in pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main() 