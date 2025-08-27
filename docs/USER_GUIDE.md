# User Guide

Complete guide for using the Links Analysis Pipeline to transform web content collections into comprehensive political platforms.

## Overview

The Links Analysis Pipeline is an AI-powered system that:

- **Analyzes** web content collections
- **Extracts** political concepts and ideas using AI
- **Generates** comprehensive political platforms
- **Creates** professional documentation and visual assets
- **Produces** multi-format outputs (JSON, Markdown, HTML, Images)

## Quick Start

### 1. Prerequisites

- Python 3.13+
- OpenAI API key
- Web content collection (URLs in JSON format)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd links-analysis-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API access
cp .env.example .env
# Edit .env file with your OpenAI API key
```

### 3. Prepare Your Data

Create a JSON file with your URLs:

```json
[
  {
    "url": "https://example.com/article1",
    "title": "Article Title 1",
    "description": "Article description",
    "tags": ["politics", "democracy"]
  },
  {
    "url": "https://example.com/article2",
    "title": "Article Title 2",
    "description": "Another article",
    "tags": ["economy", "policy"]
  }
]
```

Save this as `bestofnow_urls.json` in the project root.

### 4. Run the Pipeline

```bash
# Run complete analysis
python -m src.main

# Or run step-by-step
python -m src.main --only-organize  # Organize your links
python -m src.main --only-scrape    # Scrape website content
python -m src.main --only-extract   # Extract political concepts
python -m src.main --only-analyze   # Generate political platform
python -m src.main --only-render    # Create documentation
python -m src.main --only-images    # Generate visual assets
```

## Understanding the Output

After running the pipeline, you'll find results in the `output/` directory:

### 1. Extracted Concepts (`extracted_concepts.json`)
AI-identified political concepts from your content:

```json
{
  "political": [
    {
      "url": "https://example.com/article1",
      "title": "Article Title",
      "concepts": "1. Democratic Reform\n- Implementation: Electoral system changes\n- Significance: Enhances representation",
      "status": "success"
    }
  ]
}
```

### 2. Political Platform (`political_platform.json`)
Comprehensive political platform organized by category:

```json
{
  "executive_summary": "Our platform champions digital democracy...",
  "political": "Strengthen digital rights and free speech...",
  "economic": "Promote regenerative economics...",
  "social": "Foster inclusive community development...",
  "technological": "Advance responsible technological innovation...",
  "other": "Additional policy positions..."
}
```

### 3. Documentation (`political_platform.md`)
Professional Markdown documentation with:
- Executive summary
- Detailed policy positions
- Implementation strategies
- Source attribution

### 4. Interactive HTML (`political_platform.html`)
Responsive web version with:
- Collapsible sections
- Professional styling
- Mobile-friendly design
- Navigation tabs

### 5. Visual Assets (`platform_images/`)
AI-generated images representing key platform themes using GPT-Image-1:
- `platform_image_1.png` - Executive summary visualization
- `platform_image_2.png` - Digital democracy concept
- `platform_image_3.png` - Economic innovation scene
- `platform_image_4.png` - Environmental responsibility
- `platform_image_5.png` - Additional thematic imagery

GPT-Image-1 provides superior image quality with high-definition output and vivid creative styling for more engaging visual representations.

## Advanced Usage

### Configuration Options

Customize behavior through environment variables:

```bash
# Processing limits
export MAX_LINKS=100           # Limit number of URLs to process
export REQUEST_TIMEOUT=30      # Web request timeout (seconds)

# AI settings
export GPT_MODEL=gpt-4o-mini   # AI model (gpt-4o-mini, gpt-4, etc.)
export LOG_LEVEL=INFO          # Logging verbosity

# Performance
export MAX_CONCURRENT_REQUESTS=5  # Concurrent scraping limit
```

### Selective Execution

#### Skip Expensive Stages

```bash
# Skip web scraping (use cached data)
python -m src.main --skip-scrape

# Skip image generation (faster execution)
python -m src.main --skip-images

# Skip concept extraction (reuse existing analysis)
python -m src.main --skip-extract
```

#### Run Only Specific Stages

```bash
# Only organize new content
python -m src.main --only-organize

# Only generate new images
python -m src.main --only-images

# Only update documentation
python -m src.main --only-render
```

### Custom Data Formats

#### Alternative URL Format

```json
{
  "political_articles": [
    {"url": "https://example.com/politics1", "category": "politics"},
    {"url": "https://example.com/politics2", "category": "politics"}
  ],
  "economic_articles": [
    {"url": "https://example.com/economy1", "category": "economic"}
  ]
}
```

#### Tag-Based Organization

```json
{
  "https://example.com/article1": ["democracy", "voting", "reform"],
  "https://example.com/article2": ["economy", "taxation", "policy"],
  "https://example.com/article3": ["environment", "climate", "sustainability"]
}
```

## Working with Large Datasets

### Batch Processing

For large URL collections, the pipeline automatically:
- Processes content in batches
- Saves interim results every 10 URLs
- Provides progress updates
- Handles rate limiting gracefully

### Performance Optimization

```bash
# Use faster model for development
export GPT_MODEL=gpt-4o-mini

# Limit processing for testing
export MAX_LINKS=20

# Enable caching
# (automatic - no configuration needed)
```

### Memory Management

The pipeline is designed to handle large datasets efficiently:
- Streams large files
- Processes content in batches
- Cleans up temporary data
- Provides memory usage monitoring

## Troubleshooting

### Common Issues

#### API Key Problems

**Error**: `AuthenticationError: Invalid API key`
**Solution**:
```bash
# Check your API key
cat .env | grep OPENAI_API_KEY

# Verify key format (should start with 'sk-')
# Get new key from https://platform.openai.com/api-keys
```

#### Network Issues

**Error**: `ConnectionError: Failed to connect`
**Solution**:
```bash
# Check network connectivity
ping google.com

# Verify URL accessibility
curl -I https://example.com

# Increase timeout
export REQUEST_TIMEOUT=60
```

#### Memory Issues

**Error**: `MemoryError: Out of memory`
**Solution**:
```bash
# Process fewer items
export MAX_LINKS=50

# Restart with clean cache
rm -rf cached_data/
python -m src.main
```

#### Rate Limiting

**Error**: `RateLimitError: API rate limit exceeded`
**Solution**:
```bash
# Wait and retry
sleep 60
python -m src.main --skip-scrape

# Or use different model
export GPT_MODEL=gpt-4o-mini
```

### Getting Help

#### Logging

Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python -m src.main
```

#### Demo Mode

Experience the system without processing data:
```bash
python demo_logging.py
```

#### Test Suite

Run tests to verify functionality:
```bash
python -m pytest tests/integration/test_pipeline.py::test_real_data_integration -v
```

## Output Customization

### Modifying AI Prompts

The system uses sophisticated prompts for AI analysis. You can customize these by editing the prompt templates in:

- `src/analysis/extract_concepts.py` - Concept extraction prompts
- `src/analysis/generate_platform.py` - Platform generation prompts
- `src/analysis/generate_images.py` - Image generation prompts

### Custom Categories

To use different categorization schemes, modify the keyword lists in `src/data/organize_links.py`:

```python
category_keywords = {
    "politics": ["politics", "government", "election", "policy"],
    "economy": ["economy", "finance", "business", "trade"],
    "environment": ["environment", "climate", "sustainability"],
    "technology": ["technology", "digital", "innovation", "AI"]
}
```

### Output Formats

The system generates multiple output formats. You can extend this by modifying `src/analysis/render_markdown.py` to add:

- PDF generation
- Word documents
- Presentation formats
- Custom HTML themes

## Best Practices

### Data Preparation

1. **Quality URLs**: Ensure URLs are accessible and contain relevant content
2. **Diverse Sources**: Include multiple perspectives for balanced analysis
3. **Recent Content**: Use current articles for relevant analysis
4. **Complete Metadata**: Provide titles and descriptions when possible

### Performance Optimization

1. **Caching**: Let the system cache web content for faster subsequent runs
2. **Batch Processing**: Process large collections in stages
3. **Resource Monitoring**: Monitor API usage and costs
4. **Incremental Updates**: Use selective execution for updates

### Content Strategy

1. **Thematic Balance**: Include content from different political perspectives
2. **Source Diversity**: Draw from various publications and authors
3. **Topic Coverage**: Ensure comprehensive coverage of key issues
4. **Quality Control**: Review AI-generated content for accuracy

## Examples

### Political Analysis

**Input**: Collection of articles about democracy, voting rights, and governance

**Output**: Comprehensive democratic reform platform with:
- Voting system modernization proposals
- Digital democracy implementation strategies
- Civic engagement initiatives
- Institutional reform recommendations

### Economic Policy Development

**Input**: Articles about sustainable economics, social entrepreneurship, and economic inequality

**Output**: Progressive economic platform featuring:
- Universal basic income proposals
- Green economy transition strategies
- Worker cooperative development programs
- Economic justice initiatives

### Environmental Policy

**Input**: Climate change articles, environmental justice content, sustainability reports

**Output**: Environmental platform including:
- Climate action implementation plans
- Environmental justice frameworks
- Sustainable development strategies
- Biodiversity conservation programs

## Support and Resources

### Documentation

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Architecture Guide](ARCHITECTURE.md) - System design and components
- [Development Guide](DEVELOPMENT.md) - Contributing and development
- [Testing Guide](TESTING.md) - Testing strategy and practices

### Community

- **Issues**: Report bugs and request features
- **Discussions**: Share use cases and get help
- **Wiki**: Community-contributed guides and examples

### Professional Services

For enterprise deployments, custom integrations, or specialized analysis:
- Contact the development team
- Inquire about consulting services
- Request custom feature development

---

This user guide provides comprehensive instructions for effectively using the Links Analysis Pipeline. The system is designed to be flexible, powerful, and accessible to users with varying technical expertise.
