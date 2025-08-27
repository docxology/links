"""
Module for generating images from essay content using OpenAI's image generation API.
"""

import json
import os
import requests
from pathlib import Path
from typing import Dict, List, Any
from src.utils.logger import get_logger
from openai import OpenAI
from httpx import Client

# Set up logger
logger = get_logger("generate_essay_images", "images.log")

# Set up OpenAI API client
from src.utils.config import OPENAI_KEY, IMAGE_MODEL
http_client = Client(timeout=120.0)
client = OpenAI(api_key=OPENAI_KEY, http_client=http_client)

def extract_image_prompts_from_essay(essay_content: str, category: str) -> List[str]:
    """
    Extract or generate image prompts from essay content.

    Args:
        essay_content: The full essay text
        category: The category name (for context)

    Returns:
        List of 2 image prompts
    """
    # Create prompts based on the essay content
    prompt = f"""
Based on the following essay about {category}, create 2 detailed image prompts that would visually represent the key themes and concepts discussed.

ESSAY CONTENT:
{essay_content[:2000]}  # Limit for token efficiency

Create 2 distinct image prompts that capture different aspects of the essay's main ideas about {category}. Each prompt should be:

1. Visually descriptive and detailed, focusing on the conceptual essence of {category}
2. Represent the philosophical and practical dimensions discussed in the essay
3. Professional and thought-provoking, suitable for academic/professional context
4. Abstract/metaphorical rather than literal representations

Consider the core themes of the essay when creating prompts - these should visually represent the deep values, actions, important matters, and desired endpoints that are discussed.

Format your response as a JSON array with exactly 2 prompts:
["prompt 1", "prompt 2"]

Make sure each prompt is optimized for AI image generation and captures the intellectual depth of the essay's content.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 for generating prompts
            messages=[
                {"role": "system", "content": "You are a creative visual designer who creates compelling image prompts based on complex ideas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        prompts_text = response.choices[0].message.content.strip()

        # Try to parse as JSON
        try:
            prompts = json.loads(prompts_text)
            if isinstance(prompts, list) and len(prompts) == 2:
                return prompts
        except:
            pass

        # Fallback: extract prompts manually
        import re
        prompt_matches = re.findall(r'"([^"]+)"', prompts_text)
        if len(prompt_matches) >= 2:
            return prompt_matches[:2]

        # Final fallback: create generic prompts based on category
        return [
            f"Abstract visualization representing key concepts in {category}",
            f"Conceptual artwork depicting themes of {category} in modern society"
        ]

    except Exception as e:
        logger.error(f"Error generating image prompts: {str(e)}")
        return [
            f"Abstract visualization representing key concepts in {category}",
            f"Conceptual artwork depicting themes of {category} in modern society"
        ]

def generate_image(prompt: str, category: str, image_number: int, output_dir: Path) -> str:
    """
    Generate a single image from a prompt.

    Args:
        prompt: The image prompt
        category: The category name
        image_number: Image number (1 or 2)
        output_dir: Directory to save the image

    Returns:
        Path to the generated image
    """
    try:
        logger.info(f"Generating image {image_number} for {category}: {prompt[:100]}...")

        response = client.images.generate(
            model="dall-e-3",  # Use DALL-E 3 which is more widely available
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        image_url = response.data[0].url

        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        # Save the image
        image_filename = f"{category}_image_{image_number}.png"
        image_path = output_dir / image_filename

        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        logger.info(f"Image saved to {image_path}")
        return str(image_path)

    except Exception as e:
        logger.error(f"Error generating image for {category}: {str(e)}")
        return ""

def generate_images_for_essay(essay_file: Path, category: str, output_dir: Path) -> List[str]:
    """
    Generate 2 images for a specific essay.

    Args:
        essay_file: Path to the essay file
        category: The category name
        output_dir: Directory to save images

    Returns:
        List of paths to generated images
    """
    logger.info(f"Generating images for {category} essay")

    # Read the essay content
    try:
        with open(essay_file, 'r', encoding='utf-8') as f:
            essay_content = f.read()
    except Exception as e:
        logger.error(f"Error reading essay file {essay_file}: {str(e)}")
        return []

    # Extract image prompts from the essay
    prompts = extract_image_prompts_from_essay(essay_content, category)
    logger.info(f"Generated prompts: {prompts}")

    # Generate images
    generated_images = []
    for i, prompt in enumerate(prompts, 1):
        image_path = generate_image(prompt, category, i, output_dir)
        if image_path:
            generated_images.append(image_path)

    return generated_images

def main():
    """
    Main function to generate images for all essays.
    """
    from src.utils.config import OUTPUT_DIR

    essays_dir = OUTPUT_DIR / "essays"
    images_dir = OUTPUT_DIR / "essay_images"
    images_dir.mkdir(exist_ok=True, parents=True)

    if not essays_dir.exists():
        logger.error(f"Essays directory not found: {essays_dir}")
        return

    logger.info("Starting image generation process")

    # Find all essay files
    essay_files = list(essays_dir.glob("*_essay.md"))
    generated_images = {}

    for essay_file in essay_files:
        category = essay_file.stem.replace("_essay", "")
        images = generate_images_for_essay(essay_file, category, images_dir)
        generated_images[category] = images

    logger.info(f"Image generation completed. Images saved to {images_dir}")

    # Save a summary of generated images
    summary_file = images_dir / "generation_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total_categories": len(generated_images),
            "categories": generated_images
        }, f, indent=2)

    return {
        "images_dir": str(images_dir),
        "generated_images": generated_images
    }

if __name__ == "__main__":
    main()
