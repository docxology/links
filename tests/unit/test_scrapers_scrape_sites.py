"""
Unit tests for the scrape_sites module.
"""

import os
import json
import pytest
from unittest.mock import patch, Mock, MagicMock, mock_open
from src.scrapers.scrape_sites import (
    load_organized_links, scrape_url, scrape_links, save_scraped_data,
    extract_meaningful_content, get_cache_path, is_cached
)


def test_load_organized_links():
    """Test loading organized links from a file."""
    # Create a mock for open
    mock_data = '{"tech": [{"url": "https://example.com", "title": "Example", "tags": ["tag1"]}]}'
    with patch('builtins.open', mock_open(read_data=mock_data)):
        # Call the function
        links = load_organized_links('organized_links.json')
        
        # Verify expected output
        assert links == {"tech": [{"url": "https://example.com", "title": "Example", "tags": ["tag1"]}]}


@patch('src.scrapers.scrape_sites.BeautifulSoup')
def test_extract_meaningful_content(mock_bs4):
    """Test extracting meaningful content from BeautifulSoup object."""
    # Setup mock soup object
    mock_soup = MagicMock()
    mock_title_tag = MagicMock()
    mock_title_tag.get_text.return_value = "Test Page"
    mock_soup.find.return_value = mock_title_tag

    # Mock find_all to handle different arguments
    def mock_find_all(tag, **kwargs):
        if tag == 'p':
            return [MagicMock(get_text=lambda: "Paragraph 1"), MagicMock(get_text=lambda: "Paragraph 2")]
        elif tag == 'h1':
            return [MagicMock(get_text=lambda: "Main Heading")]
        elif tag == 'h2':
            return [MagicMock(get_text=lambda: "Subheading")]
        elif tag == 'li':
            return [MagicMock(get_text=lambda: "Item 1"), MagicMock(get_text=lambda: "Item 2")]
        elif tag == 'meta' and 'property' in kwargs:
            return []
        elif tag == 'meta' and 'name' in kwargs:
            return []
        return []

    mock_soup.find_all = mock_find_all
    mock_bs4.return_value = mock_soup

    # Call the function
    content = extract_meaningful_content(mock_soup)

    # Verify expected output structure
    assert "title" in content
    assert "paragraphs" in content
    assert "headings" in content
    assert "list_items" in content
    assert "metadata" in content


@patch('src.scrapers.scrape_sites.requests.get')
@patch('src.scrapers.scrape_sites.BeautifulSoup')
@patch('src.scrapers.scrape_sites.extract_meaningful_content')
@patch('src.scrapers.scrape_sites.cache_content')
@patch('src.scrapers.scrape_sites.is_cached')
def test_scrape_url_success(mock_is_cached, mock_cache, mock_extract, mock_bs4, mock_get):
    """Test scraping URL successfully."""
    # Setup mocks
    mock_is_cached.return_value = False
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html>Test</html>"
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    mock_soup = MagicMock()
    mock_bs4.return_value = mock_soup

    mock_extract.return_value = {
        "title": "Test Title",
        "paragraphs": ["Test content"],
        "headings": ["Test heading"],
        "list_items": ["Item 1"],
        "metadata": {}
    }

    # Call the function
    result = scrape_url("https://example.com")

    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["status"] == "success"
    assert "content" in result
    assert result["content"]["title"] == "Test Title"


@patch('requests.get')
def test_scrape_url_failure(mock_get):
    """Test scraping URL with failure."""
    # Setup mock to raise a RequestException (which is what the function catches)
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")

    # Call the function
    result = scrape_url("https://example.com")

    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["status"] == "error"
    assert "Connection error" in result["error"]


def test_get_cache_path():
    """Test getting cache path for URL."""
    path = get_cache_path("https://example.com/test")
    assert "cached_data" in str(path)
    assert "example.com_test" in str(path)


@patch('os.path.exists')
def test_is_cached(mock_exists):
    """Test checking if URL is cached."""
    mock_exists.return_value = True
    assert is_cached("https://example.com") == True

    mock_exists.return_value = False
    assert is_cached("https://example.com") == False


@patch('src.scrapers.scrape_sites.scrape_url')
@patch('tqdm.tqdm')
def test_scrape_links(mock_tqdm, mock_scrape_url):
    """Test scraping multiple links."""
    # Setup mock to return sample data
    mock_scrape_url.side_effect = [
        {"url": "https://example.com/1", "status": "success", "content": {"title": "Test 1"}},
        {"url": "https://example.com/2", "status": "error", "error": "Failed"}
    ]

    # Create sample organized links
    organized_links = {
        "category": [
            {"url": "https://example.com/1", "title": "Example 1", "tags": ["tag1"]},
            {"url": "https://example.com/2", "title": "Example 2", "tags": ["tag2"]}
        ]
    }

    # Setup mock progress bar
    mock_progress_bar = MagicMock()
    mock_tqdm.return_value = mock_progress_bar

    # Call the function
    results = scrape_links(organized_links)

    # Verify expected output
    assert "category" in results
    assert len(results["category"]) == 2
    assert results["category"][0]["url"] == "https://example.com/1"
    assert results["category"][0]["status"] == "success"
    assert results["category"][1]["url"] == "https://example.com/2"
    assert results["category"][1]["status"] == "error"

    # Verify mock was called twice
    assert mock_scrape_url.call_count == 2


@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
@patch('os.makedirs')
def test_save_scraped_data(mock_makedirs, mock_json_dump, mock_file):
    """Test saving scraped data to a file."""
    # Create sample data with proper structure for text extraction
    data = {"category": [{"url": "https://example.com", "status": "success", "content": {"title": "Test", "paragraphs": ["test content"]}}]}

    # Call the function
    save_scraped_data(data, "scraped_data.json")

    # Verify directory creation
    mock_makedirs.assert_called_once()

    # Verify file openings (should open 2 files: JSON and text extract)
    assert mock_file.call_count == 2
    mock_file.assert_any_call("scraped_data.json", 'w', encoding='utf-8')
    mock_file.assert_any_call("scraped_data_text_extract.txt", 'w', encoding='utf-8')

    # Verify JSON dumping
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == data 