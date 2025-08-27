"""
Unit tests for the config module.
"""

import os
import pytest
from pathlib import Path
from src.utils.config import (
    BASE_DIR, DATA_DIR, OUTPUT_DIR, LOGS_DIR,
    OPENAI_KEY, GPT_MODEL, REQUEST_TIMEOUT, MAX_CONCURRENT_REQUESTS
)


def test_directory_paths():
    """Test that directory paths exist and are correctly set."""
    # Test that BASE_DIR points to the project root
    assert BASE_DIR.exists()
    assert BASE_DIR.is_dir()
    assert (BASE_DIR / "src").exists()

    # Test that DATA_DIR is a subdirectory of BASE_DIR
    assert DATA_DIR.exists() or DATA_DIR == BASE_DIR / "data"
    assert DATA_DIR.parent == BASE_DIR or DATA_DIR.parent.parent == BASE_DIR

    # Test that OUTPUT_DIR is a subdirectory of BASE_DIR
    assert OUTPUT_DIR.exists() or OUTPUT_DIR == BASE_DIR / "output"
    assert OUTPUT_DIR.parent == BASE_DIR or OUTPUT_DIR.parent.parent == BASE_DIR

    # Test that LOGS_DIR is a subdirectory of BASE_DIR
    assert LOGS_DIR.exists() or LOGS_DIR == BASE_DIR / "logs"
    assert LOGS_DIR.parent == BASE_DIR or LOGS_DIR.parent.parent == BASE_DIR


def test_api_settings():
    """Test that API settings are set appropriately."""
    # OPENAI_KEY might be None in test environment, but it should be defined
    if os.environ.get("OPENAI_API_KEY"):
        assert OPENAI_KEY is not None
    
    # GPT_MODEL should be a string
    assert isinstance(GPT_MODEL, str)
    assert GPT_MODEL.startswith("gpt-")
    
    # REQUEST_TIMEOUT should be a positive integer
    assert isinstance(REQUEST_TIMEOUT, int)
    assert REQUEST_TIMEOUT > 0
    
    # MAX_CONCURRENT_REQUESTS should be a positive integer
    assert isinstance(MAX_CONCURRENT_REQUESTS, int)
    assert MAX_CONCURRENT_REQUESTS > 0


def test_file_paths():
    """Test that file paths are defined correctly."""
    # Test that file paths are Path objects
    from src.utils.config import ORGANIZED_LINKS_PATH, SCRAPED_DATA_PATH
    assert isinstance(ORGANIZED_LINKS_PATH, Path)
    assert isinstance(SCRAPED_DATA_PATH, Path)
    
    # Test that paths are in the correct directories
    assert ORGANIZED_LINKS_PATH.parent == DATA_DIR
    assert SCRAPED_DATA_PATH.parent == DATA_DIR 