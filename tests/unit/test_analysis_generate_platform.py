"""
Unit tests for the generate_platform module.
"""

import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.analysis.generate_platform import (
    load_extracted_concepts, generate_platform, save_platform
)


def test_load_extracted_concepts():
    """Test loading extracted concepts from a JSON file."""
    # Mock data for the file
    mock_data = '{"tech": [{"url": "https://example.com", "concepts": "concept"}]}'
    
    # Mock open to return the mock data
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = load_extracted_concepts("extracted_concepts.json")
        
        # Verify expected output
        assert result == {"tech": [{"url": "https://example.com", "concepts": "concept"}]}


@patch('src.analysis.generate_platform.client.chat.completions.create')
def test_generate_platform(mock_openai):
    """Test generating a political platform from extracted concepts."""
    # Setup mock OpenAI response
    mock_platform = {
        "title": "Political Platform",
        "executive_summary": "Summary of platform",
        "categories": {
            "political": {
                "title": "Political Reforms",
                "items": [
                    {
                        "title": "Democratic Reform",
                        "description": "Improving democratic processes",
                        "details": "Electoral system changes",
                        "sources": ["https://example.com/politics"]
                    }
                ]
            },
            "technological": {
                "title": "Technology Policy",
                "items": [
                    {
                        "title": "AI Ethics",
                        "description": "Ethical AI guidelines",
                        "details": "Regulatory frameworks",
                        "sources": ["https://example.com/tech"]
                    }
                ]
            }
        }
    }
    
    # Convert platform to JSON string for the mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(mock_platform)
    mock_openai.return_value = mock_response
    
    # Create sample extracted concepts
    extracted_concepts = {
        "tech": [
            {
                "url": "https://example.com/tech",
                "title": "Tech Article",
                "status": "success",
                "concepts": "AI Ethics: Establishing ethical guidelines"
            }
        ],
        "politics": [
            {
                "url": "https://example.com/politics",
                "title": "Politics Article",
                "status": "success",
                "concepts": "Democratic Reform: Improving processes"
            }
        ]
    }
    
    # Call the function
    result = generate_platform(extracted_concepts)

    # Verify expected output structure
    assert isinstance(result, dict)
    assert "executive_summary" in result
    
    # Verify OpenAI was called (once for each category + once for executive summary)
    assert mock_openai.call_count == 3


@patch('src.analysis.generate_platform.client.chat.completions.create')
def test_generate_platform_invalid_response(mock_openai):
    """Test generating a platform with an invalid response from the API."""
    # Setup mock OpenAI to return invalid JSON
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is not valid JSON"
    mock_openai.return_value = mock_response
    
    # Create sample extracted concepts
    extracted_concepts = {
        "tech": [{"url": "https://example.com", "concepts": "concept"}]
    }
    
    # Call the function - it should handle invalid JSON gracefully
    result = generate_platform(extracted_concepts)

    # Verify that it still returns a valid structure
    assert isinstance(result, dict)
    assert "executive_summary" in result
    # The invalid response may be the raw invalid JSON or an error message
    assert isinstance(result["executive_summary"], str)
    assert len(result["executive_summary"]) > 0


@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
@patch('os.makedirs')
def test_save_platform(mock_makedirs, mock_json_dump, mock_file):
    """Test saving the generated platform to a file."""
    # Create sample platform
    platform = {
        "title": "Platform Title",
        "executive_summary": "Summary",
        "categories": {}
    }
    
    # Call the function
    save_platform(platform, "platform.json")
    
    # Verify directory creation
    mock_makedirs.assert_called_once()
    
    # Verify file opening
    mock_file.assert_called_once_with("platform.json", 'w', encoding='utf-8')
    
    # Verify JSON dumping
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == platform


@patch('src.analysis.generate_platform.load_extracted_concepts')
@patch('src.analysis.generate_platform.generate_platform')
@patch('src.analysis.generate_platform.save_platform')
def test_main_function(mock_save, mock_generate, mock_load):
    """Test the main function of generate_platform."""
    # Setup mocks
    mock_load.return_value = {"tech": [{"url": "https://example.com", "concepts": "concept"}]}
    mock_generate.return_value = {"title": "Platform", "categories": {}}
    
    # Call the function
    from src.analysis.generate_platform import main
    main()
    
    # Verify functions were called
    mock_load.assert_called_once()
    mock_generate.assert_called_once_with(mock_load.return_value)
    mock_save.assert_called_once_with(mock_generate.return_value, mock_save.call_args[0][1]) 