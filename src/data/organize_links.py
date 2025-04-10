"""
Module for organizing and categorizing links and tags.

This module processes the raw link data and organizes it into a structured format.
"""

import json
import os
from pathlib import Path
from tqdm import tqdm
from src.utils.logger import get_logger
from src.utils.config import RAW_LINKS_PATH, ORGANIZED_LINKS_PATH, MAX_LINKS

# Set up logger
logger = get_logger("organize_links", "organize.log")

def load_raw_links(file_path):
    """
    Load raw links from a JSON file.
    
    Args:
        file_path (str): Path to the raw links JSON file.
        
    Returns:
        dict: Dictionary containing the raw links data.
    """
    logger.info(f"Loading raw links from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_links = json.load(f)
            
            # Limit the number of links as per configuration
            if MAX_LINKS > 0 and len(raw_links) > MAX_LINKS:
                logger.info(f"Limiting to {MAX_LINKS} links as per configuration")
                raw_links = raw_links[:MAX_LINKS]
                
            return raw_links
    except Exception as e:
        logger.error(f"Error loading raw links: {str(e)}")
        raise

def categorize_links(links_data):
    """
    Categorize links based on their tags and content.
    
    Args:
        links_data (dict): Dictionary containing the raw links data.
        
    Returns:
        dict: Dictionary containing categorized links.
    """
    logger.info("Categorizing links")
    
    # Define category keywords for matching
    category_keywords = {
        "political": ["politics", "government", "election", "democracy", "policy", "law", "vote", "candidate", "legislation", "congress", "senate", "president", "parliament"],
        "economic": ["economy", "finance", "market", "business", "trade", "investment", "budget", "tax", "inflation", "gdp", "economic", "fiscal", "monetary", "banking"],
        "social": ["social", "society", "community", "education", "health", "welfare", "family", "culture", "religion", "ethnicity", "gender", "equality", "diversity", "inclusion"],
        "technological": ["technology", "innovation", "digital", "software", "hardware", "internet", "ai", "artificial intelligence", "app", "mobile", "computer", "tech", "automation", "robot"]
    }
    
    # Initialize categorized links dictionary
    categorized_links = {
        "political": [],
        "economic": [],
        "social": [],
        "technological": [],
        "other": []
    }
    
    # Create progress bar for categorization
    progress_bar = tqdm(total=len(links_data), desc="Categorizing links")
    
    # Process each link
    for link in links_data:
        url = link.get("url", "")
        title = link.get("title", "")
        description = link.get("description", "")
        tags = link.get("tags", [])
        
        # Combine all text fields for keyword matching
        combined_text = (url + " " + title + " " + description + " " + " ".join(tags)).lower()
        
        # Determine the best category match
        matched_category = None
        max_matches = 0
        
        for category, keywords in category_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in combined_text)
            if matches > max_matches:
                max_matches = matches
                matched_category = category
        
        # If no keywords matched, put in "other" category
        if not matched_category or max_matches == 0:
            categorized_links["other"].append(link)
        else:
            categorized_links[matched_category].append(link)
            
        # Update progress bar
        progress_bar.update(1)
    
    # Close progress bar
    progress_bar.close()
    
    # Log the number of links in each category
    for category, links in categorized_links.items():
        logger.info(f"Category '{category}': {len(links)} links")
    
    return categorized_links

def save_organized_links(organized_links, output_path):
    """
    Save organized links to a JSON file.
    
    Args:
        organized_links (dict): Dictionary containing organized links.
        output_path (str): Path to save the organized links.
    """
    logger.info(f"Saving organized links to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(organized_links, f, indent=2)
        logger.info("Organized links saved successfully")
    except Exception as e:
        logger.error(f"Error saving organized links: {str(e)}")
        raise

def main():
    """
    Main function to organize links.
    """
    logger.info("Starting link organization process")
    
    # Load raw links
    raw_links = load_raw_links(RAW_LINKS_PATH)
    
    # Categorize links
    organized_links = categorize_links(raw_links)
    
    # Save organized links
    save_organized_links(organized_links, ORGANIZED_LINKS_PATH)
    
    logger.info("Link organization process completed")
    return organized_links

if __name__ == "__main__":
    main() 