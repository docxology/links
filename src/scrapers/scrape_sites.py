"""
Module for scraping website content from organized links.

This module takes the organized links and scrapes the content from the websites.
"""

import json
import os
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
import random
from src.utils.logger import get_logger
from src.utils.config import ORGANIZED_LINKS_PATH, SCRAPED_DATA_PATH, REQUEST_TIMEOUT, CACHE_DIR

# Set up logger
logger = get_logger("scrape_sites", "scraper.log")

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

def load_organized_links(file_path):
    """
    Load organized links from a JSON file.
    
    Args:
        file_path (str): Path to the organized links JSON file.
        
    Returns:
        dict: Dictionary containing the organized links data.
    """
    logger.info(f"Loading organized links from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading organized links: {str(e)}")
        raise

def get_cache_path(url):
    """
    Get the file path for cached website content.
    
    Args:
        url (str): URL of the website.
        
    Returns:
        str: Path for the cached file.
    """
    # Create a valid filename from the URL
    filename = url.replace('://', '_').replace('/', '_').replace('?', '_').replace('&', '_')
    if len(filename) > 200:  # Avoid filename too long errors
        filename = filename[:200]
    return os.path.join(CACHE_DIR, f"{filename}.html")

def is_cached(url):
    """
    Check if a URL is already cached.
    
    Args:
        url (str): URL to check.
        
    Returns:
        bool: True if cached, False otherwise.
    """
    cache_path = get_cache_path(url)
    return os.path.exists(cache_path)

def get_cached_content(url):
    """
    Get cached content for a URL.
    
    Args:
        url (str): URL to get cached content for.
        
    Returns:
        str or None: Cached HTML content or None if not cached.
    """
    cache_path = get_cache_path(url)
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading cache for {url}: {str(e)}")
    return None

def cache_content(url, content):
    """
    Cache website content.
    
    Args:
        url (str): URL of the website.
        content (str): HTML content to cache.
    """
    cache_path = get_cache_path(url)
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Error caching content for {url}: {str(e)}")

def extract_url_from_link(link):
    """
    Extract URL from a link object.
    
    Args:
        link (dict): Link data.
        
    Returns:
        str or None: URL if found, None otherwise.
    """
    # Try to get URL from different possible locations
    if isinstance(link, dict):
        # Direct url field
        if "url" in link:
            return link["url"]
        # Inside data field
        if "data" in link and isinstance(link["data"], dict):
            if "url" in link["data"]:
                return link["data"]["url"]
    
    logger.warning(f"Could not extract URL from link: {link}")
    return None

def extract_meaningful_content(soup):
    """
    Extract meaningful content from a webpage, focusing on article content.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object containing the HTML.
        
    Returns:
        dict: Dictionary containing extracted content and metadata.
    """
    # Extract title
    title = soup.title.string.strip() if soup.title else "No title found"
    
    # Initialize content storage
    content = {
        "title": title,
        "headings": [],
        "paragraphs": [],
        "lists": [],
        "full_text": ""
    }
    
    # First try to find the main content container
    main_content = None
    
    # Common content container selectors (in order of priority)
    content_selectors = [
        "article", "main", 
        ".post-content", ".article-content", ".entry-content", ".content", ".post",
        "#content", "#main", "#article", 
        "[role='main']", "[itemprop='articleBody']"
    ]
    
    # Try to find the main content container
    for selector in content_selectors:
        if selector.startswith('.') or selector.startswith('#') or selector.startswith('['):
            elements = soup.select(selector)
        else:
            elements = soup.find_all(selector)
            
        if elements:
            main_content = elements[0]
            break
    
    # If no main content container found, use the body
    if not main_content:
        main_content = soup.body if soup.body else soup
    
    # Extract headings (h1, h2, h3, etc.)
    headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        text = heading.get_text().strip()
        if text:
            content["headings"].append({
                "level": int(heading.name[1]),
                "text": text
            })
    
    # Extract paragraphs
    paragraphs = main_content.find_all('p')
    for p in paragraphs:
        text = p.get_text().strip()
        if text and len(text) > 20:  # Ignore very short paragraphs (likely not content)
            content["paragraphs"].append(text)
    
    # Extract lists
    lists = main_content.find_all(['ul', 'ol'])
    for list_elem in lists:
        list_items = []
        for item in list_elem.find_all('li'):
            text = item.get_text().strip()
            if text:
                list_items.append(text)
        
        if list_items:
            content["lists"].append({
                "type": list_elem.name,
                "items": list_items
            })
    
    # Combine all text for full-text search
    full_text = "\n\n".join([
        title,
        "\n".join([h["text"] for h in content["headings"]]),
        "\n\n".join(content["paragraphs"]),
        "\n".join(["\n".join(lst["items"]) for lst in content["lists"]])
    ])
    
    content["full_text"] = full_text
    
    return content

def scrape_url(url):
    """
    Scrape content from a single URL.
    
    Args:
        url (str): URL to scrape.
        
    Returns:
        dict: Dictionary containing the scraped content.
    """
    logger.info(f"Scraping URL: {url}")
    
    # Check cache first
    if is_cached(url):
        logger.info(f"Using cached content for {url}")
        html_content = get_cached_content(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract meaningful content
            extracted_content = extract_meaningful_content(soup)
            
            return {
                "url": url,
                "title": extracted_content["title"],
                "content": extracted_content,
                "status": "success",
                "source": "cache"
            }
    
    # If not cached or cache read failed, download the content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        # Cache the response
        cache_content(url, response.text)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract meaningful content
        extracted_content = extract_meaningful_content(soup)
        
        return {
            "url": url,
            "title": extracted_content["title"],
            "content": extracted_content,
            "status": "success",
            "source": "web"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return {
            "url": url,
            "title": None,
            "content": None,
            "status": "error",
            "error": str(e)
        }

def scrape_links(organized_links):
    """
    Scrape content from all organized links.
    
    Args:
        organized_links (dict): Dictionary containing organized links.
        
    Returns:
        dict: Dictionary containing scraped content by category.
    """
    logger.info("Starting scraping process")
    scraped_data = {}
    
    # For testing: limit to first 20 links only in each category
    for category in organized_links:
        if len(organized_links[category]) > 20:
            logger.info(f"Limiting {category} to first 20 links for testing")
            organized_links[category] = organized_links[category][:20]
    
    total_links = sum(len(links) for links in organized_links.values())
    logger.info(f"Total links to scrape: {total_links}")
    
    # Initialize counters for success and failure
    success_count = 0
    error_count = 0
    skipped_count = 0
    processed_count = 0
    
    # Create a progress bar for all links
    progress_bar = tqdm(total=total_links, desc=f"Scraping: {success_count} success, {error_count} failed, {skipped_count} skipped")
    
    # Scrape each category
    for category, links in organized_links.items():
        logger.info(f"Scraping {len(links)} links in category: {category}")
        scraped_data[category] = []
        
        for link in links:
            try:
                # Extract URL from link
                url = extract_url_from_link(link)
                
                if url:
                    # Add a random delay between requests (1-3 seconds)
                    delay = random.uniform(1, 3)
                    time.sleep(delay)
                    
                    scraped_content = scrape_url(url)
                    scraped_content["original_link"] = link
                    scraped_data[category].append(scraped_content)
                    
                    # Update counters based on scrape result
                    if scraped_content["status"] == "success":
                        success_count += 1
                    else:
                        error_count += 1
                else:
                    skipped_count += 1
                    logger.warning(f"Missing URL in link: {link}")
            except Exception as e:
                error_count += 1
                logger.error(f"Error processing link {link}: {str(e)}")
            
            # Update progress bar description with current counts
            progress_bar.set_description(f"Scraping: {success_count} success, {error_count} failed, {skipped_count} skipped")
            
            # Update progress bar
            progress_bar.update(1)
            
            # Increment processed count
            processed_count += 1
            
            # Save interim results every 20 links
            if processed_count % 20 == 0:
                logger.info(f"Saving interim results after processing {processed_count} links")
                try:
                    interim_path = str(SCRAPED_DATA_PATH).replace('.json', f'_interim.json')
                    with open(interim_path, 'w', encoding='utf-8') as f:
                        json.dump(scraped_data, f, indent=2)
                    logger.info(f"Interim results saved to {interim_path}")
                except Exception as e:
                    logger.error(f"Error saving interim results: {str(e)}")
    
    # Close progress bar
    progress_bar.close()
    
    # Log final statistics
    logger.info(f"Scraping completed. Success: {success_count}, Failed: {error_count}, Skipped: {skipped_count}")
    
    return scraped_data

def save_scraped_data(scraped_data, output_path):
    """
    Save scraped data to a JSON file.
    
    Args:
        scraped_data (dict): Dictionary containing scraped data.
        output_path (str): Path to save the scraped data.
    """
    logger.info(f"Saving scraped data to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Also save a plain text extract for easier analysis
    text_extract_path = str(output_path).replace('.json', '_text_extract.txt')
    logger.info(f"Saving text extract to {text_extract_path}")
    
    try:
        # Save the main JSON data
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2)
        logger.info("Scraped data saved successfully")
        
        # Save a plain text extract with just the content for easier analysis
        with open(text_extract_path, 'w', encoding='utf-8') as f:
            # For each category
            for category, items in scraped_data.items():
                f.write(f"--- CATEGORY: {category.upper()} ---\n\n")
                
                # For each item in the category
                for i, item in enumerate(items):
                    if item.get("status") == "success" and item.get("content"):
                        content = item["content"]
                        url = item["url"]
                        
                        f.write(f"[DOCUMENT {i+1}]\n")
                        f.write(f"URL: {url}\n")
                        f.write(f"TITLE: {content['title']}\n\n")
                        
                        # Write headings
                        if content.get("headings"):
                            f.write("HEADINGS:\n")
                            for heading in content["headings"]:
                                indent = "  " * (heading["level"] - 1)
                                f.write(f"{indent}* {heading['text']}\n")
                            f.write("\n")
                        
                        # Write paragraphs
                        if content.get("paragraphs"):
                            f.write("CONTENT:\n")
                            for para in content["paragraphs"]:
                                f.write(f"{para}\n\n")
                        
                        # Write lists
                        if content.get("lists"):
                            f.write("LISTS:\n")
                            for lst in content["lists"]:
                                for i, item in enumerate(lst["items"]):
                                    f.write(f"  {i+1}. {item}\n")
                            f.write("\n")
                        
                        f.write("-" * 80 + "\n\n")
                
        logger.info("Text extract saved successfully")
        
    except Exception as e:
        logger.error(f"Error saving scraped data: {str(e)}")
        raise

def main():
    """
    Main function to scrape websites.
    """
    logger.info("Starting web scraping process")
    
    # Load organized links
    organized_links = load_organized_links(ORGANIZED_LINKS_PATH)
    
    # Scrape website content
    scraped_data = scrape_links(organized_links)
    
    # Save scraped data
    save_scraped_data(scraped_data, SCRAPED_DATA_PATH)
    
    logger.info("Web scraping process completed")
    return scraped_data

if __name__ == "__main__":
    main() 