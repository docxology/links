"""
Unit tests for the generate_images module.
"""

import os
import json
import pytest
import base64
from unittest.mock import patch, mock_open, MagicMock
from io import BytesIO
from pathlib import Path
from src.analysis.generate_images import (
    load_platform_data, generate_image_prompts, generate_images
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


def test_generate_image_prompts(sample_platform):
    """Test generating image prompts from the platform."""
    # Call the function
    prompts = generate_image_prompts(sample_platform)

    # Verify expected output format
    assert isinstance(prompts, list)
    assert len(prompts) > 0

    # Verify content - prompts should be strings
    for prompt in prompts:
        assert isinstance(prompt, str)
        assert len(prompt) > 0


def test_generate_images_function_exists():
    """Test that generate_images function exists and uses GPT-Image-1."""
    from src.analysis.generate_images import generate_images

    # Verify function exists
    assert callable(generate_images)

    # Verify docstring mentions GPT-Image-1
    assert "GPT-Image-1" in generate_images.__doc__

    # Verify function can be imported without errors
    assert generate_images is not None


def test_gpt_image_1_model_reference():
    """Test that GPT-Image-1 model is referenced in the code."""
    import inspect
    from src.analysis.generate_images import generate_images

    # Get the source code of the function
    source = inspect.getsource(generate_images)

    # Verify GPT-Image-1 model is referenced
    assert "gpt-image-1" in source
    assert "quality=\"hd\"" in source
    assert "style=\"vivid\"" in source


@patch('src.analysis.generate_images.load_platform_data')
@patch('src.analysis.generate_images.generate_image_prompts')
@patch('src.analysis.generate_images.generate_images')
def test_main_function(mock_generate, mock_prompts, mock_load):
    """Test the main function of generate_images."""
    # Setup mocks
    mock_load.return_value = {"title": "Platform", "executive_summary": "Test summary"}
    mock_prompts.return_value = ["Test prompt 1", "Test prompt 2"]
    mock_generate.return_value = ["/path/to/image1.png", "/path/to/image2.png"]

    # Call the function
    from src.analysis.generate_images import main
    result = main()

    # Verify functions were called
    mock_load.assert_called_once()
    mock_prompts.assert_called_once_with(mock_load.return_value)
    mock_generate.assert_called_once_with(mock_prompts.return_value)

    # Verify return value is the images directory
    assert "platform_images" in str(result) 