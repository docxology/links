"""
Module for generating a political platform based on scraped website content.

This module analyzes the scraped website content and generates a political platform.
"""

import json
import os
from pathlib import Path
import openai
from tqdm import tqdm
from src.utils.logger import get_logger
from src.utils.config import SCRAPED_DATA_PATH, EXTRACTED_CONCEPTS_PATH, PLATFORM_OUTPUT_PATH, OPENAI_KEY, GPT_MODEL

# Set up logger
logger = get_logger("generate_platform", "platform.log")

# Set up OpenAI API client
openai.api_key = OPENAI_KEY

def load_extracted_concepts(file_path):
    """
    Load extracted concepts from a JSON file.
    
    Args:
        file_path (str): Path to the extracted concepts JSON file.
        
    Returns:
        dict: Dictionary containing the extracted concepts.
    """
    logger.info(f"Loading extracted concepts from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading extracted concepts: {str(e)}")
        raise

def prepare_prompt(category, documents):
    """
    Prepare a prompt for the GPT model based on the category and concepts.
    
    Args:
        category (str): The category of the documents.
        documents (list): List of documents with extracted concepts.
        
    Returns:
        str: Prompt for the GPT model.
    """
    # Extract successful documents with concepts
    valid_docs = [
        doc for doc in documents 
        if doc.get("status") == "success" and doc.get("concepts")
    ]
    
    # Get all concepts from these documents
    concepts_list = []
    for doc in valid_docs[:10]:  # Limit to 10 documents
        title = doc.get("title", "No title")
        concepts = doc.get("concepts", "")
        concepts_list.append(f"Source: {title}\n\n{concepts}")
    
    # Format the prompt
    prompt = """
You are a political analyst tasked with generating a comprehensive political platform based on the following extracted concepts from the '{}' category:

{}
{}
{}

Based on these concepts, generate a coherent political platform section on {} issues. Include:
1. A concise overview of the key positions and values
2. 5-7 specific policy proposals based on the concepts
3. Brief justifications for each proposal
4. A concluding statement that ties these positions together

Make sure the platform is balanced, realistic, and directly based on the extracted concepts provided.
Integrate similar ideas from different sources, and resolve any contradictions by taking a moderate position.
""".format(
        category,
        '=' * 40,
        '\n\n'.join(concepts_list),
        '=' * 40,
        category
    )
    return prompt

def generate_section(category, documents):
    """
    Generate a platform section for a category using GPT.
    
    Args:
        category (str): The category to generate a platform for.
        documents (list): List of documents with extracted concepts.
        
    Returns:
        str: Generated platform section.
    """
    logger.info(f"Generating platform section for category: {category}")
    
    try:
        # Prepare the prompt
        prompt = prepare_prompt(category, documents)
        
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful political analyst who excels at synthesizing diverse concepts into a coherent political platform."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        # Extract and return the generated content
        generated_text = response.choices[0].message.content.strip()
        return generated_text
    except Exception as e:
        logger.error(f"Error generating platform for {category}: {str(e)}")
        return f"Error generating platform for {category}: {str(e)}"

def generate_platform(extracted_data):
    """
    Generate a political platform based on the extracted concepts.
    
    Args:
        extracted_data (dict): Dictionary containing extracted concepts by category.
        
    Returns:
        dict: Dictionary containing the generated platform by category.
    """
    logger.info("Starting platform generation process")
    platform = {}
    
    # Generate platform for each category
    for category, documents in extracted_data.items():
        if documents:
            platform[category] = generate_section(category, documents)
        else:
            logger.warning(f"No documents found for category: {category}")
            platform[category] = "No data available for this category."
    
    # Generate an executive summary
    try:
        # Prepare a summary prompt
        summary_prompt = "Based on the following political platform sections, create an executive summary that presents a cohesive overview of the entire platform. Focus on highlighting the key themes, values, and proposals across all categories, and how they interconnect to form a unified vision:\n\n"
        for category, section in platform.items():
            summary_prompt += f"=== {category.upper()} ===\n{section}\n\n"
        
        # Generate the summary
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a skilled political strategist who excels at synthesizing complex policy ideas into compelling, accessible summaries."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        
        # Add the summary to the platform
        platform["executive_summary"] = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating executive summary: {str(e)}")
        platform["executive_summary"] = "Error generating executive summary."
    
    return platform

def save_platform(platform, output_path):
    """
    Save the generated platform to a JSON file.
    
    Args:
        platform (dict): Dictionary containing the generated platform.
        output_path (str): Path to save the platform.
    """
    logger.info(f"Saving generated platform to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(platform, f, indent=2)
        logger.info("Platform saved successfully")
    except Exception as e:
        logger.error(f"Error saving platform: {str(e)}")
        raise

def main():
    """
    Main function to generate a political platform.
    """
    logger.info("Starting platform generation process")
    
    # Load extracted concepts
    extracted_data = load_extracted_concepts(EXTRACTED_CONCEPTS_PATH)
    
    # Generate platform
    platform = generate_platform(extracted_data)
    
    # Save platform
    save_platform(platform, PLATFORM_OUTPUT_PATH)
    
    logger.info("Platform generation process completed")
    return platform

if __name__ == "__main__":
    main() 