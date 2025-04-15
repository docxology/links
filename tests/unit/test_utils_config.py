"""
Unit tests for the config module.
"""

import os
import pytest
from pathlib import Path
from src.utils.config import (
    ROOT_DIR, DATA_DIR, OUTPUT_DIR, LOGS_DIR, 
    OPENAI_KEY, GPT_MODEL, TIMEOUT, MAX_CONCURRENT_REQUESTS
)


def test_directory_paths():
    """Test that directory paths exist and are correctly set."""
    # Test that ROOT_DIR points to the project root
    assert ROOT_DIR.exists()
    assert ROOT_DIR.is_dir()
    assert (ROOT_DIR / "src").exists()
    
    # Test that DATA_DIR is a subdirectory of ROOT_DIR
    assert DATA_DIR.exists() or DATA_DIR == ROOT_DIR / "data"
    assert DATA_DIR.parent == ROOT_DIR or DATA_DIR.parent.parent == ROOT_DIR
    
    # Test that OUTPUT_DIR is a subdirectory of ROOT_DIR
    assert OUTPUT_DIR.exists() or OUTPUT_DIR == ROOT_DIR / "output"
    assert OUTPUT_DIR.parent == ROOT_DIR or OUTPUT_DIR.parent.parent == ROOT_DIR
    
    # Test that LOGS_DIR is a subdirectory of ROOT_DIR
    assert LOGS_DIR.exists() or LOGS_DIR == ROOT_DIR / "logs"
    assert LOGS_DIR.parent == ROOT_DIR or LOGS_DIR.parent.parent == ROOT_DIR


def test_api_settings():
    """Test that API settings are set appropriately."""
    # OPENAI_KEY might be None in test environment, but it should be defined
    if os.environ.get("OPENAI_API_KEY"):
        assert OPENAI_KEY is not None
    
    # GPT_MODEL should be a string
    assert isinstance(GPT_MODEL, str)
    assert GPT_MODEL.startswith("gpt-")
    
    # TIMEOUT should be a positive integer
    assert isinstance(TIMEOUT, int)
    assert TIMEOUT > 0
    
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