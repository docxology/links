"""
Unit tests for the render_markdown module.
"""

import os
import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from src.analysis.render_markdown import (
    load_platform, generate_markdown, generate_html, save_markdown
)


def test_load_platform():
    """Test loading the platform from a JSON file."""
    # Mock data for the file
    mock_data = '{"title": "Platform", "categories": {}}'
    
    # Mock open to return the mock data
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = load_platform("platform.json")
        
        # Verify expected output
        assert result == {"title": "Platform", "categories": {}}


def test_generate_markdown(sample_platform):
    """Test generating Markdown from the platform."""
    # Call the function
    markdown = generate_markdown(sample_platform)
    
    # Verify expected output
    assert "# Sample Political Platform" in markdown
    assert "## Executive Summary" in markdown
    assert "## Political Reforms" in markdown
    assert "### Democratic Reform" in markdown
    assert "## Technology Policy" in markdown
    assert "### AI Ethics" in markdown
    
    # Verify formatting
    assert "**Description:** Improving democratic processes" in markdown
    assert "**Details:** Electoral system changes" in markdown
    assert "**Sources:**" in markdown
    assert "- [Politics Article 1](https://example.com/politics1)" in markdown


def test_generate_html(sample_platform):
    """Test generating HTML from the platform."""
    # Call the function
    html = generate_html(sample_platform)
    
    # Verify expected output
    assert "<!DOCTYPE html>" in html
    assert "<title>Sample Political Platform</title>" in html
    assert "<h1>Sample Political Platform</h1>" in html
    
    # Verify tabs are created for categories
    assert 'data-category="political"' in html
    assert 'data-category="technological"' in html
    
    # Verify content
    assert "Democratic Reform" in html
    assert "AI Ethics" in html
    assert "Data Privacy" in html
    
    # Verify styling and JavaScript
    assert "<style>" in html
    assert "<script>" in html


@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_save_markdown(mock_makedirs, mock_file, sample_platform):
    """Test saving Markdown and HTML to files."""
    # Generate markdown and HTML
    markdown = generate_markdown(sample_platform)
    html = generate_html(sample_platform)
    
    # Call the function
    output_path = save_markdown(markdown, html, "platform.md", "platform.html")
    
    # Verify directory creation
    mock_makedirs.assert_called_once()
    
    # Verify file openings
    assert mock_file.call_count == 2
    mock_file.assert_any_call("platform.md", 'w', encoding='utf-8')
    mock_file.assert_any_call("platform.html", 'w', encoding='utf-8')
    
    # Verify contents were written
    handles = mock_file.return_value.__enter__.return_value
    handles.write.assert_any_call(markdown)
    handles.write.assert_any_call(html)
    
    # Verify output path
    assert output_path == "platform.md"


@patch('src.analysis.render_markdown.load_platform')
@patch('src.analysis.render_markdown.generate_markdown')
@patch('src.analysis.render_markdown.generate_html')
@patch('src.analysis.render_markdown.save_markdown')
def test_main_function(mock_save, mock_html, mock_markdown, mock_load):
    """Test the main function of render_markdown."""
    # Setup mocks
    mock_load.return_value = {"title": "Platform", "categories": {}}
    mock_markdown.return_value = "# Platform"
    mock_html.return_value = "<html>Platform</html>"
    mock_save.return_value = "output/platform.md"
    
    # Call the function
    from src.analysis.render_markdown import main
    result = main()
    
    # Verify functions were called
    mock_load.assert_called_once()
    mock_markdown.assert_called_once_with(mock_load.return_value)
    mock_html.assert_called_once_with(mock_load.return_value)
    mock_save.assert_called_once_with(
        mock_markdown.return_value,
        mock_html.return_value,
        mock_save.call_args[0][2],
        mock_save.call_args[0][3]
    )
    
    # Verify return value
    assert result == "output/platform.md"