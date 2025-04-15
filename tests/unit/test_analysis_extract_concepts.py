"""
Unit tests for the extract_concepts module.
"""

import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.analysis.extract_concepts import (
    load_scraped_data, extract_concepts_from_document,
    extract_concepts, save_extracted_concepts
)


def test_load_scraped_data():
    """Test loading scraped data from a JSON file."""
    # Mock data for the file
    mock_data = '{"tech": [{"url": "https://example.com", "status": "success"}]}'
    
    # Mock open to return the mock data
    with patch('builtins.open', mock_open(read_data=mock_data)):
        result = load_scraped_data("scraped_data.json")
        
        # Verify expected output
        assert result == {"tech": [{"url": "https://example.com", "status": "success"}]}


@patch('openai.ChatCompletion.create')
def test_extract_concepts_from_document_success(mock_openai):
    """Test extracting concepts from a document successfully."""
    # Setup mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "1. Test Concept\n- Implementation: test\n- Significance: important"
    mock_openai.return_value = mock_response
    
    # Create a test document
    document = {
        "url": "https://example.com",
        "title": "Test Document",
        "status": "success",
        "content": {
            "title": "Test Document",
            "headings": [{"level": 1, "text": "Test Heading"}],
            "paragraphs": ["This is a test paragraph."],
            "lists": [{"items": ["Item 1", "Item 2"]}]
        }
    }
    
    # Call the function
    result = extract_concepts_from_document(document)
    
    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["title"] == "Test Document"
    assert result["status"] == "success"
    assert "1. Test Concept" in result["concepts"]
    
    # Verify OpenAI was called
    mock_openai.assert_called_once()


def test_extract_concepts_from_document_failure():
    """Test extracting concepts from a document that has no content."""
    # Create a test document with no content
    document = {
        "url": "https://example.com",
        "title": "Test Document",
        "status": "error"
    }
    
    # Call the function
    result = extract_concepts_from_document(document)
    
    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["title"] == "Test Document"
    assert result["status"] == "skipped"
    assert result["concepts"] == []


def test_extract_concepts_from_document_invalid_content():
    """Test extracting concepts from a document with invalid content format."""
    # Create a test document with invalid content format
    document = {
        "url": "https://example.com",
        "title": "Test Document",
        "status": "success",
        "content": "This is not a dictionary"
    }
    
    # Call the function
    result = extract_concepts_from_document(document)
    
    # Verify expected output
    assert result["url"] == "https://example.com"
    assert result["title"] == "Test Document"
    assert result["status"] == "skipped"
    assert result["concepts"] == []


@patch('src.analysis.extract_concepts.extract_concepts_from_document')
def test_extract_concepts(mock_extract):
    """Test extracting concepts from all documents."""
    # Setup mock to return sample data
    mock_extract.side_effect = [
        {"url": "https://example.com/1", "title": "Doc 1", "status": "success", "concepts": "Concept 1"},
        {"url": "https://example.com/2", "title": "Doc 2", "status": "error", "error": "Failed"}
    ]
    
    # Create sample scraped data
    scraped_data = {
        "tech": [
            {"url": "https://example.com/1", "title": "Doc 1", "status": "success"},
            {"url": "https://example.com/2", "title": "Doc 2", "status": "success"}
        ]
    }
    
    # Call the function with a mock progress bar
    with patch('tqdm.tqdm') as mock_tqdm:
        mock_tqdm.return_value.__iter__.return_value = range(2)
        results = extract_concepts(scraped_data)
    
    # Verify expected output
    assert "tech" in results
    assert len(results["tech"]) == 2
    assert results["tech"][0]["url"] == "https://example.com/1"
    assert results["tech"][0]["status"] == "success"
    assert results["tech"][0]["concepts"] == "Concept 1"
    assert results["tech"][1]["url"] == "https://example.com/2"
    assert results["tech"][1]["status"] == "error"
    
    # Verify extract_concepts_from_document was called for each document
    assert mock_extract.call_count == 2


@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
@patch('os.makedirs')
def test_save_extracted_concepts(mock_makedirs, mock_json_dump, mock_file):
    """Test saving extracted concepts to JSON and text files."""
    # Create sample extracted data
    extracted_data = {
        "tech": [
            {
                "url": "https://example.com",
                "title": "Test Document",
                "status": "success",
                "concepts": "1. Test Concept\n- Implementation: test"
            }
        ]
    }
    
    # Call the function
    save_extracted_concepts(extracted_data, "extracted_concepts.json")
    
    # Verify directory creation
    mock_makedirs.assert_called_once()
    
    # Verify file opening - should be called twice (JSON and text files)
    assert mock_file.call_count == 2
    mock_file.assert_any_call("extracted_concepts.json", 'w', encoding='utf-8')
    mock_file.assert_any_call("extracted_concepts_text.txt", 'w', encoding='utf-8')
    
    # Verify JSON dumping
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == extracted_data


@patch('src.analysis.extract_concepts.load_scraped_data')
@patch('src.analysis.extract_concepts.extract_concepts')
@patch('src.analysis.extract_concepts.save_extracted_concepts')
def test_main_function(mock_save, mock_extract, mock_load):
    """Test the main function of extract_concepts."""
    # Setup mocks
    mock_load.return_value = {"tech": [{"url": "https://example.com"}]}
    mock_extract.return_value = {"tech": [{"url": "https://example.com", "concepts": "concept"}]}
    
    # Call the function
    from src.analysis.extract_concepts import main
    main()
    
    # Verify functions were called
    mock_load.assert_called_once()
    mock_extract.assert_called_once_with(mock_load.return_value)
    mock_save.assert_called_once() 