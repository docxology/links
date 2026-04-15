"""
Module for generating images based on the political platform manifesto.

This module uses OpenAI's GPT-Image-1 model to generate images that visually represent
the key themes and concepts from the political platform. GPT-Image-1 provides
advanced text-to-image generation with superior quality and creative capabilities.
"""

import os
import json
import time
from pathlib import Path
import base64
import requests
from openai import OpenAI
from src.utils.logger import get_logger
from src.utils.config import PLATFORM_OUTPUT_PATH, OUTPUT_DIR, OPENAI_API_KEY

# Set up logger
logger = get_logger("generate_images", "images.log")

# Define image output directory
IMAGES_OUTPUT_DIR = OUTPUT_DIR / "platform_images"
IMAGES_OUTPUT_DIR.mkdir(exist_ok=True)

def load_platform_data(file_path):
    """
    Load political platform data from a JSON file.
    
    Args:
        file_path (str or Path): Path to the political platform JSON file.
        
    Returns:
        dict: Dictionary containing the political platform data.
    """
    logger.info(f"Loading political platform data from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading political platform data: {str(e)}")
        raise

def generate_image_prompts(platform_data, num_prompts=5):
    """
    Generate prompts for image creation based on the platform data.
    
    Args:
        platform_data (dict): Dictionary containing the political platform data.
        num_prompts (int): Number of prompts to generate.
        
    Returns:
        list: List of image generation prompts.
    """
    logger.info(f"Generating {num_prompts} image prompts from platform data")
    
    prompts = []

    # Get executive summary for overall theme
    if "executive_summary" in platform_data and platform_data["executive_summary"]:
        exec_summary = platform_data["executive_summary"]
        prompts.append(f"A symbolic representation of a political platform with themes of: {exec_summary[:500]}")

        # Extract key themes from executive summary for additional prompts
        if len(prompts) < num_prompts and "digital democracy" in exec_summary.lower():
            prompts.append("Digital democracy concept with interconnected networks, diverse people collaborating online, blockchain symbols, and democratic participation")
        if len(prompts) < num_prompts and "economic innovation" in exec_summary.lower():
            prompts.append("Economic innovation scene with sustainable businesses, community currencies, green technology, and collaborative workspaces")
        if len(prompts) < num_prompts and "environmental responsibility" in exec_summary.lower():
            prompts.append("Environmental responsibility illustration with renewable energy, community gardens, sustainable cities, and nature conservation")

    # Process each category to extract key themes
    categories = ["political", "economic", "social", "technological", "other"]

    for category in categories:
        if len(prompts) >= num_prompts:
            break

        if category in platform_data and platform_data[category] and platform_data[category] != "No data available for this category." and len(platform_data[category]) > 50:
            content = platform_data[category][:500]

            # Create more specific prompts based on category content
            if category == "other":
                if "digital democracy" in content.lower():
                    prompts.append(f"Digital democracy and decentralized governance with themes: {content[:300]}")
                elif "economic innovation" in content.lower():
                    prompts.append(f"Economic innovation and sustainable development with themes: {content[:300]}")
                elif "environmental responsibility" in content.lower():
                    prompts.append(f"Environmental stewardship and community sustainability with themes: {content[:300]}")
                else:
                    prompts.append(f"Innovative {category} policy and governance with themes: {content[:300]}")
            else:
                prompts.append(f"An inspirational and symbolic image representing {category} policy with themes of: {content}")

    # If we still need more prompts, create some based on combined themes
    if len(prompts) < num_prompts:
        prompts.append("A visually striking political campaign poster that represents progressive ideas and forward thinking")
    if len(prompts) < num_prompts:
        prompts.append("Futuristic cityscape with sustainable architecture, renewable energy, diverse community, and technological innovation")
    if len(prompts) < num_prompts:
        prompts.append("Community gathering with people of diverse backgrounds collaborating on environmental and social projects")
    
    # Trim list to exactly the number requested
    return prompts[:num_prompts]

def generate_images(prompts):
    """
    Generate images using OpenAI's GPT-Image-1 model.

    GPT-Image-1 provides advanced text-to-image generation with superior quality,
    creative capabilities, and flexible styling options.

    Args:
        prompts (list): List of image generation prompts.

    Returns:
        list: List of paths to saved images.
    """
    logger.info(f"Generating {len(prompts)} images using GPT-Image-1")

    from httpx import Client
    http_client = Client(timeout=60.0)
    client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
    image_paths = []

    for i, prompt in enumerate(prompts):
        try:
            logger.info(f"Generating image {i+1} with prompt: {prompt[:100]}...")

            response = client.images.generate(
                model="gpt-image-1",  # Use GPT-Image-1 model
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="hd",  # Use high definition for better quality
                style="vivid"  # Use vivid style for more creative results
            )

                        # Get image URL from response
            image_url = response.data[0].url

            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Save the image
                image_path = IMAGES_OUTPUT_DIR / f"platform_image_{i+1}.png"
                with open(str(image_path), 'wb') as f:
                    f.write(image_response.content)

                image_paths.append(image_path)
                logger.info(f"Image saved to {str(image_path)}")
            else:
                logger.error(f"Failed to download image: {image_response.status_code}")

            # Add a small delay to avoid rate limiting
            time.sleep(1)

        except Exception as e:
            logger.error(f"Error generating image {i+1}: {str(e)}")

    return image_paths

def main():
    """
    Main function to generate images from the political platform using GPT-Image-1.

    Returns:
        Path: Path to the directory containing generated images.
    """
    try:
        # Load platform data
        platform_data = load_platform_data(PLATFORM_OUTPUT_PATH)
        
        # Generate prompts
        prompts = generate_image_prompts(platform_data)
        
        # Generate images
        image_paths = generate_images(prompts)
        
        logger.info(f"Generated {len(image_paths)} images based on platform manifesto")
        logger.info(f"Images saved to {IMAGES_OUTPUT_DIR}")
        
        return IMAGES_OUTPUT_DIR
    
    except Exception as e:
        logger.error(f"Error in image generation process: {str(e)}")
        raise

if __name__ == "__main__":
    main() 