"""
Unit tests for the render_markdown module.
"""

import os
import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from src.analysis.render_markdown import (
    load_platform_data, render_markdown, render_html, save_markdown
)


def test_load_platform_data():
    """Test loading the platform data from a JSON file."""
    # Mock data for the file
    mock_data = '{"title": "Platform", "executive_summary": "Test summary"}'

    # Mock open to return the mock data
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = load_platform_data("platform.json")

        # Verify expected output
        assert result == {"title": "Platform", "executive_summary": "Test summary"}


def test_render_markdown(sample_platform):
    """Test rendering Markdown from the platform."""
    # Call the function
    markdown = render_markdown(sample_platform)
    
    # Verify expected output
    assert "# Political Platform" in markdown
    assert "## Executive Summary" in markdown

    # Verify that the executive summary content is included
    assert "This is a sample political platform for testing." in markdown

    # Verify footer
    assert "*This political platform was generated based on analysis of multiple sources" in markdown


def test_render_html(sample_platform):
    """Test rendering HTML from the platform."""
    # Call the function
    html = render_html(sample_platform)
    
    # Verify expected output
    assert "<!DOCTYPE html>" in html
    assert "<title>Political Platform</title>" in html
    assert "<h1>Political Platform</h1>" in html

    # Verify executive summary section
    assert "Executive Summary" in html
    assert "This is a sample political platform for testing." in html

    # Verify styling
    assert "<style>" in html

    # Verify footer
    assert "This political platform was generated based on analysis of multiple sources" in html


@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_save_markdown(mock_makedirs, mock_file, sample_platform):
    """Test saving Markdown to a file."""
    # Generate markdown
    markdown = render_markdown(sample_platform)

    # Call the function
    save_markdown(markdown, "platform.md")

    # Verify directory creation
    mock_makedirs.assert_called_once()

    # Verify file opening
    mock_file.assert_called_once_with("platform.md", 'w', encoding='utf-8')

    # Verify content was written
    handle = mock_file.return_value.__enter__.return_value
    handle.write.assert_called_once_with(markdown)


@patch('src.analysis.render_markdown.load_platform_data')
@patch('src.analysis.render_markdown.render_markdown')
@patch('src.analysis.render_markdown.render_html')
@patch('src.analysis.render_markdown.save_markdown')
@patch('src.analysis.render_markdown.save_html')
def test_main_function(mock_save_html, mock_save_md, mock_html, mock_md, mock_load):
    """Test the main function of render_markdown."""
    # Setup mocks
    mock_load.return_value = {"title": "Platform", "executive_summary": "Test"}
    mock_md.return_value = "# Platform"
    mock_html.return_value = "<html>Platform</html>"

    # Call the function
    from src.analysis.render_markdown import main
    result = main()

    # Verify functions were called
    mock_load.assert_called_once()
    mock_md.assert_called_once_with(mock_load.return_value)
    mock_html.assert_called_once_with(mock_load.return_value)
    mock_save_md.assert_called_once()
    mock_save_html.assert_called_once()

    # Verify return value is a tuple of paths
    assert isinstance(result, tuple)
    assert len(result) == 2