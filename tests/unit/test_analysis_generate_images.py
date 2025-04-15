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
    load_platform, generate_image_prompts, generate_images, save_image
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


def test_generate_image_prompts(sample_platform):
    """Test generating image prompts from the platform."""
    # Call the function
    prompts = generate_image_prompts(sample_platform)
    
    # Verify expected output format
    assert isinstance(prompts, list)
    assert len(prompts) > 0
    
    # Verify content
    for prompt in prompts:
        assert isinstance(prompt, dict)
        assert "title" in prompt
        assert "prompt" in prompt
        assert "category" in prompt
        assert prompt["category"] in ["overview", "political", "technological", "economic"]


@patch('openai.Image.create')
def test_generate_images(mock_openai_image):
    """Test generating images from prompts."""
    # Setup mock response
    mock_response = MagicMock()
    # Base64 encoded tiny transparent PNG
    mock_png_data = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\xe7\xe6\x00\x00\x00\x00IEND\xaeB`\x82').decode('utf-8')
    
    mock_response.data = [{"b64_json": mock_png_data}]
    mock_openai_image.return_value = mock_response
    
    # Create sample prompts
    prompts = [
        {"title": "Overview", "prompt": "A visual representation of a political platform", "category": "overview"}
    ]
    
    # Call the function
    with patch('tqdm.tqdm') as mock_tqdm:
        mock_tqdm.return_value.__iter__.return_value = range(1)
        results = generate_images(prompts)
    
    # Verify expected output
    assert len(results) == 1
    assert results[0]["title"] == "Overview"
    assert results[0]["category"] == "overview"
    assert "image_data" in results[0]
    
    # Verify OpenAI was called
    mock_openai_image.assert_called_once()
    args, kwargs = mock_openai_image.call_args
    assert kwargs["prompt"] == "A visual representation of a political platform"


@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_save_image(mock_makedirs, mock_file):
    """Test saving an image to a file."""
    # Create sample image data (Base64 encoded tiny transparent PNG)
    image_data = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\xe7\xe6\x00\x00\x00\x00IEND\xaeB`\x82').decode('utf-8')
    
    # Call the function
    filename = save_image(image_data, "output/images", "test_image", "overview")
    
    # Verify directory creation
    mock_makedirs.assert_called_once_with("output/images", exist_ok=True)
    
    # Verify file opening
    expected_filename = "output/images/overview_test_image.png"
    mock_file.assert_called_once_with(expected_filename, 'wb')
    
    # Verify image data was written
    handle = mock_file.return_value.__enter__.return_value
    handle.write.assert_called_once()
    
    # Verify return value
    assert filename == expected_filename


@patch('src.analysis.generate_images.load_platform')
@patch('src.analysis.generate_images.generate_image_prompts')
@patch('src.analysis.generate_images.generate_images')
@patch('src.analysis.generate_images.save_image')
def test_main_function(mock_save, mock_generate, mock_prompts, mock_load):
    """Test the main function of generate_images."""
    # Setup mocks
    mock_load.return_value = {"title": "Platform", "categories": {}}
    mock_prompts.return_value = [{"title": "Test", "prompt": "Test prompt", "category": "overview"}]
    mock_generate.return_value = [{"title": "Test", "category": "overview", "image_data": "data"}]
    mock_save.return_value = "output/images/overview_test.png"
    
    # Call the function
    from src.analysis.generate_images import main
    result = main()
    
    # Verify functions were called
    mock_load.assert_called_once()
    mock_prompts.assert_called_once_with(mock_load.return_value)
    mock_generate.assert_called_once_with(mock_prompts.return_value)
    assert mock_save.call_count == 1
    
    # Verify return value is the images directory
    assert result == "output/images" 