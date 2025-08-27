# Development Guide

This guide covers development workflows, best practices, and contribution guidelines for the Links Analysis Pipeline.

## Development Environment

### Prerequisites

- Python 3.13+
- Git
- OpenAI API key

### Setup

```bash
# Clone repository
git clone <repository-url>
cd links-analysis-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Setup environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### IDE Configuration

This project includes `.cursorrules` that defines development standards:

- **Real data analysis** - No mock methods, always use actual data
- **Modular professional style** - Clean, well-documented code
- **TDD approach** - Test-driven development
- **Modern OpenAI API** - Use v1.0+ client-based approach

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes following TDD
# 1. Write failing tests
# 2. Implement functionality
# 3. Ensure tests pass

# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/
flake8 src/ tests/

# Update documentation if needed
```

### 2. Code Quality Standards

#### Naming Conventions
- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Variables**: `snake_case`
- **Constants**: `UPPER_CASE`

#### Documentation
- All public functions require docstrings
- Use Google/NumPy docstring format
- Include type hints for function parameters and return values
- Document complex algorithms and business logic

#### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Log errors with appropriate context
- Gracefully handle external service failures

### 3. Testing Strategy

#### Test Structure
```
tests/
├── unit/           # Unit tests for individual functions
├── integration/    # End-to-end pipeline tests
└── fixtures/       # Test data and fixtures
```

#### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/unit/test_analysis_extract_concepts.py

# Run tests matching pattern
python -m pytest -k "extract"

# Debug mode
python -m pytest -v -s
```

#### Writing Tests

```python
import pytest
from unittest.mock import patch, MagicMock
from src.module import function_to_test

def test_function_success():
    """Test successful execution."""
    # Arrange
    mock_data = {"test": "data"}

    # Act
    with patch('external_dependency') as mock_dep:
        mock_dep.return_value = "expected_result"
        result = function_to_test(mock_data)

    # Assert
    assert result == "expected_output"
    mock_dep.assert_called_once()

def test_function_error():
    """Test error handling."""
    # Arrange
    invalid_data = None

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        function_to_test(invalid_data)

    assert "error message" in str(excinfo.value)
```

### 4. OpenAI API Usage

#### Best Practices

1. **Client Initialization**
```python
from openai import OpenAI
from httpx import Client

http_client = Client(timeout=60.0)
client = OpenAI(api_key=API_KEY, http_client=http_client)
```

2. **Error Handling**
```python
try:
    response = client.chat.completions.create(...)
    content = response.choices[0].message.content
except openai.APIError as e:
    logger.error(f"OpenAI API error: {e}")
    raise
```

3. **Token Management**
- Monitor token usage
- Implement rate limiting
- Use appropriate model sizes

4. **Cost Optimization**
- Use `gpt-4o-mini` for development
- Batch requests where possible
- Cache expensive operations

### 5. Logging Standards

#### Logger Setup
```python
from src.utils.logger import get_logger, log_with_emoji

logger = get_logger("module_name", "module.log")
```

#### Logging Levels
- **DEBUG**: Detailed development information
- **INFO**: General operational messages
- **WARNING**: Warning conditions
- **ERROR**: Error conditions
- **CRITICAL**: Critical errors requiring immediate attention

#### Emoji Logging
```python
log_with_emoji(logger, 'INFO', 'START', "Starting process")
log_with_emoji(logger, 'SUCCESS', 'COMPLETE', "Process completed")
log_with_emoji(logger, 'ERROR', 'ERROR', "Process failed")
```

### 6. Performance Considerations

#### Optimization Techniques
- **Caching**: Implement appropriate caching strategies
- **Batch Processing**: Process data in batches where possible
- **Async Operations**: Use async for I/O bound operations
- **Memory Management**: Monitor memory usage with large datasets

#### Profiling
```bash
# Profile specific function
python -m cProfile -s cumtime src/module.py

# Memory profiling
python -m memory_profiler src/module.py
```

### 7. Security Best Practices

#### API Keys
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly
- Monitor API usage and costs

#### Input Validation
```python
def validate_url(url):
    """Validate URL format and security."""
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    # Additional security checks
    if ".." in url or "<script>" in url:
        raise ValueError("Potentially malicious URL")

    return url
```

#### Data Sanitization
- Sanitize user inputs
- Validate file paths
- Escape HTML content
- Limit data sizes

### 8. Git Workflow

#### Branch Naming
- `feature/feature-name`: New features
- `bugfix/bug-description`: Bug fixes
- `hotfix/critical-fix`: Critical fixes
- `refactor/component-name`: Code refactoring

#### Commit Messages
```
feat: add user authentication system
fix: resolve memory leak in data processing
docs: update API documentation
refactor: simplify logging configuration
test: add integration tests for pipeline
```

#### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Create pull request with description
6. Code review and approval
7. Merge to `main`

### 9. Continuous Integration

#### GitHub Actions Setup
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest --cov=src
      - name: Check code quality
        run: |
          black --check src/ tests/
          flake8 src/ tests/
```

### 10. Deployment

#### Environment Configuration
```bash
# Production environment variables
OPENAI_API_KEY=sk-prod-...
LOG_LEVEL=WARNING
MAX_LINKS=500
GPT_MODEL=gpt-4
```

#### Docker Deployment
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "src.main"]
```

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Check API key validity
   - Monitor rate limits
   - Verify model availability

2. **Web Scraping Failures**
   - Check network connectivity
   - Verify URL accessibility
   - Review user agent settings

3. **Memory Issues**
   - Monitor data sizes
   - Implement batching
   - Clear caches regularly

4. **Test Failures**
   - Update test expectations
   - Check mock configurations
   - Verify environment setup

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python -m src.main --verbose

# Debug specific module
python -c "import src.module; breakpoint()"
```

## Contributing

1. Follow the development workflow
2. Write comprehensive tests
3. Update documentation
4. Follow code style guidelines
5. Ensure all tests pass
6. Submit pull request

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python Best Practices](https://python.org/dev/peps/pep-0008/)
- [Testing in Python](https://docs.python.org/3/library/unittest.html)
- [Beautiful Soup Documentation](https://beautiful-soup-4.readthedocs.io/)
