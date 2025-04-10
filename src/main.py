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
from src.utils.logger import get_logger
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
    
    logger.info("Starting pipeline")
    
    # Stage 1: Organize links and tags
    if not skip_organize:
        logger.info("Stage 1: Organizing links and tags")
        organize_links_main()
        logger.info("Stage 1 completed")
    else:
        logger.info("Skipping Stage 1: Organizing links and tags")
    
    # Stage 2: Scrape websites
    if not skip_scrape:
        logger.info("Stage 2: Scraping websites")
        scrape_sites_main()
        logger.info("Stage 2 completed")
    else:
        logger.info("Skipping Stage 2: Scraping websites")
    
    # Stage 3: Extract concepts
    if not skip_extract:
        logger.info("Stage 3: Extracting concepts")
        extract_concepts_main()
        logger.info(f"Stage 3 completed. Concepts saved to {EXTRACTED_CONCEPTS_PATH}")
    else:
        logger.info("Skipping Stage 3: Extracting concepts")
    
    # Stage 4: Generate political platform
    if not skip_analyze:
        logger.info("Stage 4: Generating political platform")
        generate_platform_main()
        logger.info(f"Stage 4 completed. Platform saved to {PLATFORM_OUTPUT_PATH}")
    else:
        logger.info("Skipping Stage 4: Generating political platform")
    
    # Stage 5: Render platform as Markdown
    if not skip_render:
        logger.info("Stage 5: Rendering platform as Markdown")
        markdown_path = render_markdown_main()
        logger.info(f"Stage 5 completed. Markdown saved to {markdown_path}")
    else:
        logger.info("Skipping Stage 5: Rendering platform as Markdown")
    
    # Stage 6: Generate images from platform
    if not skip_images:
        logger.info("Stage 6: Generating images from platform")
        images_dir = generate_images_main()
        logger.info(f"Stage 6 completed. Images saved to {images_dir}")
    else:
        logger.info("Skipping Stage 6: Generating images from platform")
    
    end_time = time.time()
    logger.info(f"Pipeline completed in {end_time - start_time:.2f} seconds")

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
        logger.error(f"Error in pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main() 