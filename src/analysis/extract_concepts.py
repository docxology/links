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
from src.utils.config import SCRAPED_DATA_PATH, OUTPUT_DIR, OPENAI_API_KEY, GPT_MODEL, EXTRACTED_CONCEPTS_PATH

# Set up logger
logger = get_logger("extract_concepts", "concepts.log")

# Define output path for extracted concepts (no longer needed)
# CONCEPTS_PATH = OUTPUT_DIR / "extracted_concepts.json"

# Set up OpenAI API client
from openai import OpenAI
from httpx import Client
http_client = Client(timeout=60.0)
client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)

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
        
        # Prepare the prompt for extracting Principles, Policies, Values, Goals
        prompt = f"""
Analyze the following content and extract information specifically related to these four categories:

{text_to_analyze}

**PRINCIPLES** (deep first values): Core philosophical foundations, fundamental beliefs, or guiding doctrines that represent the deepest level of what the content holds as fundamentally true or important.

**POLICIES** (actions of individuals and collectives): Specific proposals, concrete plans, strategies, or methods that individuals or groups should take to achieve outcomes.

**VALUES** (what matters): Moral or ethical standards, priorities, or ideals that are considered important - what the content indicates should be valued or protected.

**GOALS** (desired endpoints): Objectives, aims, targets, visions, or desired outcomes that the content seeks to achieve - the ultimate endpoints being pursued.

For each category, provide:
- Direct quotes or paraphrases from the content that support the extraction
- Detailed explanation of what the principle/policy/value/goal entails
- Context of how it relates to the overall content
- Any specific implementation details or examples mentioned

Format your response as a structured JSON with these exact keys:
{{
  "principles": [
    {{
      "title": "Clear, concise title",
      "content": "Direct quote or paraphrase from content",
      "explanation": "Detailed explanation of the deep first value",
      "context": "How it fits into the broader content",
      "implementation": "Any specific implementation details mentioned"
    }}
  ],
  "policies": [...],
  "values": [...],
  "goals": [...]
}}

Be comprehensive but focused - only include items that are clearly supported by the content. Focus on extracting actionable insights that reveal the content's core worldview and intentions. If a category has no relevant content, return an empty array for that category.
"""
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a skilled political analyst who excels at extracting specific, detailed concepts from text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )

        # Extract the generated content
        extracted_content = response.choices[0].message.content.strip()

        # Try to parse as JSON, if it fails, wrap in the expected structure
        try:
            # Look for JSON content within the response
            import re
            json_match = re.search(r'\{.*\}', extracted_content, re.DOTALL)
            if json_match:
                extracted_json = json.loads(json_match.group())
            else:
                extracted_json = json.loads(extracted_content)

            # Ensure all expected categories exist and validate structure
            extracted_data = {}
            for category in ["principles", "policies", "values", "goals"]:
                items = extracted_json.get(category, [])
                # Validate that each item has required fields
                validated_items = []
                for item in items:
                    if isinstance(item, dict) and "title" in item and "content" in item:
                        # Ensure all required fields exist
                        validated_item = {
                            "title": item.get("title", "No title"),
                            "content": item.get("content", "No content"),
                            "explanation": item.get("explanation", "No explanation"),
                            "context": item.get("context", ""),
                            "implementation": item.get("implementation", "")
                        }
                        validated_items.append(validated_item)
                extracted_data[category] = validated_items

        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed for {document.get('url')}: {str(e)}")
            # If JSON parsing fails, create a basic structure with the raw content
            extracted_data = {
                "principles": [{"title": "Raw Content", "content": extracted_content[:500], "explanation": "Could not parse structured data", "context": "", "implementation": ""}],
                "policies": [],
                "values": [],
                "goals": []
            }

        return {
            "url": document.get("url", "Unknown URL"),
            "title": title,
            "categories": extracted_data,
            "raw_response": extracted_content,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error extracting concepts from document {document.get('url')}: {str(e)}")
        return {
            "url": document.get("url", "Unknown URL"),
            "title": document.get("title", "Unknown Title"),
            "categories": {
                "principles": [],
                "policies": [],
                "values": [],
                "goals": []
            },
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

                        # Write out each category for this document
                        categories_data = item.get('categories', {})
                        for cat_name, cat_items in categories_data.items():
                            if cat_items:
                                f.write(f"**{cat_name.upper()}:**\n")
                                for cat_item in cat_items:
                                    f.write(f"• {cat_item.get('title', 'No title')}\n")
                                    f.write(f"  Content: {cat_item.get('content', 'No content')}\n")
                                    f.write(f"  Explanation: {cat_item.get('explanation', 'No explanation')}\n")
                                    if cat_item.get('context'):
                                        f.write(f"  Context: {cat_item.get('context')}\n")
                                    if cat_item.get('implementation'):
                                        f.write(f"  Implementation: {cat_item.get('implementation')}\n")
                                    f.write("\n")
                                f.write("\n")

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