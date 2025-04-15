"""
Module for extracting concepts and key ideas from scraped website content.

This module processes the scraped content through an LLM to extract specific ideas,
positions, and beliefs that would be relevant for a manifesto or political platform.
"""

import json
import os
from pathlib import Path
import openai
from tqdm import tqdm
from src.utils.logger import get_logger
from src.utils.config import SCRAPED_DATA_PATH, OUTPUT_DIR, OPENAI_KEY, GPT_MODEL, EXTRACTED_CONCEPTS_PATH

# Set up logger
logger = get_logger("extract_concepts", "concepts.log")

# Define output path for extracted concepts (no longer needed)
# CONCEPTS_PATH = OUTPUT_DIR / "extracted_concepts.json"

# Set up OpenAI API client
openai.api_key = OPENAI_KEY

def load_scraped_data(file_path):
    """
    Load scraped data from a JSON file.
    
    Args:
        file_path (str): Path to the scraped data JSON file.
        
    Returns:
        dict: Dictionary containing the scraped data.
    """
    logger.info(f"Loading scraped data from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading scraped data: {str(e)}")
        raise

def extract_concepts_from_document(document):
    """
    Extract concepts from a single document using an LLM.
    
    Args:
        document (dict): Document containing scraped content.
        
    Returns:
        dict: Dictionary containing the extracted concepts.
    """
    if document.get("status") != "success" or not document.get("content"):
        return {
            "url": document.get("url", "Unknown URL"),
            "title": document.get("title", "Unknown Title"),
            "concepts": [],
            "status": "skipped",
            "reason": "No content available"
        }
    
    try:
        # Extract content from the document
        content = document["content"]
        
        # Check if content is a string or dictionary and handle appropriately
        if not isinstance(content, dict):
            return {
                "url": document.get("url", "Unknown URL"),
                "title": document.get("title", "Unknown Title"),
                "concepts": [],
                "status": "skipped",
                "reason": "Content is not in expected format"
            }
            
        title = content.get("title", "No title")
        
        # Prepare the text to analyze
        text_to_analyze = f"Title: {title}\n\n"
        
        # Add headings - ensure it's a list before iterating
        if content.get("headings") and isinstance(content["headings"], list):
            text_to_analyze += "Headings:\n"
            for heading in content["headings"]:
                if isinstance(heading, dict) and "level" in heading and "text" in heading:
                    indent = "  " * (heading["level"] - 1)
                    text_to_analyze += f"{indent}* {heading['text']}\n"
            text_to_analyze += "\n"
        
        # Add paragraphs (limit to avoid token limits) - ensure it's a list before iterating
        if content.get("paragraphs") and isinstance(content["paragraphs"], list):
            paragraphs = content["paragraphs"]
            # Take first 5 and last 5 paragraphs if there are more than 10
            if len(paragraphs) > 10:
                selected_paragraphs = paragraphs[:5] + paragraphs[-5:]
            else:
                selected_paragraphs = paragraphs
                
            text_to_analyze += "Content:\n"
            for para in selected_paragraphs:
                if isinstance(para, str):
                    text_to_analyze += f"{para}\n\n"
        
        # Add lists - ensure it's a list before iterating
        if content.get("lists") and isinstance(content["lists"], list):
            text_to_analyze += "Lists:\n"
            for lst in content["lists"][:3]:  # Limit to 3 lists
                if isinstance(lst, dict) and "items" in lst and isinstance(lst["items"], list):
                    for i, item in enumerate(lst["items"]):
                        if isinstance(item, str):
                            text_to_analyze += f"  {i+1}. {item}\n"
        
        # Prepare the prompt for concept extraction
        prompt = f"""
Analyze the following content and extract specific ideas, positions, and beliefs that would be relevant for a manifesto or political platform. 

{text_to_analyze}

Extract the following in detail:
1. Key political ideas and positions expressed
2. Economic concepts or policies mentioned
3. Social values and principles advocated for
4. Technological or scientific perspectives
5. Environmental stances or approaches
6. All named people and bioregions

For each concept, include:
- A clear, concise title
- A detailed explanation of the concept
- Any specific implementation details mentioned
- Why this concept is significant for a political platform

Format your response as a structured list of concepts, being as specific and detailed as possible. Focus on extracting actionable ideas that could be incorporated into a political platform.
"""
        
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a skilled political analyst who excels at extracting specific, detailed concepts from text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        # Extract the generated content
        extracted_concepts = response.choices[0].message.content.strip()
        
        return {
            "url": document.get("url", "Unknown URL"),
            "title": title,
            "concepts": extracted_concepts,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error extracting concepts from document {document.get('url')}: {str(e)}")
        return {
            "url": document.get("url", "Unknown URL"),
            "title": document.get("title", "Unknown Title"),
            "concepts": [],
            "status": "error",
            "error": str(e)
        }

def extract_concepts(scraped_data):
    """
    Extract concepts from all scraped documents.
    
    Args:
        scraped_data (dict): Dictionary containing scraped data by category.
        
    Returns:
        dict: Dictionary containing the extracted concepts by category.
    """
    logger.info("Starting concept extraction process")
    extracted_data = {}
    
    # Count total documents
    total_docs = sum(len(docs) for docs in scraped_data.values())
    logger.info(f"Processing {total_docs} documents")
    
    # Create a progress bar
    progress_bar = tqdm(total=total_docs, desc="Extracting concepts")
    
    # Process each category
    for category, documents in scraped_data.items():
        logger.info(f"Processing {len(documents)} documents in category: {category}")
        extracted_data[category] = []
        
        for document in documents:
            # Extract concepts from the document
            result = extract_concepts_from_document(document)
            extracted_data[category].append(result)
            
            # Update progress bar
            progress_bar.update(1)
            
    # Close progress bar
    progress_bar.close()
    
    # Log results
    success_count = sum(1 for cat in extracted_data.values() for doc in cat if doc.get("status") == "success")
    error_count = sum(1 for cat in extracted_data.values() for doc in cat if doc.get("status") == "error")
    skipped_count = sum(1 for cat in extracted_data.values() for doc in cat if doc.get("status") == "skipped")
    
    logger.info(f"Concept extraction completed. Success: {success_count}, Error: {error_count}, Skipped: {skipped_count}")
    
    return extracted_data

def save_extracted_concepts(extracted_data, output_path):
    """
    Save the extracted concepts to a JSON file.
    
    Args:
        extracted_data (dict): Dictionary containing the extracted concepts.
        output_path (str): Path to save the extracted concepts.
    """
    logger.info(f"Saving extracted concepts to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2)
        logger.info("Extracted concepts saved successfully")
        
        # Also save a plain text version for easier review
        text_path = str(output_path).replace('.json', '_text.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            for category, items in extracted_data.items():
                f.write(f"=== CATEGORY: {category.upper()} ===\n\n")
                
                for i, item in enumerate(items):
                    if item.get("status") == "success":
                        f.write(f"[DOCUMENT {i+1}]\n")
                        f.write(f"URL: {item.get('url', 'Unknown URL')}\n")
                        f.write(f"TITLE: {item.get('title', 'Unknown Title')}\n\n")
                        f.write("EXTRACTED CONCEPTS:\n")
                        f.write(f"{item.get('concepts', 'No concepts extracted')}\n\n")
                        f.write("-" * 80 + "\n\n")
                
        logger.info(f"Text version saved to {text_path}")
        
    except Exception as e:
        logger.error(f"Error saving extracted concepts: {str(e)}")
        raise

def main():
    """
    Main function to extract concepts from scraped data.
    """
    logger.info("Starting concept extraction process")
    
    # Load scraped data
    scraped_data = load_scraped_data(SCRAPED_DATA_PATH)
    
    # Extract concepts
    extracted_data = extract_concepts(scraped_data)
    
    # Save extracted concepts
    save_extracted_concepts(extracted_data, EXTRACTED_CONCEPTS_PATH)
    
    logger.info("Concept extraction process completed")
    return extracted_data

if __name__ == "__main__":
    main() 