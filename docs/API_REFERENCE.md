# API Reference

## Core Modules

### `src.main`

Main pipeline entry point providing command-line interface and orchestration.

#### `run_pipeline(skip_organize=False, skip_scrape=False, skip_extract=False, skip_analyze=False, skip_render=False, skip_images=False)`

Runs the complete analysis pipeline with selective stage execution.

**Parameters:**
- `skip_organize` (bool): Skip data organization stage
- `skip_scrape` (bool): Skip web scraping stage
- `skip_extract` (bool): Skip concept extraction stage
- `skip_analyze` (bool): Skip platform generation stage
- `skip_render` (bool): Skip content rendering stage
- `skip_images` (bool): Skip image generation stage

**Returns:** None

---

## Data Processing

### `src.data.organize_links`

#### `load_raw_links(file_path)`

Loads raw URL data from JSON file.

**Parameters:**
- `file_path` (str): Path to JSON file containing URL data

**Returns:** list - List of link objects with URL, title, description, and tags

#### `categorize_links(links_data)`

Categorizes links based on content analysis.

**Parameters:**
- `links_data` (list): List of link objects

**Returns:** dict - Categorized links by topic (political, economic, social, technological, other)

#### `save_organized_links(organized_links, output_path)`

Saves organized link data to JSON file.

**Parameters:**
- `organized_links` (dict): Categorized link data
- `output_path` (str): Output file path

**Returns:** None

---

## Web Scraping

### `src.scrapers.scrape_sites`

#### `load_organized_links(file_path)`

Loads organized link data for scraping.

**Parameters:**
- `file_path` (str): Path to organized links JSON file

**Returns:** dict - Organized link data by category

#### `scrape_url(url)`

Scrapes content from a single URL with caching and error handling.

**Parameters:**
- `url` (str): URL to scrape

**Returns:** dict - Scraped content with status, content, and metadata

#### `scrape_links(organized_links)`

Scrapes content from multiple organized links.

**Parameters:**
- `organized_links` (dict): Organized links by category

**Returns:** dict - Scraped content organized by category

#### `extract_meaningful_content(soup)`

Extracts structured content from BeautifulSoup object.

**Parameters:**
- `soup` (BeautifulSoup): Parsed HTML content

**Returns:** dict - Extracted content with title, headings, paragraphs, list_items, metadata

#### `save_scraped_data(scraped_data, output_path)`

Saves scraped data to JSON and text extract files.

**Parameters:**
- `scraped_data` (dict): Scraped content data
- `output_path` (str): Output JSON file path

**Returns:** None

---

## Content Analysis

### `src.analysis.extract_concepts`

#### `load_scraped_data(file_path)`

Loads scraped data for concept extraction.

**Parameters:**
- `file_path` (str): Path to scraped data JSON file

**Returns:** dict - Scraped data organized by category

#### `extract_concepts_from_document(document)`

Extracts political concepts from a single document using AI.

**Parameters:**
- `document` (dict): Document with scraped content

**Returns:** dict - Extracted concepts with metadata

#### `extract_concepts(scraped_data)`

Extracts concepts from all scraped documents.

**Parameters:**
- `scraped_data` (dict): Scraped data by category

**Returns:** dict - Extracted concepts organized by category

#### `save_extracted_concepts(extracted_data, output_path)`

Saves extracted concepts to JSON and text files.

**Parameters:**
- `extracted_data` (dict): Extracted concept data
- `output_path` (str): Output JSON file path

**Returns:** None

---

### `src.analysis.generate_platform`

#### `load_extracted_concepts(file_path)`

Loads extracted concepts for platform generation.

**Parameters:**
- `file_path` (str): Path to extracted concepts JSON file

**Returns:** dict - Extracted concepts by category

#### `generate_section(category, documents)`

Generates platform section for a specific category.

**Parameters:**
- `category` (str): Category name
- `documents` (list): Documents with extracted concepts

**Returns:** str - Generated platform section content

#### `generate_platform(extracted_data)`

Generates complete political platform with executive summary.

**Parameters:**
- `extracted_data` (dict): Extracted concepts by category

**Returns:** dict - Complete political platform

#### `save_platform(platform, output_path)`

Saves generated platform to JSON file.

**Parameters:**
- `platform` (dict): Generated platform data
- `output_path` (str): Output JSON file path

**Returns:** None

---

### `src.analysis.render_markdown`

#### `load_platform_data(file_path)`

Loads platform data for rendering.

**Parameters:**
- `file_path` (str): Path to platform JSON file

**Returns:** dict - Platform data

#### `render_markdown(platform_data)`

Renders platform data as Markdown document.

**Parameters:**
- `platform_data` (dict): Platform data

**Returns:** str - Markdown formatted content

#### `render_html(platform_data)`

Renders platform data as interactive HTML document.

**Parameters:**
- `platform_data` (dict): Platform data

**Returns:** str - HTML formatted content

#### `save_markdown(markdown_content, output_path)`

Saves Markdown content to file.

**Parameters:**
- `markdown_content` (str): Markdown content
- `output_path` (str): Output file path

**Returns:** None

#### `save_html(html_content, output_path)`

Saves HTML content to file.

**Parameters:**
- `html_content` (str): HTML content
- `output_path` (str): Output file path

**Returns:** None

---

### `src.analysis.generate_images`

#### `load_platform_data(file_path)`

Loads platform data for image generation.

**Parameters:**
- `file_path` (str): Path to platform JSON file

**Returns:** dict - Platform data

#### `generate_image_prompts(platform_data, num_prompts=5)`

Generates image prompts based on platform content.

**Parameters:**
- `platform_data` (dict): Platform data
- `num_prompts` (int): Number of prompts to generate

**Returns:** list - List of image generation prompts

#### `generate_images(prompts)`

Generates images using OpenAI GPT-Image-1 based on prompts.

GPT-Image-1 provides advanced text-to-image generation with superior quality,
creative capabilities, and flexible styling options.

**Parameters:**
- `prompts` (list): List of image prompts

**Returns:** list - List of generated image file paths

**Features:**
- High-definition image quality (`quality="hd"`)
- Vivid creative style (`style="vivid"`)
- Advanced prompt understanding and transformation
- Superior image composition and aesthetics

---

## Utilities

### `src.utils.config`

Configuration management module.

#### Key Constants
- `BASE_DIR`: Project root directory
- `DATA_DIR`: Data processing directory
- `OUTPUT_DIR`: Output files directory
- `LOGS_DIR`: Log files directory
- `OPENAI_API_KEY`: OpenAI API key from environment
- `GPT_MODEL`: AI model to use (default: gpt-4o-mini)
- `REQUEST_TIMEOUT`: Web request timeout
- `MAX_LINKS`: Maximum links to process

### `src.utils.logger`

Logging system with emoji-enhanced output.

#### `get_logger(name, log_file=None)`

Creates configured logger instance.

**Parameters:**
- `name` (str): Logger name
- `log_file` (str, optional): Log file name

**Returns:** logging.Logger - Configured logger

#### `log_with_emoji(logger, level, emoji_key, message)`

Logs message with emoji and specified level.

**Parameters:**
- `logger`: Logger instance
- `level` (str): Log level (INFO, WARNING, ERROR, etc.)
- `emoji_key` (str): Emoji key from EMOJI dictionary
- `message` (str): Log message

**Returns:** None

#### `ColoredFormatter`

Custom log formatter with colors and emojis.

---

## Data Structures

### Link Object
```python
{
    "url": "https://example.com",
    "title": "Article Title",
    "description": "Article description",
    "tags": ["technology", "ai"]
}
```

### Scraped Content
```python
{
    "url": "https://example.com",
    "title": "Page Title",
    "content": {
        "title": "Page Title",
        "headings": ["Heading 1", "Heading 2"],
        "paragraphs": ["Paragraph 1", "Paragraph 2"],
        "list_items": ["Item 1", "Item 2"],
        "metadata": {"description": "Page description"}
    },
    "status": "success",
    "source": "web"
}
```

### Extracted Concepts
```python
{
    "url": "https://example.com",
    "title": "Article Title",
    "concepts": "AI Ethics: Establishing ethical guidelines for AI development...",
    "status": "success"
}
```

### Political Platform
```python
{
    "executive_summary": "Comprehensive platform overview...",
    "political": "Political platform section content...",
    "economic": "Economic platform section content...",
    "social": "Social platform section content...",
    "technological": "Technological platform section content...",
    "other": "Other category platform content..."
}
```

---

## Error Handling

All modules implement comprehensive error handling:

- **Network errors**: Graceful handling of connection failures
- **API errors**: Robust OpenAI API error management
- **File I/O errors**: Safe file operations with proper error reporting
- **Data validation**: Input validation and sanitization
- **Logging**: Comprehensive error logging with context

---

## Configuration

The system supports configuration through environment variables:

- `OPENAI_API_KEY`: Required OpenAI API key
- `LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `MAX_LINKS`: Maximum number of links to process
- `GPT_MODEL`: OpenAI model to use
- `TIMEOUT`: Request timeout in seconds
- `MAX_CONCURRENT_REQUESTS`: Maximum concurrent requests

---

## Dependencies

- **openai**: OpenAI API client
- **requests**: HTTP client for web scraping
- **beautifulsoup4**: HTML parsing
- **python-dotenv**: Environment variable management
- **tqdm**: Progress bars
- **colorama**: Terminal colors
