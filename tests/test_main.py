"""
Tests for the main.py module that contains the CLI interface.
"""

import sys
import pytest
from unittest.mock import patch, MagicMock


@patch('src.main.run_pipeline')
def test_main_with_no_args(mock_run_pipeline):
    """Test the main function with no arguments."""
    # Set up sys.argv with no arguments
    with patch('sys.argv', ['src/main.py']):
        # Import and run the main function
        from src.main import main
        main()
        
        # Verify run_pipeline was called with no skips
        mock_run_pipeline.assert_called_once_with(
            skip_organize=False,
            skip_scrape=False,
            skip_extract=False,
            skip_analyze=False,
            skip_render=False,
            skip_images=False
        )


@patch('src.main.run_pipeline')
def test_main_with_skip_args(mock_run_pipeline):
    """Test the main function with skip arguments."""
    # Set up sys.argv with skip arguments
    with patch('sys.argv', ['src/main.py', '--skip-organize', '--skip-scrape']):
        # Import and run the main function
        from src.main import main
        main()
        
        # Verify run_pipeline was called with the right skips
        mock_run_pipeline.assert_called_once_with(
            skip_organize=True,
            skip_scrape=True,
            skip_extract=False,
            skip_analyze=False,
            skip_render=False,
            skip_images=False
        )


@patch('src.main.run_pipeline')
def test_main_with_only_args(mock_run_pipeline):
    """Test the main function with only arguments."""
    # Set up sys.argv with only arguments
    with patch('sys.argv', ['src/main.py', '--only-extract']):
        # Import and run the main function
        from src.main import main
        main()
        
        # Verify run_pipeline was called with the right skips
        mock_run_pipeline.assert_called_once_with(
            skip_organize=True,
            skip_scrape=True,
            skip_extract=False,
            skip_analyze=True,
            skip_render=True,
            skip_images=True
        )


@patch('src.main.run_pipeline')
def test_main_with_multiple_only_args(mock_run_pipeline):
    """Test the main function with multiple only arguments."""
    # Set up sys.argv with multiple only arguments
    with patch('sys.argv', ['src/main.py', '--only-extract', '--only-analyze']):
        # Import and run the main function
        from src.main import main
        main()
        
        # Verify run_pipeline was called with the right skips
        # When multiple only flags are provided, they should all run
        mock_run_pipeline.assert_called_once_with(
            skip_organize=True,
            skip_scrape=True,
            skip_extract=False,
            skip_analyze=False,
            skip_render=True,
            skip_images=True
        )


@patch('src.main.run_pipeline')
def test_main_with_mixed_args(mock_run_pipeline):
    """Test the main function with a mix of skip and only arguments."""
    # Set up sys.argv with mixed arguments
    with patch('sys.argv', ['src/main.py', '--only-extract', '--skip-images']):
        # Import and run the main function
        from src.main import main
        main()
        
        # Verify run_pipeline was called with the right skips
        # The only flag takes precedence and sets all others to skip
        mock_run_pipeline.assert_called_once_with(
            skip_organize=True,
            skip_scrape=True,
            skip_extract=False,
            skip_analyze=True,
            skip_render=True,
            skip_images=True
        )


@patch('src.main.run_pipeline')
def test_main_with_error(mock_run_pipeline):
    """Test the main function when an error occurs."""
    # Set up the mock to raise an exception
    mock_run_pipeline.side_effect = Exception("Test error")
    
    # Set up sys.argv
    with patch('sys.argv', ['src/main.py']):
        # Import the main function
        from src.main import main
        
        # Verify an exception is raised
        with pytest.raises(Exception) as excinfo:
            main()
        
        assert "Test error" in str(excinfo.value)


def test_pipeline_stages():
    """Test that all pipeline stages can be run individually."""
    # Test that we can import and call each stage's main function
    with patch('src.data.organize_links.main') as mock_organize, \
         patch('src.scrapers.scrape_sites.main') as mock_scrape, \
         patch('src.analysis.extract_concepts.main') as mock_extract, \
         patch('src.analysis.generate_platform.main') as mock_generate, \
         patch('src.analysis.render_markdown.main') as mock_render, \
         patch('src.analysis.generate_images.main') as mock_images:
        
        # Import the run_pipeline function
        from src.main import run_pipeline
        
        # Run each stage individually
        
        # Only organize
        run_pipeline(skip_scrape=True, skip_extract=True, skip_analyze=True, skip_render=True, skip_images=True)
        mock_organize.assert_called_once()
        mock_organize.reset_mock()
        
        # Only scrape
        run_pipeline(skip_organize=True, skip_extract=True, skip_analyze=True, skip_render=True, skip_images=True)
        mock_scrape.assert_called_once()
        mock_scrape.reset_mock()
        
        # Only extract
        run_pipeline(skip_organize=True, skip_scrape=True, skip_analyze=True, skip_render=True, skip_images=True)
        mock_extract.assert_called_once()
        mock_extract.reset_mock()
        
        # Only analyze
        run_pipeline(skip_organize=True, skip_scrape=True, skip_extract=True, skip_render=True, skip_images=True)
        mock_generate.assert_called_once()
        mock_generate.reset_mock()
        
        # Only render
        run_pipeline(skip_organize=True, skip_scrape=True, skip_extract=True, skip_analyze=True, skip_images=True)
        mock_render.assert_called_once()
        mock_render.reset_mock()
        
        # Only images
        run_pipeline(skip_organize=True, skip_scrape=True, skip_extract=True, skip_analyze=True, skip_render=True)
        mock_images.assert_called_once() 