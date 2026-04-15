"""
Module for generating images from essay content using OpenAI's image generation API.
"""

import json
import re
from pathlib import Path
from typing import Any, List

import requests
from httpx import Client
from openai import OpenAI

from src.utils.config import OPENAI_API_KEY, ESSAY_IMAGE_MODEL, GPT_MODEL
from src.utils.logger import get_logger

logger = get_logger("generate_essay_images", "images.log")

http_client = Client(timeout=120.0)
client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)


def _parse_two_prompt_strings(raw: str) -> List[str]:
    """
    Parse model output into exactly two non-empty string prompts.
    Raises ValueError if the response is not a strict JSON array of two strings.
    """
    text = raw.strip()
    try:
        parsed: Any = json.loads(text)
    except json.JSONDecodeError:
        pass
    else:
        if isinstance(parsed, list) and len(parsed) == 2:
            if all(isinstance(x, str) and x.strip() for x in parsed):
                return [parsed[0].strip(), parsed[1].strip()]
        raise ValueError("Expected a JSON array of exactly two non-empty strings")

    # Some models wrap JSON in markdown fences
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        return _parse_two_prompt_strings(fence.group(1))

    raise ValueError("Could not parse two image prompts as JSON array of strings")


def extract_image_prompts_from_essay(essay_content: str, category: str) -> List[str]:
    """
    Ask the chat model for exactly two image prompts; strict JSON array of two strings.

    Args:
        essay_content: The full essay text
        category: The category name (for context)

    Returns:
        List of 2 image prompt strings

    Raises:
        ValueError: If the model output is not a valid JSON array of two strings.
    """
    prompt = f"""Based on the following essay about {category}, create 2 detailed image prompts that would visually represent the key themes and concepts discussed.

ESSAY CONTENT:
{essay_content[:2000]}

Create 2 distinct image prompts that capture different aspects of the essay's main ideas about {category}. Each prompt should be:

1. Visually descriptive and detailed, focusing on the conceptual essence of {category}
2. Represent the philosophical and practical dimensions discussed in the essay
3. Professional and thought-provoking, suitable for academic/professional context
4. Abstract/metaphorical rather than literal representations

Consider the core themes of the essay when creating prompts - these should visually represent the deep values, actions, important matters, and desired endpoints that are discussed.

Format your response as a JSON array with exactly 2 prompts (strings only, no other keys):
["prompt 1", "prompt 2"]

Make sure each prompt is optimized for AI image generation and captures the intellectual depth of the essay's content."""

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a creative visual designer who creates compelling image prompts based on complex ideas. Reply with only a JSON array of two strings.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7,
    )

    prompts_text = response.choices[0].message.content
    if not prompts_text:
        raise ValueError("Empty response from chat model for image prompts")

    return _parse_two_prompt_strings(prompts_text)


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

    Raises:
        RuntimeError: If generation or download fails.
    """
    logger.info(f"Generating image {image_number} for {category}: {prompt[:100]}...")

    response = client.images.generate(
        model=ESSAY_IMAGE_MODEL,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    if not image_url:
        raise RuntimeError("Image API returned no URL")

    image_response = requests.get(image_url, timeout=120)
    image_response.raise_for_status()

    image_filename = f"{category}_image_{image_number}.png"
    image_path = output_dir / image_filename

    with open(image_path, "wb") as f:
        f.write(image_response.content)

    logger.info(f"Image saved to {image_path}")
    return str(image_path)


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

    with open(essay_file, "r", encoding="utf-8") as f:
        essay_content = f.read()

    prompts = extract_image_prompts_from_essay(essay_content, category)
    logger.info(f"Generated prompts: {prompts}")

    generated_images: List[str] = []
    for i, p in enumerate(prompts, 1):
        image_path = generate_image(p, category, i, output_dir)
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

    essay_files = list(essays_dir.glob("*_essay.md"))
    generated_images = {}

    for essay_file in essay_files:
        category = essay_file.stem.replace("_essay", "")
        images = generate_images_for_essay(essay_file, category, images_dir)
        generated_images[category] = images

    logger.info(f"Image generation completed. Images saved to {images_dir}")

    summary_file = images_dir / "generation_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_categories": len(generated_images),
                "categories": generated_images,
            },
            f,
            indent=2,
        )

    return {
        "images_dir": str(images_dir),
        "generated_images": generated_images,
    }


if __name__ == "__main__":
    main()
