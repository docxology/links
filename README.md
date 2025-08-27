# Links Analysis Pipeline

A comprehensive AI-powered pipeline for analyzing web content collections and generating political platforms. This project demonstrates modern software engineering practices with modular architecture, comprehensive testing, and professional documentation.

## Features

- **Web Scraping**: Intelligent content extraction with caching and error handling
- **AI-Powered Analysis**: LLM-based concept extraction and political platform generation
- **Multi-format Output**: JSON, Markdown, HTML, and image generation
- **Comprehensive Testing**: Unit tests, integration tests, and real data validation
- **Professional Logging**: Emoji-enhanced logging with progress tracking
- **Modular Architecture**: Clean separation of concerns with well-documented APIs

## Project Structure

```
/
├── src/                           # Source code
│   ├── main.py                    # Main pipeline entry point
│   ├── data/
│   │   ├── organize_links.py      # Link organization and categorization
│   │   └── __init__.py
│   ├── scrapers/
│   │   ├── scrape_sites.py        # Web scraping and content extraction
│   │   └── __init__.py
│   ├── analysis/
│   │   ├── extract_concepts.py    # AI-powered concept extraction
│   │   ├── generate_platform.py   # Political platform generation
│   │   ├── render_markdown.py     # Multi-format output rendering
│   │   ├── generate_images.py     # AI image generation
│   │   └── __init__.py
│   └── utils/
│       ├── config.py              # Configuration management
│       ├── logger.py              # Logging system
│       ├── demo_logger.py         # Logging demonstrations
│       └── __init__.py
├── tests/                         # Comprehensive test suite
│   ├── unit/                      # Unit tests for individual modules
│   ├── integration/               # Integration tests for end-to-end functionality
│   └── fixtures/                  # Test data fixtures
├── data/                          # Data processing directory
│   ├── organized_links.json       # Processed link data
│   ├── scraped_data.json          # Scraped website content
│   └── scraped_data_text_extract.txt # Human-readable content extract
├── output/                        # Generated outputs
│   ├── extracted_concepts.json    # AI-extracted concepts
│   ├── extracted_concepts_text.txt # Text version of concepts
│   ├── political_platform.json    # Generated political platform
│   ├── political_platform.md      # Markdown documentation
│   ├── political_platform.html    # Interactive HTML version
│   └── platform_images/           # AI-generated images
├── cached_data/                   # Web scraping cache
├── logs/                          # Application logs
├── docs/                          # Documentation
├── bestofnow_urls.json           # Input URL collection
├── bestofnow_tags.json           # URL categorization tags
├── .env                          # Environment configuration
├── .cursorrules                  # IDE development guidelines
├── requirements.txt              # Python dependencies
├── pyrightconfig.json            # Python type checking config
└── README.md                     # This file
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file from `.env.example` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

   Additional optional environment variables:
   ```
   LOG_LEVEL=INFO          # Logging level (INFO, DEBUG, WARNING, ERROR)
   MAX_LINKS=100           # Maximum number of links to process
   GPT_MODEL=gpt-4         # OpenAI model to use
   TIMEOUT=30              # Request timeout in seconds
   MAX_CONCURRENT_REQUESTS=5   # Maximum concurrent scraping requests
   ```

5. Required input files:
   The pipeline expects the following input files in the project root:
   - `bestofnow_urls.json`: JSON file containing the links to analyze
   - `bestofnow_tags.json`: JSON file containing tags for the links

## Logging System

The project includes an enhanced logging system with the following features:

### 🎨 Colorful Emoji Logging

The logging system uses emojis and colors to make the terminal output more readable:

- 🚀 `START`: Beginning of a process
- ✅ `SUCCESS`: Successful operation
- ⏳ `PROCESSING`: Processing data
- 🔎 `SCRAPING`: Scraping websites
- 🔮 `EXTRACTING`: Extracting concepts
- 🧠 `ANALYZING`: Analyzing data
- ✨ `GENERATING`: Generating content
- 🎨 `RENDERING`: Rendering output
- 💾 `SAVING`: Saving data
- 📂 `LOADING`: Loading data
- ⏭️ `SKIPPED`: Skipped operation
- ❌ `ERROR`: Error in operation
- 🏁 `COMPLETE`: Completion of a process

### 📊 Enhanced Progress Bars

The progress bars now include:
- Emoji indicators
- Clear success/failure counters
- Better visual formatting
- Elapsed and estimated time remaining
- Percentage completion

### 🔍 Demo Script

To see a demonstration of the logging system:

```bash
./demo_logging.py
```

This demo showcases the various logging features without running the full pipeline.

## Pipeline Architecture

The Links Analysis Pipeline consists of six modular stages that work together to transform web content into comprehensive political platforms:

### 1. Data Organization (`organize_links.py`)
- **Input**: Raw URL collections and categorization tags
- **Process**: Categorizes links by topic (political, economic, social, technological)
- **Output**: Structured link data ready for scraping

### 2. Web Scraping (`scrape_sites.py`)
- **Input**: Organized link collections
- **Process**: Intelligent content extraction with caching and error handling
- **Output**: Structured website content (titles, headings, paragraphs, metadata)
- **Features**: Rate limiting, caching, BeautifulSoup parsing, user-agent rotation

### 3. Concept Extraction (`extract_concepts.py`)
- **Input**: Scraped website content
- **Process**: AI-powered analysis using GPT models to extract political concepts
- **Output**: Structured concepts with significance and implementation details
- **Features**: Context-aware prompting, error handling, batch processing

### 4. Platform Generation (`generate_platform.py`)
- **Input**: Extracted concepts by category
- **Process**: Synthesizes concepts into cohesive political platform sections
- **Output**: Comprehensive political platform with executive summary
- **Features**: Cross-category synthesis, executive summary generation

### 5. Content Rendering (`render_markdown.py`)
- **Input**: Generated political platform
- **Process**: Multi-format output generation (Markdown, HTML)
- **Output**: Professional documentation and interactive web versions
- **Features**: Responsive HTML design, collapsible sections, professional styling

### 6. Image Generation (`generate_images.py`)
- **Input**: Political platform content
- **Process**: AI image generation based on platform themes
- **Output**: Visual representations of key platform concepts
- **Features**: Thematic image prompts, multiple image generation, GPT-Image-1 integration

## Usage

### Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd links-analysis-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run the complete pipeline
python -m src.main
```

### Selective Execution

#### Run Individual Stages
```bash
# Data organization only
python -m src.main --only-organize

# Web scraping only
python -m src.main --only-scrape

# Concept extraction only
python -m src.main --only-extract

# Platform generation only
python -m src.main --only-analyze

# Content rendering only
python -m src.main --only-render

# Image generation only
python -m src.main --only-images
```

#### Skip Stages
```bash
# Skip web scraping (use cached data)
python -m src.main --skip-scrape

# Skip image generation (faster execution)
python -m src.main --skip-images
```

### Configuration

The pipeline supports various configuration options via environment variables:

```bash
# Processing limits
MAX_LINKS=100           # Maximum links to process
REQUEST_TIMEOUT=30      # Web request timeout (seconds)

# AI Model settings
GPT_MODEL=gpt-4o-mini   # OpenAI model to use
MAX_TOKENS=2000         # Maximum tokens per request

# Logging
LOG_LEVEL=INFO          # Logging verbosity
```

### Demo Mode

Experience the logging system without running the full pipeline:

```bash
python demo_logging.py
```

## Output

After running the pipeline:
1. Organized links will be saved to `data/organized_links.json`
2. Scraped content will be saved to `data/scraped_data.json`
3. Extracted concepts will be in `output/extracted_concepts.json` and `output/extracted_concepts_text.txt`
4. The generated political platform will be in `output/political_platform.json`
5. A formatted Markdown version of the platform will be in `output/political_platform.md`
6. An interactive HTML version of the platform will be in `output/political_platform.html`
7. Generated images based on the platform will be in `output/platform_images/`
8. Logs will be saved to `logs/`

## Pipeline Stages

### 1. Organize Links and Tags
Processes raw links and associated tags, categorizing them for analysis.

### 2. Scrape Websites
Downloads and extracts meaningful content from the websites, extracting paragraphs, headings, and lists while filtering out navigation and layout elements.

### 3. Extract Concepts
Processes each scraped website through an LLM to extract specific ideas, positions, and beliefs that would be relevant for a political platform. This creates a structured set of concepts and positions from varied sources.

### 4. Generate Political Platform
Analyzes the extracted concepts and synthesizes them into a coherent political platform, organized by category (political, economic, social, technological, etc.) with an executive summary.

### 5. Render Markdown and HTML
Converts the political platform from JSON format into:
- A well-formatted Markdown document with proper sections and formatting
- An interactive HTML document with tabs for different platform sections, collapsible content areas, and professional styling for better presentation and readability

### 6. Generate Images
Creates a set of 5 images based on the political platform content using OpenAI's GPT-Image-1:
- Generates images that visually represent key themes from the manifesto
- Creates images for different platform categories (political, economic, social, etc.)
- Saves the generated images in the `output/platform_images/` directory

## Dependencies

See `requirements.txt` for the full list of dependencies. 