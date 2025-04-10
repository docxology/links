# Links Analysis

A project to analyze links from a collection, scrape their content, and generate a political platform using LLMs.

## Project Structure

```
/
├── src/                    # Source code
│   ├── utils/              # Utility functions
│   ├── data/               # Data processing scripts
│   ├── scrapers/           # Web scraping scripts
│   ├── analysis/           # Content analysis and generation scripts
│   └── main.py             # Main script to run the entire pipeline
├── data/                   # Data directory
│   ├── raw/                # Raw input data
│   └── processed/          # Processed data
├── output/                 # Generated output files
│   ├── extracted_concepts.json    # Extracted concepts from scraped content
│   ├── extracted_concepts_text.txt # Text version of extracted concepts
│   ├── political_platform.json    # Generated political platform
│   ├── political_platform.md      # Markdown version of the platform
│   ├── political_platform.html    # Interactive HTML version of the platform
│   └── platform_images/          # Generated images for the platform
├── cached_data/            # Cached data for faster processing
├── logs/                   # Log files
├── bestofnow_urls.json     # Input URLs for analysis
├── bestofnow_tags.json     # Tags for the input URLs
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md               # This file
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

## Running the Pipeline

The pipeline consists of six stages:
1. Organize links and tags
2. Scrape websites
3. Extract concepts from scraped content
4. Generate a political platform
5. Render the platform as a formatted Markdown document
6. Generate images based on the platform manifesto

### Run the entire pipeline:

```
python -m src.main
```

### Run specific stages:

To run only the organization step:
```
python -m src.main --only-organize
```

To run only the scraping step:
```
python -m src.main --only-scrape
```

To run only the concept extraction step:
```
python -m src.main --only-extract
```

To run only the platform generation step:
```
python -m src.main --only-analyze
```

To run only the Markdown rendering step:
```
python -m src.main --only-render
```

To run only the image generation step:
```
python -m src.main --only-images
```

### Skip specific stages:

To skip the organization step:
```
python -m src.main --skip-organize
```

To skip the scraping step:
```
python -m src.main --skip-scrape
```

To skip the concept extraction step:
```
python -m src.main --skip-extract
```

To skip the platform generation step:
```
python -m src.main --skip-analyze
```

To skip the Markdown rendering step:
```
python -m src.main --skip-render
```

To skip the image generation step:
```
python -m src.main --skip-images
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
Creates a set of 5 images based on the political platform content using OpenAI's DALL-E:
- Generates images that visually represent key themes from the manifesto
- Creates images for different platform categories (political, economic, social, etc.)
- Saves the generated images in the `output/platform_images/` directory

## Dependencies

See `requirements.txt` for the full list of dependencies. 