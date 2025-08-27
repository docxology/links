"""
Unit tests for the organize_links module.
"""

import os
import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from src.data.organize_links import load_raw_links, categorize_links, save_organized_links


@patch('builtins.open', new_callable=mock_open, read_data='[{"url": "https://example.com/tech", "title": "Tech"}]')
def test_load_raw_links(mock_file):
    """Test loading raw links from a JSON file."""
    links = load_raw_links("urls.json")
    assert links == [{"url": "https://example.com/tech", "title": "Tech"}]
    mock_file.assert_called_once_with("urls.json", 'r', encoding='utf-8')


def test_categorize_links(sample_urls):
    """Test categorizing links by category."""
    organized = categorize_links(sample_urls)

    # Verify structure of organized links
    assert isinstance(organized, dict)
    assert "political" in organized
    assert "economic" in organized
    assert "social" in organized
    assert "technological" in organized
    assert "other" in organized

    # Verify content of organized links
    for category, links in organized.items():
        assert isinstance(links, list)
        for link in links:
            assert "url" in link
            assert "title" in link


@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
def test_save_organized_links(mock_json_dump, mock_file, sample_urls):
    """Test saving organized links to a JSON file."""
    # Organize links first
    organized = categorize_links(sample_urls)

    # Mock os.makedirs to prevent actual directory creation
    with patch('os.makedirs'):
        save_organized_links(organized, "organized_links.json")

    # Verify the file was opened for writing
    mock_file.assert_called_once_with("organized_links.json", 'w', encoding='utf-8')

    # Verify json.dump was called with the organized links
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == organized  # First arg is the data
    assert args[1] == mock_file().__enter__()  # Second arg is the file handle


@patch('src.data.organize_links.load_raw_links')
@patch('src.data.organize_links.categorize_links')
@patch('src.data.organize_links.save_organized_links')
def test_main_function(mock_save, mock_categorize, mock_load):
    """Test the main function of organize_links."""
    # Configure mocks
    mock_load.return_value = [{"url": "http://example.com", "title": "Test"}]
    mock_categorize.return_value = {"other": [{"url": "http://example.com", "title": "Test"}]}

    # Import and run main function
    from src.data.organize_links import main
    main()

    # Verify all functions were called
    mock_load.assert_called_once()
    mock_categorize.assert_called_once_with(mock_load.return_value)
    mock_save.assert_called_once() 