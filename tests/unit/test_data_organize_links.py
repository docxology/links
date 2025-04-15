"""
Unit tests for the organize_links module.
"""

import os
import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from src.data.organize_links import load_urls, load_tags, organize_links_by_category, save_organized_links


@patch('builtins.open', new_callable=mock_open, read_data='{"tech": [{"url": "https://example.com/tech", "title": "Tech"}]}')
def test_load_urls(mock_file):
    """Test loading URLs from a JSON file."""
    urls = load_urls("urls.json")
    assert urls == {"tech": [{"url": "https://example.com/tech", "title": "Tech"}]}
    mock_file.assert_called_once_with("urls.json", 'r', encoding='utf-8')


@patch('builtins.open', new_callable=mock_open, read_data='{"https://example.com/tech": ["technology"]}')
def test_load_tags(mock_file):
    """Test loading tags from a JSON file."""
    tags = load_tags("tags.json")
    assert tags == {"https://example.com/tech": ["technology"]}
    mock_file.assert_called_once_with("tags.json", 'r', encoding='utf-8')


def test_organize_links_by_category(sample_urls, sample_tags):
    """Test organizing links by category."""
    organized = organize_links_by_category(sample_urls, sample_tags)
    
    # Verify structure of organized links
    assert isinstance(organized, dict)
    assert "tech" in organized
    assert "politics" in organized
    
    # Verify content of organized links
    for category, links in organized.items():
        assert isinstance(links, list)
        for link in links:
            assert "url" in link
            assert "title" in link
            assert "tags" in link
            assert isinstance(link["tags"], list)


@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
def test_save_organized_links(mock_json_dump, mock_file, sample_urls, sample_tags):
    """Test saving organized links to a JSON file."""
    # Organize links first
    organized = organize_links_by_category(sample_urls, sample_tags)
    
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


@patch('src.data.organize_links.load_urls')
@patch('src.data.organize_links.load_tags')
@patch('src.data.organize_links.organize_links_by_category')
@patch('src.data.organize_links.save_organized_links')
def test_main_function(mock_save, mock_organize, mock_load_tags, mock_load_urls):
    """Test the main function of organize_links."""
    # Configure mocks
    mock_load_urls.return_value = {"category": [{"url": "http://example.com"}]}
    mock_load_tags.return_value = {"http://example.com": ["tag1", "tag2"]}
    mock_organize.return_value = {"category": [{"url": "http://example.com", "tags": ["tag1", "tag2"]}]}
    
    # Import and run main function
    from src.data.organize_links import main
    main()
    
    # Verify all functions were called
    mock_load_urls.assert_called_once()
    mock_load_tags.assert_called_once()
    mock_organize.assert_called_once_with(
        mock_load_urls.return_value, mock_load_tags.return_value
    )
    mock_save.assert_called_once() 