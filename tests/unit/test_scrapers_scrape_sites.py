"""
Unit tests for the scrape_sites module.
"""

import os
import json
import pytest
from unittest.mock import patch, Mock, MagicMock
from src.scrapers.scrape_sites import (
    load_organized_links, fetch_page_content, extract_content,
    scrape_website, process_websites, save_scraped_data
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


@patch('requests.get')
def test_fetch_page_content_success(mock_get):
    """Test fetching page content successfully."""
    # Setup mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><h1>Test Page</h1><p>Test content</p></body></html>"
    mock_get.return_value = mock_response
    
    # Call the function
    status, content = fetch_page_content("https://example.com")
    
    # Verify expected output
    assert status == "success"
    assert content == "<html><body><h1>Test Page</h1><p>Test content</p></body></html>"
    mock_get.assert_called_once_with("https://example.com", timeout=30)


@patch('requests.get')
def test_fetch_page_content_failure(mock_get):
    """Test fetching page content with a failure."""
    # Setup mock to raise an exception
    mock_get.side_effect = Exception("Connection error")
    
    # Call the function
    status, content = fetch_page_content("https://example.com")
    
    # Verify expected output
    assert status == "error"
    assert "Connection error" in content
    mock_get.assert_called_once_with("https://example.com", timeout=30)


def test_extract_content():
    """Test extracting content from HTML."""
    # Create test HTML
    html = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <header>Header content</header>
            <h1>Main Heading</h1>
            <h2>Subheading</h2>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
            <footer>Footer content</footer>
        </body>
    </html>
    """
    
    # Call the function
    content = extract_content(html)
    
    # Verify expected output
    assert "title" in content
    assert content["title"] == "Test Page"
    
    assert "headings" in content
    assert len(content["headings"]) == 2
    assert content["headings"][0]["text"] == "Main Heading"
    assert content["headings"][0]["level"] == 1
    assert content["headings"][1]["text"] == "Subheading"
    assert content["headings"][1]["level"] == 2
    
    assert "paragraphs" in content
    assert len(content["paragraphs"]) == 2
    assert "Paragraph 1" in content["paragraphs"]
    assert "Paragraph 2" in content["paragraphs"]
    
    assert "lists" in content
    assert len(content["lists"]) == 1
    assert len(content["lists"][0]["items"]) == 2
    assert "Item 1" in content["lists"][0]["items"]
    assert "Item 2" in content["lists"][0]["items"]


@patch('src.scrapers.scrape_sites.fetch_page_content')
@patch('src.scrapers.scrape_sites.extract_content')
def test_scrape_website_success(mock_extract, mock_fetch):
    """Test scraping a website successfully."""
    # Setup mocks
    mock_fetch.return_value = ("success", "<html></html>")
    mock_extract.return_value = {"title": "Test", "paragraphs": ["Test paragraph"]}
    
    # Create sample link
    link = {"url": "https://example.com", "title": "Example", "tags": ["tag1"]}
    
    # Call the function
    result = scrape_website(link)
    
    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["title"] == "Example"
    assert result["status"] == "success"
    assert "content" in result
    assert result["content"]["title"] == "Test"
    assert "Test paragraph" in result["content"]["paragraphs"]
    
    # Verify mocks were called
    mock_fetch.assert_called_once_with("https://example.com")
    mock_extract.assert_called_once_with("<html></html>")


@patch('src.scrapers.scrape_sites.fetch_page_content')
def test_scrape_website_failure(mock_fetch):
    """Test scraping a website with a failure."""
    # Setup mock to return an error
    mock_fetch.return_value = ("error", "Failed to fetch")
    
    # Create sample link
    link = {"url": "https://example.com", "title": "Example", "tags": ["tag1"]}
    
    # Call the function
    result = scrape_website(link)
    
    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["title"] == "Example"
    assert result["status"] == "error"
    assert result["error"] == "Failed to fetch"
    
    # Verify mock was called
    mock_fetch.assert_called_once_with("https://example.com")


@patch('src.scrapers.scrape_sites.scrape_website')
def test_process_websites(mock_scrape):
    """Test processing multiple websites."""
    # Setup mock to return sample data
    mock_scrape.side_effect = [
        {"url": "https://example.com/1", "status": "success", "content": {"title": "Test 1"}},
        {"url": "https://example.com/2", "status": "error", "error": "Failed"}
    ]
    
    # Create sample links
    links = {
        "category": [
            {"url": "https://example.com/1", "title": "Example 1", "tags": ["tag1"]},
            {"url": "https://example.com/2", "title": "Example 2", "tags": ["tag2"]}
        ]
    }
    
    # Call the function with a mock progress bar
    with patch('tqdm.tqdm') as mock_tqdm:
        mock_tqdm.return_value.__iter__.return_value = range(2)
        results = process_websites(links)
    
    # Verify expected output
    assert "category" in results
    assert len(results["category"]) == 2
    assert results["category"][0]["url"] == "https://example.com/1"
    assert results["category"][0]["status"] == "success"
    assert results["category"][1]["url"] == "https://example.com/2"
    assert results["category"][1]["status"] == "error"
    
    # Verify mock was called twice
    assert mock_scrape.call_count == 2


@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
@patch('os.makedirs')
def test_save_scraped_data(mock_makedirs, mock_json_dump, mock_file):
    """Test saving scraped data to a file."""
    # Create sample data
    data = {"category": [{"url": "https://example.com", "status": "success"}]}
    
    # Call the function
    save_scraped_data(data, "scraped_data.json")
    
    # Verify directory creation
    mock_makedirs.assert_called_once()
    
    # Verify file opening
    mock_file.assert_called_once_with("scraped_data.json", 'w', encoding='utf-8')
    
    # Verify JSON dumping
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == data 