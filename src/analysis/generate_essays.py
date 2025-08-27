"""
Module for generating overview essays from compiled principles, policies, values, and goals.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any
from src.utils.logger import get_logger
from openai import OpenAI
from httpx import Client

# Set up logger
logger = get_logger("generate_essays", "essays.log")

# Set up OpenAI API client
from src.utils.config import OPENAI_KEY, GPT_MODEL
http_client = Client(timeout=120.0)
client = OpenAI(api_key=OPENAI_KEY, http_client=http_client)

def load_compiled_data(compiled_dir: Path) -> Dict[str, Any]:
    """
    Load compiled data for all categories.

    Args:
        compiled_dir: Directory containing compiled JSON files

    Returns:
        Dictionary with compiled data for each category
    """
    compiled_data = {}
    categories = ["principles", "policies", "values", "goals"]

    for category in categories:
        json_file = compiled_dir / f"{category}.json"
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                compiled_data[category] = data.get("items", [])
        else:
            compiled_data[category] = []

    return compiled_data

def generate_essay(category: str, items: List[Dict[str, Any]]) -> str:
    """
    Generate an overview essay for a specific category with proper source attribution.

    Args:
        category: The category name (principles, policies, values, goals)
        items: List of items in that category

    Returns:
        Generated essay text
    """
    if not items:
        return f"No {category} found to generate an essay."

    # Create a source index for better referencing
    sources = {}
    for i, item in enumerate(items[:25], 1):  # Increased limit for better coverage
        source_title = item.get('source_title', 'Unknown Source')
        source_url = item.get('source_url', 'Unknown URL')
        sources[f"Source {i}"] = {
            'title': source_title,
            'url': source_url
        }

    # Prepare the content for the LLM with enhanced source information
    items_text = ""
    for i, item in enumerate(items[:25], 1):  # Increased limit for better coverage
        items_text += f"[Source {i}] {item.get('source_title', 'Unknown Source')}\n"
        items_text += f"   URL: {item.get('source_url', 'Unknown URL')}\n"
        items_text += f"   {category.title()}: {item.get('title', 'No title')}\n"
        items_text += f"   Content: {item.get('content', 'No content')}\n"
        items_text += f"   Explanation: {item.get('explanation', 'No explanation')}\n"
        if item.get('context'):
            items_text += f"   Context: {item.get('context')}\n"
        if item.get('implementation'):
            items_text += f"   Implementation: {item.get('implementation')}\n"
        items_text += "\n"

    prompt = f"""
Based on the following collected {category} from various online sources, write a comprehensive overview essay with meticulous source attribution.

SOURCE INDEX:
{chr(10).join([f"[Source {i}] {sources[f'Source {i}']['title']}" for i in range(1, len(sources) + 1)])}

{category.upper()} DATA:
{items_text}

Write an essay that:

1. **Introduction**: Provide an overview of the main themes and patterns observed across these {category.lower()} from diverse sources

2. **Analysis**: Analyze the key ideas, showing connections and relationships between different {category.lower()} while ALWAYS attributing each idea to its source

3. **Synthesis**: Create a coherent narrative that weaves together the most significant and recurring {category.lower()}, comparing and contrasting how different sources approach similar themes

4. **Conclusion**: Discuss the implications and potential impact of these {category.lower()} when considered together

CRITICAL REQUIREMENTS FOR SOURCE ATTRIBUTION:
- **MANDATORY SOURCE CITATION**: Every single {category.lower()} or idea discussed MUST be attributed to its source using the format: "[Source X] Source Title"
- **DIRECT QUOTES REQUIRED**: For each major point, include direct quotes from the source content using the format: "As [Source X] states: '[exact quote from content field]'"
- **SOURCE COMPARISON**: When discussing related {category.lower()}, compare how different sources approach the same theme (e.g., "While [Source 1] emphasizes X, [Source 2] focuses on Y")
- **NO GENERIC REFERENCES**: Never use generic terms like "some sources" or "various articles" - always reference specific sources by their [Source X] identifier
- **URL REFERENCES**: When appropriate, include source URLs in parentheses for additional credibility

ESSAY STRUCTURE REQUIREMENTS:
- Use the source index [Source X] format consistently throughout
- Group related {category.lower()} by theme, clearly showing which sources contribute to each theme
- Highlight agreements and disagreements between sources
- Show evolution of ideas across different sources
- End each major section with a synthesis statement that connects multiple sources

QUALITY STANDARDS:
- **ZERO TOLERANCE FOR UNCITED CLAIMS**: Every claim about a {category.lower()} must include source citation and supporting evidence
- **MINIMUM CITATION DENSITY**: Aim for at least 8-12 source citations per 1000 words
- **QUOTE INTEGRATION**: Integrate quotes naturally into the analysis, not as standalone elements
- **SOURCE CONTEXT**: When citing a source, briefly explain its context or perspective to help readers understand the source's viewpoint

Style guidelines:
- Write in an academic but accessible tone
- Be comprehensive but focused on the most significant patterns
- Show rather than tell - use specific examples from the data with proper attribution
- Maintain objectivity while highlighting important insights
- Aim for 900-1300 words
- **MANDATORY**: Every claim about a {category.lower()} must include source citation and supporting quote

Format the essay with proper headings and subheadings. Begin each major claim with its source attribution.
"""

    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": f"You are an expert academic writer specializing in synthesizing information from multiple sources into well-attributed, insightful analyses of {category.lower()}. You excel at proper source attribution and creating meaningful connections between different perspectives."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3500,
            temperature=0.3  # Lower temperature for more focused, attribution-heavy writing
        )

        essay = response.choices[0].message.content.strip()

        # Post-process to ensure source index is included at the top of the essay
        source_index_text = "\n\n**Source Index:**\n" + "\n".join([f"[Source {i}] {sources[f'Source {i}']['title']} ({sources[f'Source {i}']['url']})" for i in range(1, len(sources) + 1)])

        return essay + source_index_text

    except Exception as e:
        logger.error(f"Error generating essay for {category}: {str(e)}")
        return f"Error generating essay: {str(e)}"

def generate_category_essay(category: str, items: List[Dict[str, Any]], output_dir: Path) -> Path:
    """
    Generate and save an essay for a specific category.

    Args:
        category: The category name
        items: List of items in that category
        output_dir: Directory to save the essay

    Returns:
        Path to the saved essay file
    """
    logger.info(f"Generating essay for {category} ({len(items)} items)")

    essay = generate_essay(category, items)

    # Save the essay
    essay_file = output_dir / f"{category}_essay.md"
    with open(essay_file, 'w', encoding='utf-8') as f:
        f.write(f"# {category.title()} Overview Essay\n\n")
        f.write(f"Generated from {len(items)} collected {category.lower()}\n\n")
        f.write("---\n\n")
        f.write(essay)

    logger.info(f"Essay saved to {essay_file}")

    # Validate essay quality
    validation_results = validate_essay_quality(essay, category)

    # Log validation results
    logger.info(f"Essay validation completed for {category}")

    return essay_file

def main():
    """
    Main function to generate essays for all categories.
    """
    from src.utils.config import OUTPUT_DIR

    essays_dir = OUTPUT_DIR / "essays"
    essays_dir.mkdir(exist_ok=True, parents=True)

    compiled_dir = OUTPUT_DIR / "compiled"

    if not compiled_dir.exists():
        logger.error(f"Compiled directory not found: {compiled_dir}")
        return

    logger.info("Starting essay generation process")

    # Load compiled data
    compiled_data = load_compiled_data(compiled_dir)

    # Generate essays for each category
    generated_essays = {}
    for category, items in compiled_data.items():
        if items:  # Only generate essays for categories with data
            essay_file = generate_category_essay(category, items, essays_dir)
            generated_essays[category] = str(essay_file)
        else:
            logger.info(f"No data found for {category}, skipping essay generation")

    logger.info(f"Essay generation completed. Essays saved to {essays_dir}")

    return {
        "essays_dir": str(essays_dir),
        "generated_essays": generated_essays
    }

def validate_essay_quality(essay_content: str, category: str) -> Dict[str, Any]:
    """
    Validate the quality of generated essays to ensure they meet requirements.

    Args:
        essay_content: The generated essay content
        category: The category name

    Returns:
        Dictionary with validation results
    """
    validation_results = {
        "has_source_citations": False,
        "has_quotes": False,
        "citation_count": 0,
        "quote_count": 0,
        "word_count": len(essay_content.split()),
        "has_structure": False,
        "has_source_index": False,
        "quotes_with_sources": 0,
        "url_references": 0
    }

    # Check for source citations using multiple patterns
    citation_patterns = [
        r"As seen in\s+[^,]+",
        r"The\s+[^.]+\s+articulates",
        r"[^.]+\s+exemplifies",
        r"According to\s+[^,]+",
        r"[^.]+\s+states:",
        r"[^.]+\s+describes",
        r"\[Source \d+\]",  # Specific pattern for [Source X] format
        r"Source \d+",      # Alternative Source X format
    ]

    for pattern in citation_patterns:
        matches = re.findall(pattern, essay_content, re.IGNORECASE)
        validation_results["citation_count"] += len(matches)
        if matches:
            validation_results["has_source_citations"] = True

    # Check for source index presence
    validation_results["has_source_index"] = "**Source Index:**" in essay_content or "Source Index" in essay_content

    # Check for proper quote integration with source attribution
    quote_with_source_pattern = r'\[Source \d+\][^"]*"[^"]{10,}"'
    quote_matches_with_source = re.findall(quote_with_source_pattern, essay_content)
    validation_results["quotes_with_sources"] = len(quote_matches_with_source)

    # Check for URL references
    url_pattern = r'https?://[^\s)]+'
    url_matches = re.findall(url_pattern, essay_content)
    validation_results["url_references"] = len(url_matches)

    # Check for quotes (looking for quotation marks with content)
    quote_matches = re.findall(r'"[^"]{10,}"', essay_content)  # Quotes with at least 10 characters
    validation_results["quote_count"] = len(quote_matches)
    validation_results["has_quotes"] = len(quote_matches) > 0

    # Check for proper essay structure
    structure_indicators = ["## Introduction", "## Analysis", "## Synthesis", "## Conclusion"]
    validation_results["has_structure"] = any(indicator in essay_content for indicator in structure_indicators)

    logger.info(f"Essay quality validation for {category}:")
    logger.info(f"  - Has source citations: {validation_results['has_source_citations']}")
    logger.info(f"  - Has quotes: {validation_results['has_quotes']}")
    logger.info(f"  - Citation count: {validation_results['citation_count']}")
    logger.info(f"  - Quote count: {validation_results['quote_count']}")
    logger.info(f"  - Quotes with sources: {validation_results['quotes_with_sources']}")
    logger.info(f"  - Has source index: {validation_results['has_source_index']}")
    logger.info(f"  - URL references: {validation_results['url_references']}")
    logger.info(f"  - Word count: {validation_results['word_count']}")
    logger.info(f"  - Has structure: {validation_results['has_structure']}")

    return validation_results

if __name__ == "__main__":
    main()
