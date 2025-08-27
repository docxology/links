# Testing Guide

Comprehensive testing strategy and guidelines for the Links Analysis Pipeline.

## Testing Philosophy

The project follows a **test-driven development (TDD)** approach with an emphasis on:

- **Real Data Testing**: Use actual data rather than mocks where possible
- **Integration Focus**: Test complete workflows, not just individual units
- **Comprehensive Coverage**: Test both success and failure scenarios
- **Maintainable Tests**: Clear, readable test code that serves as documentation

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── fixtures/                # Test data files
│   ├── sample_extracted_concepts.json
│   ├── sample_platform.json
│   ├── sample_scraped_data.json
│   ├── sample_tags.json
│   └── sample_urls.json
├── unit/                    # Unit tests for individual functions
│   ├── test_analysis_extract_concepts.py
│   ├── test_analysis_generate_images.py
│   ├── test_analysis_generate_platform.py
│   ├── test_analysis_render_markdown.py
│   ├── test_data_organize_links.py
│   ├── test_scrapers_scrape_sites.py
│   ├── test_utils_config.py
│   └── test_utils_logger.py
└── integration/             # Integration tests for end-to-end workflows
    └── test_pipeline.py
```

## Running Tests

### Basic Commands

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/unit/test_data_organize_links.py

# Run tests matching pattern
python -m pytest -k "extract"

# Run with coverage report
python -m pytest --cov=src --cov-report=html

# Run tests in parallel (if pytest-xdist installed)
python -m pytest -n auto
```

### Test Categories

```bash
# Run only unit tests
python -m pytest tests/unit/

# Run only integration tests
python -m pytest tests/integration/

# Run tests for specific module
python -m pytest tests/unit/test_analysis_*.py
```

### Debug Mode

```bash
# Stop on first failure
python -m pytest -x

# Show print statements
python -m pytest -s

# Enter debugger on failure
python -m pytest --pdb

# Verbose failure information
python -m pytest -vv
```

## Writing Tests

### Test Organization

Each test file should follow this structure:

```python
"""
Unit tests for module_name module.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.module_name import function_to_test


class TestFunctionGroup:
    """Test class for related functions."""

    def test_success_case(self):
        """Test successful execution."""
        # Arrange
        test_input = "valid_input"

        # Act
        result = function_to_test(test_input)

        # Assert
        assert result == "expected_output"

    def test_error_case(self):
        """Test error handling."""
        # Arrange
        invalid_input = None

        # Act & Assert
        with pytest.raises(ValueError):
            function_to_test(invalid_input)

    def test_edge_case(self):
        """Test edge cases."""
        # Test with empty input, large input, special characters, etc.
        pass
```

### Fixtures

Use fixtures for reusable test data:

```python
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "url": "https://example.com",
        "title": "Test Article",
        "content": "Test content"
    }


def test_with_sample_data(sample_data):
    """Test using sample data fixture."""
    result = process_data(sample_data)
    assert result is not None
```

### Mocking Strategy

#### External Dependencies

```python
@patch('requests.get')
def test_api_call(mock_get):
    """Test function that makes HTTP requests."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response

    # Test the function
    result = call_external_api()

    # Verify
    assert result["data"] == "test"
    mock_get.assert_called_once()
```

#### OpenAI API Mocking

```python
@patch('src.analysis.extract_concepts.client.chat.completions.create')
def test_ai_extraction(mock_openai):
    """Test AI-powered concept extraction."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Extracted concepts..."
    mock_openai.return_value = mock_response

    # Test
    result = extract_concepts_from_document(test_document)

    # Verify
    assert "concepts" in result
    mock_openai.assert_called_once()
```

#### File System Mocking

```python
@patch('builtins.open', new_callable=mock_open)
def test_file_operations(mock_file):
    """Test functions that read/write files."""
    # Setup mock file content
    mock_file.return_value.__enter__.return_value.read.return_value = "file content"

    # Test
    content = read_file("test.txt")

    # Verify
    assert content == "file content"
    mock_file.assert_called_with("test.txt", "r")
```

## Test Data Management

### Fixtures Directory

The `tests/fixtures/` directory contains sample data files:

- **sample_urls.json**: Sample URL collection
- **sample_tags.json**: URL categorization tags
- **sample_scraped_data.json**: Mock scraped content
- **sample_extracted_concepts.json**: AI extraction results
- **sample_platform.json**: Generated platform data

### Generating Test Data

```python
def create_test_data():
    """Helper function to create test data."""
    return {
        "url": "https://example.com",
        "title": "Test Article",
        "content": {
            "paragraphs": ["Test paragraph"],
            "headings": ["Test Heading"]
        }
    }
```

## Integration Testing

### Pipeline Integration Tests

The integration tests verify complete workflows:

```python
def test_real_data_integration():
    """Test pipeline with real data files."""
    # Load actual data files
    from src.utils.config import ORGANIZED_LINKS_PATH

    # Test data loading
    from src.data.organize_links import load_raw_links
    data = load_raw_links(ORGANIZED_LINKS_PATH)
    assert isinstance(data, dict)

    # Test subsequent processing stages
    # ... integration test logic
```

### End-to-End Testing

```python
def test_pipeline_flow():
    """Test complete pipeline execution."""
    with patch('src.data.organize_links.main') as mock_organize, \
         patch('src.scrapers.scrape_sites.main') as mock_scrape, \
         patch('src.analysis.extract_concepts.main') as mock_extract:

        # Mock successful execution
        mock_organize.return_value = None
        mock_scrape.return_value = None
        mock_extract.return_value = None

        # Run pipeline
        from src.main import run_pipeline
        run_pipeline()

        # Verify all stages called
        mock_organize.assert_called_once()
        mock_scrape.assert_called_once()
        mock_extract.assert_called_once()
```

## Performance Testing

### Benchmarking

```python
import time

def test_processing_performance():
    """Test processing performance."""
    test_data = create_large_test_dataset()

    start_time = time.time()
    result = process_data(test_data)
    end_time = time.time()

    processing_time = end_time - start_time

    # Assert performance requirements
    assert processing_time < 5.0  # Should complete in under 5 seconds
    assert result is not None
```

### Memory Testing

```python
import psutil
import os

def test_memory_usage():
    """Test memory usage during processing."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    # Perform memory-intensive operation
    large_result = process_large_dataset()

    final_memory = process.memory_info().rss
    memory_used = final_memory - initial_memory

    # Assert memory usage is reasonable (under 100MB)
    assert memory_used < 100 * 1024 * 1024
```

## Coverage Requirements

### Minimum Coverage

- **Unit Tests**: 80% coverage minimum
- **Integration Tests**: 90% of pipeline workflows
- **Error Handling**: All error paths tested

### Coverage Measurement

```bash
# Generate coverage report
python -m pytest --cov=src --cov-report=html

# Open HTML report
open htmlcov/index.html
```

### Coverage Goals by Module

- **Data Processing**: 90%+ (critical path)
- **Scraping**: 85%+ (error-prone)
- **Analysis**: 90%+ (complex logic)
- **Utilities**: 95%+ (simple functions)

## Continuous Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: python -m pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Test Maintenance

### Regular Tasks

1. **Update Tests**: Keep tests current with code changes
2. **Review Coverage**: Ensure new code is tested
3. **Performance Monitoring**: Track test execution times
4. **Fixture Updates**: Update test data as needed

### Test Organization Best Practices

- **Descriptive Names**: `test_function_name_descriptive_action`
- **Single Responsibility**: One assertion per test
- **Independent Tests**: Tests should not depend on each other
- **Fast Execution**: Keep tests running quickly
- **Clear Documentation**: Document complex test scenarios

### Debugging Failing Tests

```bash
# Run specific failing test with debug info
python -m pytest tests/unit/test_specific.py::TestClass::test_method -v -s --pdb

# Check test data
python -c "from tests.conftest import sample_data; print(sample_data())"

# Verify mock setup
python -c "from unittest.mock import MagicMock; mock = MagicMock(); print(mock.method())"
```

## Best Practices

### Test Design

1. **Arrange-Act-Assert**: Clear test structure
2. **Descriptive Assertions**: Explain what is being tested
3. **Edge Cases**: Test boundary conditions
4. **Error Scenarios**: Test failure modes
5. **Data Validation**: Verify data integrity

### Mock Usage

1. **Minimal Mocking**: Mock only external dependencies
2. **Realistic Responses**: Use realistic mock data
3. **Verification**: Verify mock interactions
4. **Cleanup**: Reset mocks between tests

### Performance

1. **Fast Tests**: Keep execution time under 100ms per test
2. **Parallel Execution**: Use pytest-xdist for parallel runs
3. **Selective Testing**: Run only relevant tests during development
4. **Caching**: Cache expensive test setup

## Troubleshooting

### Common Issues

#### Import Errors
```python
# Fix: Ensure PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### Mock Errors
```python
# Fix: Verify mock target path
@patch('src.module.submodule.function')  # Correct
@patch('module.submodule.function')     # Incorrect
```

#### Coverage Issues
```python
# Fix: Add tests for uncovered lines
# Or exclude from coverage
# pragma: no cover
```

#### Async Test Issues
```python
# Fix: Use pytest-asyncio
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

This testing guide ensures comprehensive, maintainable tests that validate the entire Links Analysis Pipeline functionality.
