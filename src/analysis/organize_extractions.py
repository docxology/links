"""
Module for organizing extracted principles, policies, values, and goals into site-specific and compiled formats.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from src.utils.logger import get_logger

# Set up logger
logger = get_logger("organize_extractions", "organize.log")

def create_site_specific_structure(extracted_data: Dict[str, Any], output_dir: Path) -> Path:
    """
    Create site-specific files with scraped content organized by extracted categories.

    Args:
        extracted_data: Dictionary containing extracted data by category
        output_dir: Base output directory

    Returns:
        Path to the site-specific folder
    """
    site_specific_dir = output_dir / "site_specific"
    site_specific_dir.mkdir(exist_ok=True, parents=True)

    logger.info(f"Creating site-specific structure in {site_specific_dir}")

    for category_name, documents in extracted_data.items():
        category_dir = site_specific_dir / category_name
        category_dir.mkdir(exist_ok=True)

        for doc_idx, document in enumerate(documents):
            if document.get("status") != "success":
                continue

            url = document.get("url", "unknown")
            # Create a safe filename from URL
            safe_filename = "".join(c for c in url if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_filename:
                safe_filename = f"document_{doc_idx}"

            doc_file = category_dir / f"{safe_filename}.json"

            # Structure the document with original content and extracted categories
            doc_data = {
                "url": document.get("url"),
                "title": document.get("title"),
                "categories": document.get("categories", {}),
                "raw_response": document.get("raw_response", "")
            }

            with open(doc_file, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, indent=2)

    return site_specific_dir

def create_compiled_structure(extracted_data: Dict[str, Any], output_dir: Path) -> Path:
    """
    Create compiled files with principles, policies, values, goals aggregated across sites.

    Args:
        extracted_data: Dictionary containing extracted data by category
        output_dir: Base output directory

    Returns:
        Path to the compiled folder
    """
    compiled_dir = output_dir / "compiled"
    compiled_dir.mkdir(exist_ok=True, parents=True)

    logger.info(f"Creating compiled structure in {compiled_dir}")

    # Initialize compiled data structure
    compiled_data = {
        "principles": [],
        "policies": [],
        "values": [],
        "goals": []
    }

    # Aggregate data from all documents
    for category_name, documents in extracted_data.items():
        for document in documents:
            if document.get("status") != "success":
                continue

            doc_url = document.get("url", "unknown")
            doc_title = document.get("title", "unknown")
            categories = document.get("categories", {})

            # Add each item from each category with source information
            for cat_name, items in categories.items():
                for item in items:
                    compiled_item = {
                        "source_url": doc_url,
                        "source_title": doc_title,
                        **item
                    }
                    compiled_data[cat_name].append(compiled_item)

    # Save compiled data for each category
    for cat_name, items in compiled_data.items():
        if items:  # Only save non-empty categories
            category_file = compiled_dir / f"{cat_name}.json"
            with open(category_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "category": cat_name,
                    "count": len(items),
                    "items": items
                }, f, indent=2)

            # Also create a text summary
            text_file = compiled_dir / f"{cat_name}_summary.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"=== {cat_name.upper()} SUMMARY ===\n\n")
                f.write(f"Total items: {len(items)}\n\n")

                for i, item in enumerate(items, 1):
                    f.write(f"{i}. {item.get('title', 'No title')}\n")
                    f.write(f"   Source: {item.get('source_title', 'Unknown')} ({item.get('source_url', 'Unknown URL')})\n")
                    f.write(f"   Content: {item.get('content', 'No content')}\n")
                    f.write(f"   Explanation: {item.get('explanation', 'No explanation')}\n")
                    if item.get('context'):
                        f.write(f"   Context: {item.get('context')}\n")
                    if item.get('implementation'):
                        f.write(f"   Implementation: {item.get('implementation')}\n")
                    f.write("\n" + "-"*80 + "\n\n")

    return compiled_dir

def main():
    """
    Main function to organize extracted data into site-specific and compiled formats.
    """
    from src.utils.config import OUTPUT_DIR, EXTRACTED_CONCEPTS_PATH

    logger.info("Starting organization of extracted data")

    # Load extracted data
    if not EXTRACTED_CONCEPTS_PATH.exists():
        logger.error(f"Extracted concepts file not found: {EXTRACTED_CONCEPTS_PATH}")
        return

    with open(EXTRACTED_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        extracted_data = json.load(f)

    # Create site-specific structure
    site_specific_dir = create_site_specific_structure(extracted_data, OUTPUT_DIR)

    # Create compiled structure
    compiled_dir = create_compiled_structure(extracted_data, OUTPUT_DIR)

    logger.info(f"Organization completed. Site-specific: {site_specific_dir}, Compiled: {compiled_dir}")

    return {
        "site_specific_dir": str(site_specific_dir),
        "compiled_dir": str(compiled_dir)
    }

if __name__ == "__main__":
    main()
