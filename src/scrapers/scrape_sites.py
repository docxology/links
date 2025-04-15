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
from tqdm.auto import tqdm  # Use tqdm.auto to automatically select the best progress bar
import random
from src.utils.logger import get_logger, log_with_emoji, EMOJI
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
    log_with_emoji(logger, 'INFO', 'LOADING', f"Loading organized links from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_with_emoji(logger, 'ERROR', 'ERROR', f"Error loading organized links: {str(e)}")
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
    Check if a URL's content is cached.
    
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
        str or None: Cached content if available, None otherwise.
    """
    cache_path = get_cache_path(url)
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Error reading cache for {url}: {str(e)}")
            return None
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
    Extract meaningful content from a BeautifulSoup object.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the page HTML.
        
    Returns:
        dict: Dictionary containing the extracted content.
    """
    # Extract title
    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text().strip()
    else:
        # Try to find a suitable heading as the title
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text().strip()
    
    # Extract main content
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text:
            paragraphs.append(text)
    
    # Extract headings
    headings = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for h in soup.find_all(tag):
            text = h.get_text().strip()
            if text and text not in headings:
                headings.append(text)
    
    # Extract lists
    list_items = []
    for li in soup.find_all('li'):
        text = li.get_text().strip()
        if text:
            list_items.append(text)
    
    # Extract structured data (metadata tags)
    metadata = {}
    
    # OpenGraph tags
    og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
    for tag in og_tags:
        if tag.get('content'):
            metadata[tag['property']] = tag['content']
    
    # Twitter card tags
    twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
    for tag in twitter_tags:
        if tag.get('content'):
            metadata[tag['name']] = tag['content']
    
    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        metadata['description'] = meta_desc['content']
    
    # Meta keywords
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords and meta_keywords.get('content'):
        metadata['keywords'] = meta_keywords['content']
    
    return {
        "title": title,
        "paragraphs": paragraphs,
        "headings": headings,
        "list_items": list_items,
        "metadata": metadata
    }

def scrape_url(url):
    """
    Scrape content from a single URL.
    
    Args:
        url (str): URL to scrape.
        
    Returns:
        dict: Dictionary containing the scraped content.
    """
    log_with_emoji(logger, 'INFO', 'SCRAPING', f"Scraping URL: {url}")
    
    # Check cache first
    if is_cached(url):
        log_with_emoji(logger, 'INFO', 'LOADING', f"Using cached content for {url}")
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
        log_with_emoji(logger, 'ERROR', 'ERROR', f"Error scraping {url}: {str(e)}")
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
    log_with_emoji(logger, 'INFO', 'START', "Starting scraping process")
    scraped_data = {}
    
    # For testing: limit to first 20 links only in each category
    for category in organized_links:
        if len(organized_links[category]) > 20:
            log_with_emoji(logger, 'INFO', 'INFO', f"Limiting {category} to first 20 links for testing")
            organized_links[category] = organized_links[category][:20]
    
    total_links = sum(len(links) for links in organized_links.values())
    log_with_emoji(logger, 'INFO', 'INFO', f"Total links to scrape: {total_links}")
    
    # Initialize counters for success and failure
    success_count = 0
    error_count = 0
    skipped_count = 0
    processed_count = 0
    
    # Create a progress bar with improved formatting
    progress_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    progress_bar = tqdm(
        total=total_links,
        desc=f"{EMOJI['SCRAPING']}Scraping: {success_count} success, {error_count} failed, {skipped_count} skipped",
        bar_format=progress_format,
        ncols=100  # Set fixed width for cleaner display
    )
    
    # Save interim results every 10 links
    interim_save_interval = 10
    
    # Scrape each category
    for category, links in organized_links.items():
        log_with_emoji(logger, 'INFO', 'PROCESSING', f"Scraping {len(links)} links in category: {category}")
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
            
            # Update progress bar description with current counts and emoji
            progress_bar.set_description(
                f"{EMOJI['SCRAPING']}Scraping: {success_count} success, {error_count} failed, {skipped_count} skipped"
            )
            
            # Update progress bar
            progress_bar.update(1)
            
            # Increment processed count
            processed_count += 1
            
            # Save interim results periodically
            if processed_count % interim_save_interval == 0:
                log_with_emoji(logger, 'INFO', 'SAVING', f"Saving interim results after processing {processed_count} links")
                interim_file = str(SCRAPED_DATA_PATH).replace('.json', '_interim.json')
                try:
                    with open(interim_file, 'w', encoding='utf-8') as f:
                        json.dump(scraped_data, f, indent=2)
                    log_with_emoji(logger, 'INFO', 'SUCCESS', f"Interim results saved to {interim_file}")
                except Exception as e:
                    logger.error(f"Error saving interim results: {str(e)}")
    
    # Close the progress bar
    progress_bar.close()
    
    # Log the final results
    log_with_emoji(logger, 'INFO', 'COMPLETE', f"Scraping completed. Success: {success_count}, Failed: {error_count}, Skipped: {skipped_count}")
    
    return scraped_data

def save_scraped_data(scraped_data, output_path):
    """
    Save scraped data to a JSON file.
    
    Args:
        scraped_data (dict): Dictionary containing scraped data.
        output_path (str): Path to save the scraped data.
    """
    log_with_emoji(logger, 'INFO', 'SAVING', f"Saving scraped data to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Also save a plain text extract for easier analysis
    text_extract_path = str(output_path).replace('.json', '_text_extract.txt')
    log_with_emoji(logger, 'INFO', 'SAVING', f"Saving text extract to {text_extract_path}")
    
    try:
        # Save the main JSON data
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2)
        log_with_emoji(logger, 'INFO', 'SUCCESS', "Scraped data saved successfully")
        
        # Save a plain text extract with just the content for easier analysis
        with open(text_extract_path, 'w', encoding='utf-8') as f:
            f.write(f"SCRAPED CONTENT EXTRACT\n")
            f.write(f"======================\n\n")
            
            for category, items in scraped_data.items():
                f.write(f"CATEGORY: {category.upper()}\n")
                f.write(f"{'=' * (len(category) + 10)}\n\n")
                
                for item in items:
                    if item["status"] == "success" and item["content"]:
                        f.write(f"URL: {item['url']}\n")
                        f.write(f"TITLE: {item['title']}\n")
                        f.write(f"{'-' * 40}\n\n")
                        
                        content = item["content"]
                        
                        # Write paragraphs
                        if content["paragraphs"]:
                            f.write("PARAGRAPHS:\n")
                            for p in content["paragraphs"]:
                                f.write(f"- {p}\n\n")
                        
                        # Write list items
                        if content["list_items"]:
                            f.write("LIST ITEMS:\n")
                            for li in content["list_items"]:
                                f.write(f"* {li}\n")
                            f.write("\n")
                        
                        f.write(f"{'-' * 80}\n\n")
        
        log_with_emoji(logger, 'INFO', 'SUCCESS', "Text extract saved successfully")
    except Exception as e:
        log_with_emoji(logger, 'ERROR', 'ERROR', f"Error saving data: {str(e)}")

def main():
    """
    Main function to scrape websites.
    """
    log_with_emoji(logger, 'INFO', 'START', "Starting web scraping process")
    
    # Load organized links
    organized_links = load_organized_links(ORGANIZED_LINKS_PATH)
    
    # Scrape website content
    scraped_data = scrape_links(organized_links)
    
    # Save scraped data
    save_scraped_data(scraped_data, SCRAPED_DATA_PATH)
    
    log_with_emoji(logger, 'INFO', 'COMPLETE', "Web scraping process completed")
    return scraped_data

if __name__ == "__main__":
    main() 