"""
Configuration settings for the link analysis pipeline.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "cached_data"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Input data paths
RAW_LINKS_PATH = BASE_DIR / "bestofnow_urls.json"
TAGS_JSON_PATH = BASE_DIR / "bestofnow_tags.json"

# Processed data paths
ORGANIZED_LINKS_PATH = DATA_DIR / "organized_links.json"
SCRAPED_DATA_PATH = DATA_DIR / "scraped_data.json"
EXTRACTED_CONCEPTS_PATH = OUTPUT_DIR / "extracted_concepts.json"
PLATFORM_OUTPUT_PATH = OUTPUT_DIR / "political_platform.json"
ANALYSIS_SUMMARY_PATH = OUTPUT_DIR / "analysis_summary.json"

# API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_KEY = OPENAI_API_KEY  # For backward compatibility
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gpt-image-1")  # Use GPT-Image-1 for image generation

# Scraping settings
REQUEST_TIMEOUT = int(os.getenv("TIMEOUT", 30))
# Set to 40 links for quick testing
MAX_LINKS = int(os.getenv("MAX_LINKS", 40))
MAX_CONCURRENT_REQUESTS = 5

# Logging settings
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO")
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR.upper(), logging.INFO)

def validate_files():
    """
    Validate that required input files exist.
    
    Raises:
        FileNotFoundError: If any required file is missing.
    """
    if not RAW_LINKS_PATH.exists():
        raise FileNotFoundError(f"Raw links file not found: {RAW_LINKS_PATH}")
    
    if not TAGS_JSON_PATH.exists():
        raise FileNotFoundError(f"Tags JSON file not found: {TAGS_JSON_PATH}")

def validate_api_key():
    """
    Validate that the OpenAI API key is set.
    
    Raises:
        ValueError: If the API key is not set.
    """
    if not OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key not found. "
            "Please set the OPENAI_API_KEY environment variable in a .env file."
        ) 