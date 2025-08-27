"""
Integration tests for the links analysis pipeline.

These tests verify that the different stages of the pipeline work together correctly.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


@pytest.fixture
def setup_test_data(tmp_path, sample_urls, sample_tags):
    """Set up test data files for the pipeline."""
    # Create sample JSON files in the temporary directory
    urls_path = tmp_path / "bestofnow_urls.json"
    tags_path = tmp_path / "bestofnow_tags.json"
    
    with open(urls_path, 'w', encoding='utf-8') as f:
        json.dump(sample_urls, f)
    
    with open(tags_path, 'w', encoding='utf-8') as f:
        json.dump(sample_tags, f)
    
    # Create necessary directories
    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    return {
        "tmp_path": tmp_path,
        "urls_path": urls_path,
        "tags_path": tags_path,
        "data_dir": data_dir,
        "output_dir": output_dir,
        "logs_dir": logs_dir
    }


@patch('src.data.organize_links.save_organized_links')
def test_organize_links_integration(mock_save, setup_test_data):
    """Test the organize_links module in an integration context."""
    # Override the input file paths
    with patch('src.data.organize_links.URLS_PATH', setup_test_data["urls_path"]), \
         patch('src.data.organize_links.TAGS_PATH', setup_test_data["tags_path"]), \
         patch('src.utils.config.ORGANIZED_LINKS_PATH', setup_test_data["data_dir"] / "organized_links.json"):
        
        # Import and run the main function
        from src.data.organize_links import main
        main()
        
        # Verify that save_organized_links was called with the expected data
        mock_save.assert_called_once()
        organized_links = mock_save.call_args[0][0]
        
        # Verify structure
        assert "tech" in organized_links
        assert "politics" in organized_links
        
        # Verify content
        for category, links in organized_links.items():
            for link in links:
                assert "url" in link
                assert "title" in link
                assert "tags" in link


@patch('src.scrapers.scrape_sites.process_websites')
@patch('src.scrapers.scrape_sites.save_scraped_data')
def test_scrape_sites_integration(mock_save, mock_process, setup_test_data, sample_urls):
    """Test the scrape_sites module in an integration context."""
    # Create a sample organized links file
    organized_links_path = setup_test_data["data_dir"] / "organized_links.json"
    with open(organized_links_path, 'w', encoding='utf-8') as f:
        json.dump(sample_urls, f)
    
    # Mock the process_websites function to return sample data
    mock_process.return_value = {
        "tech": [
            {"url": "https://example.com/tech1", "status": "success", "content": {"title": "Tech 1"}}
        ],
        "politics": [
            {"url": "https://example.com/politics1", "status": "success", "content": {"title": "Politics 1"}}
        ]
    }
    
    # Override config paths
    with patch('src.utils.config.ORGANIZED_LINKS_PATH', organized_links_path), \
         patch('src.utils.config.SCRAPED_DATA_PATH', setup_test_data["data_dir"] / "scraped_data.json"):
        
        # Import and run the main function
        from src.scrapers.scrape_sites import main
        main()
        
        # Verify that process_websites was called with the organized links
        mock_process.assert_called_once()
        assert mock_process.call_args[0][0] == sample_urls
        
        # Verify that save_scraped_data was called with the processed data
        mock_save.assert_called_once_with(mock_process.return_value, mock_save.call_args[0][1])


@patch('src.analysis.extract_concepts.extract_concepts')
@patch('src.analysis.extract_concepts.save_extracted_concepts')
def test_extract_concepts_integration(mock_save, mock_extract, setup_test_data, sample_scraped_data):
    """Test the extract_concepts module in an integration context."""
    # Create a sample scraped data file
    scraped_data_path = setup_test_data["data_dir"] / "scraped_data.json"
    with open(scraped_data_path, 'w', encoding='utf-8') as f:
        json.dump(sample_scraped_data, f)
    
    # Mock the extract_concepts function to return sample data
    mock_extract.return_value = {
        "tech": [
            {
                "url": "https://example.com/tech1",
                "title": "Tech Article 1",
                "status": "success",
                "concepts": "AI Ethics: Establishing ethical guidelines"
            }
        ]
    }
    
    # Override config paths
    with patch('src.utils.config.SCRAPED_DATA_PATH', scraped_data_path), \
         patch('src.utils.config.EXTRACTED_CONCEPTS_PATH', setup_test_data["output_dir"] / "extracted_concepts.json"):
        
        # Import and run the main function
        from src.analysis.extract_concepts import main
        main()
        
        # Verify that extract_concepts was called with the scraped data
        mock_extract.assert_called_once_with(sample_scraped_data)
        
        # Verify that save_extracted_concepts was called with the extracted concepts
        mock_save.assert_called_once_with(mock_extract.return_value, mock_save.call_args[0][1])


@patch('src.analysis.generate_platform.generate_platform')
@patch('src.analysis.generate_platform.save_platform')
def test_generate_platform_integration(mock_save, mock_generate, setup_test_data, sample_extracted_concepts):
    """Test the generate_platform module in an integration context."""
    # Create a sample extracted concepts file
    concepts_path = setup_test_data["output_dir"] / "extracted_concepts.json"
    with open(concepts_path, 'w', encoding='utf-8') as f:
        json.dump(sample_extracted_concepts, f)
    
    # Mock the generate_platform function to return sample data
    mock_platform = {
        "title": "Political Platform",
        "executive_summary": "This is a sample platform.",
        "categories": {
            "technological": {
                "title": "Technology Policy",
                "items": [
                    {
                        "title": "AI Ethics",
                        "description": "Establishing ethical guidelines",
                        "details": "Creating regulatory frameworks",
                        "sources": ["https://example.com/tech1"]
                    }
                ]
            }
        }
    }
    mock_generate.return_value = mock_platform
    
    # Override config paths
    with patch('src.utils.config.EXTRACTED_CONCEPTS_PATH', concepts_path), \
         patch('src.utils.config.PLATFORM_OUTPUT_PATH', setup_test_data["output_dir"] / "political_platform.json"):
        
        # Import and run the main function
        from src.analysis.generate_platform import main
        main()
        
        # Verify that generate_platform was called with the extracted concepts
        mock_generate.assert_called_once_with(sample_extracted_concepts)
        
        # Verify that save_platform was called with the generated platform
        mock_save.assert_called_once_with(mock_platform, mock_save.call_args[0][1])


@patch('src.analysis.render_markdown.generate_markdown')
@patch('src.analysis.render_markdown.generate_html')
@patch('src.analysis.render_markdown.save_markdown')
def test_render_markdown_integration(mock_save, mock_html, mock_markdown, setup_test_data, sample_platform):
    """Test the render_markdown module in an integration context."""
    # Create a sample platform file
    platform_path = setup_test_data["output_dir"] / "political_platform.json"
    with open(platform_path, 'w', encoding='utf-8') as f:
        json.dump(sample_platform, f)
    
    # Mock the generate functions to return sample data
    mock_markdown.return_value = "# Sample Platform\n\n## Executive Summary\n\nThis is a sample platform."
    mock_html.return_value = "<html><body><h1>Sample Platform</h1></body></html>"
    mock_save.return_value = str(setup_test_data["output_dir"] / "political_platform.md")
    
    # Override config paths
    with patch('src.utils.config.PLATFORM_OUTPUT_PATH', platform_path), \
         patch('src.utils.config.OUTPUT_DIR', setup_test_data["output_dir"]):
        
        # Import and run the main function
        from src.analysis.render_markdown import main
        result = main()
        
        # Verify that generate functions were called with the platform
        mock_markdown.assert_called_once_with(sample_platform)
        mock_html.assert_called_once_with(sample_platform)
        
        # Verify that save_markdown was called with the generated content
        mock_save.assert_called_once()
        assert mock_save.call_args[0][0] == mock_markdown.return_value
        assert mock_save.call_args[0][1] == mock_html.return_value
        
        # Verify return value
        assert result == str(setup_test_data["output_dir"] / "political_platform.md")


def test_pipeline_flow(setup_test_data):
    """Test the entire pipeline flow with mocked functions."""
    # Here we test that the pipeline flow is correct by mocking the main functions
    # of each stage and verifying they are called in the right order

    with patch('src.data.organize_links.main') as mock_organize, \
         patch('src.scrapers.scrape_sites.main') as mock_scrape, \
         patch('src.analysis.extract_concepts.main') as mock_extract, \
         patch('src.analysis.generate_platform.main') as mock_generate, \
         patch('src.analysis.render_markdown.main') as mock_render, \
         patch('src.analysis.generate_images.main') as mock_images:

        # Mock the render_markdown.main to return a file path
        mock_render.return_value = str(setup_test_data["output_dir"] / "political_platform.md")

        # Import and run the pipeline
        from src.main import run_pipeline
        run_pipeline()

        # Verify that all stages were called in order
        mock_organize.assert_called_once()
        mock_scrape.assert_called_once()
        mock_extract.assert_called_once()
        mock_generate.assert_called_once()
        mock_render.assert_called_once()
        mock_images.assert_called_once()


def test_real_data_integration():
    """Test the pipeline with real data files to ensure integration works."""
    from src.utils.config import (
        ORGANIZED_LINKS_PATH, SCRAPED_DATA_PATH,
        EXTRACTED_CONCEPTS_PATH, PLATFORM_OUTPUT_PATH
    )
    from src.analysis.render_markdown import MARKDOWN_OUTPUT_PATH, HTML_OUTPUT_PATH

    # Verify all input files exist
    assert ORGANIZED_LINKS_PATH.exists(), f"Organized links file not found: {ORGANIZED_LINKS_PATH}"
    assert SCRAPED_DATA_PATH.exists(), f"Scraped data file not found: {SCRAPED_DATA_PATH}"

    # Test data organization module
    from src.data.organize_links import load_raw_links, categorize_links
    raw_links = load_raw_links(ORGANIZED_LINKS_PATH)  # Actually organized links now
    assert isinstance(raw_links, dict)
    assert len(raw_links) > 0

    # Test scraping module
    from src.scrapers.scrape_sites import load_organized_links
    scraped_data = load_organized_links(SCRAPED_DATA_PATH)  # Actually scraped data now
    assert isinstance(scraped_data, dict)

    # Test concept extraction module
    from src.analysis.extract_concepts import load_scraped_data
    extracted_data = load_scraped_data(EXTRACTED_CONCEPTS_PATH)  # Actually extracted concepts now
    assert isinstance(extracted_data, dict)

    # Test platform generation module
    from src.analysis.generate_platform import load_extracted_concepts
    platform_data = load_extracted_concepts(PLATFORM_OUTPUT_PATH)  # Actually platform data now
    assert isinstance(platform_data, dict)
    assert "executive_summary" in platform_data

    # Test markdown rendering module
    from src.analysis.render_markdown import load_platform_data, render_markdown, render_html

    # Load platform data
    platform_data = load_platform_data(PLATFORM_OUTPUT_PATH)
    assert isinstance(platform_data, dict)

    # Render markdown
    markdown = render_markdown(platform_data)
    assert isinstance(markdown, str)
    assert len(markdown) > 0
    assert "# Political Platform" in markdown

    # Render HTML
    html = render_html(platform_data)
    assert isinstance(html, str)
    assert len(html) > 0
    assert "<!DOCTYPE html>" in html

    # Test image generation module
    from src.analysis.generate_images import generate_image_prompts

    # Generate image prompts
    prompts = generate_image_prompts(platform_data, num_prompts=3)
    assert isinstance(prompts, list)
    assert len(prompts) >= 1
    assert all(isinstance(prompt, str) for prompt in prompts)
    assert all(len(prompt) > 0 for prompt in prompts)

    # Verify prompts are meaningful (not "No data available")
    for prompt in prompts:
        assert "No data available" not in prompt


def test_output_files_structure():
    """Test that all output files have the expected structure."""
    from src.utils.config import PLATFORM_OUTPUT_PATH
    from src.analysis.render_markdown import MARKDOWN_OUTPUT_PATH, HTML_OUTPUT_PATH

    # Test platform JSON structure
    with open(PLATFORM_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        platform_data = json.load(f)

    assert isinstance(platform_data, dict)
    assert "executive_summary" in platform_data

    # Verify executive summary is meaningful
    exec_summary = platform_data["executive_summary"]
    assert exec_summary != "Error generating executive summary."
    assert len(exec_summary) > 50  # Should be substantial content

    # Verify at least one category has meaningful content
    categories = ["political", "economic", "social", "technological", "other"]
    has_content = False
    for category in categories:
        if category in platform_data and platform_data[category] != "No data available for this category.":
            has_content = True
            assert len(platform_data[category]) > 50  # Should be substantial content
            break
    assert has_content, "No category has meaningful content"

    # Test markdown content
    with open(MARKDOWN_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    assert "# Political Platform" in markdown_content
    assert "## Executive Summary" in markdown_content
    assert len(markdown_content) > 200  # Should be substantial content

    # Test HTML content
    with open(HTML_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    assert "<!DOCTYPE html>" in html_content
    assert "<title>Political Platform</title>" in html_content
    assert len(html_content) > 500  # Should be substantial content


def test_image_generation_with_real_data():
    """Test that image generation works with real platform data."""
    from src.utils.config import PLATFORM_OUTPUT_PATH
    from src.analysis.generate_images import load_platform_data, generate_image_prompts

    # Load real platform data
    platform_data = load_platform_data(PLATFORM_OUTPUT_PATH)

    # Generate prompts
    prompts = generate_image_prompts(platform_data, num_prompts=5)

    # Verify we get the expected number of prompts
    assert len(prompts) == 5

    # Verify all prompts are meaningful strings
    for i, prompt in enumerate(prompts):
        assert isinstance(prompt, str)
        assert len(prompt) > 10
        assert "No data available" not in prompt
        print(f"Prompt {i+1}: {prompt[:80]}...")

    # Verify prompt diversity - should have different themes
    prompt_text = " ".join(prompts).lower()
    themes_found = []

    if "digital democracy" in prompt_text or "democracy" in prompt_text:
        themes_found.append("democracy")
    if "economic" in prompt_text or "innovation" in prompt_text:
        themes_found.append("economic")
    if "environment" in prompt_text or "sustainable" in prompt_text:
        themes_found.append("environmental")
    if "governance" in prompt_text or "decentralized" in prompt_text:
        themes_found.append("governance")

    # Should have at least 2 different themes
    assert len(themes_found) >= 2, f"Only found themes: {themes_found}" 