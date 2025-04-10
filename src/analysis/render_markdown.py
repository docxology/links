"""
Module for rendering the political platform JSON into well-formatted Markdown and HTML documents.

This module takes the generated political platform and creates:
1. A professional Markdown document with proper sections and formatting
2. An HTML document with nice styling and static interactivity
"""

import json
import os
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config import PLATFORM_OUTPUT_PATH, OUTPUT_DIR

# Set up logger
logger = get_logger("render_markdown", "markdown.log")

# Define output paths
MARKDOWN_OUTPUT_PATH = OUTPUT_DIR / "political_platform.md"
HTML_OUTPUT_PATH = OUTPUT_DIR / "political_platform.html"

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

def render_markdown(platform_data):
    """
    Render the platform data as a Markdown document.
    
    Args:
        platform_data (dict): Dictionary containing the political platform data.
        
    Returns:
        str: Markdown formatted text.
    """
    logger.info("Rendering political platform as Markdown")
    
    # Start with a title and the executive summary
    markdown = "# Political Platform\n\n"
    
    # Add executive summary if available
    if "executive_summary" in platform_data and platform_data["executive_summary"]:
        markdown += "## Executive Summary\n\n"
        markdown += platform_data["executive_summary"].replace("Executive Summary:", "").strip() + "\n\n"
    
    # Add a horizontal rule to separate the summary from the content
    markdown += "---\n\n"
    
    # Process each category
    categories = ["political", "economic", "social", "technological", "other"]
    
    for category in categories:
        if category in platform_data and platform_data[category] and platform_data[category] != f"No data available for this category.":
            # Add a section title with category name (capitalized)
            markdown += f"## {category.capitalize()} Platform\n\n"
            
            # Parse the content - it might be already structured with numbered sections
            content = platform_data[category]
            
            # Check if content has sections like "1. Overview:"
            if content.startswith("1. "):
                # Split by numbered sections
                sections = []
                current_section = ""
                lines = content.split("\n")
                
                for line in lines:
                    if line.strip() and any(line.strip().startswith(f"{i}. ") for i in range(1, 10)):
                        if current_section:
                            sections.append(current_section)
                        current_section = line + "\n"
                    else:
                        current_section += line + "\n"
                
                if current_section:
                    sections.append(current_section)
                
                # Process each section with proper Markdown formatting
                for section in sections:
                    if section.strip():
                        # Extract section title
                        section_title = section.split("\n")[0].strip()
                        if ":" in section_title:
                            title, _ = section_title.split(":", 1)
                            markdown += f"### {title}\n\n"
                        else:
                            markdown += f"### {section_title}\n\n"
                        
                        # Add the rest of the section content
                        content_lines = section.split("\n")[1:]
                        content_text = "\n".join(line for line in content_lines if line.strip())
                        markdown += content_text + "\n\n"
            else:
                # If content is not structured with numbered sections, just add it directly
                markdown += content + "\n\n"
    
    # Add a footer
    markdown += "---\n\n"
    markdown += "*This political platform was generated based on analysis of multiple sources " 
    markdown += "using AI-powered content extraction and synthesis.*\n"
    
    return markdown

def render_html(platform_data):
    """
    Render the platform data as an HTML document with nice formatting and static interactivity.
    
    Args:
        platform_data (dict): Dictionary containing the political platform data.
        
    Returns:
        str: HTML formatted text.
    """
    logger.info("Rendering political platform as HTML")
    
    # Define CSS styles for the HTML document
    css = """
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
            margin-top: 30px;
        }
        h3 {
            color: #3498db;
            margin-top: 25px;
            cursor: pointer;
        }
        h3::before {
            content: "▶ ";
            font-size: 0.8em;
            transition: transform 0.3s ease;
        }
        .section-content {
            margin-left: 20px;
            border-left: 1px solid #e0e0e0;
            padding-left: 15px;
            overflow: hidden;
            max-height: 0;
            transition: max-height 0.5s ease;
        }
        input[type="checkbox"] {
            display: none;
        }
        input[type="checkbox"]:checked + h3::before {
            content: "▼ ";
        }
        input[type="checkbox"]:checked + h3 + .section-content {
            max-height: 1000px;
        }
        .category-tabs {
            display: flex;
            margin: 20px 0;
            border-bottom: 1px solid #ddd;
        }
        .tab-button {
            background: none;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #7f8c8d;
            text-transform: capitalize;
        }
        .tab-button:hover {
            color: #3498db;
        }
        .tab-button.active {
            color: #2980b9;
            border-bottom: 3px solid #3498db;
        }
        .tab-content {
            display: none;
            padding: 15px 0;
        }
        .tab-content.active {
            display: block;
        }
        .executive-summary {
            background-color: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #3498db;
            margin-bottom: 30px;
        }
        hr {
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 30px 0;
        }
        .footer {
            font-style: italic;
            color: #7f8c8d;
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
        }
        /* JavaScript-less tab functionality */
        #tab1:checked ~ #content1,
        #tab2:checked ~ #content2,
        #tab3:checked ~ #content3,
        #tab4:checked ~ #content4,
        #tab5:checked ~ #content5 {
            display: block;
        }
        #tab1:checked ~ .tabs label[for="tab1"],
        #tab2:checked ~ .tabs label[for="tab2"],
        #tab3:checked ~ .tabs label[for="tab3"],
        #tab4:checked ~ .tabs label[for="tab4"],
        #tab5:checked ~ .tabs label[for="tab5"] {
            color: #2980b9;
            border-bottom: 3px solid #3498db;
        }
        .tabs {
            display: flex;
            margin: 20px 0;
            border-bottom: 1px solid #ddd;
        }
        .tabs label {
            background: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #7f8c8d;
            text-transform: capitalize;
        }
        .tabs label:hover {
            color: #3498db;
        }
        .tab-content {
            display: none;
            padding: 15px 0;
        }
    </style>
    """
    
    # Start HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Political Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    {css}
</head>
<body>
    <h1>Political Platform</h1>
    """
    
    # Add executive summary if available
    if "executive_summary" in platform_data and platform_data["executive_summary"]:
        summary_content = platform_data["executive_summary"].replace("Executive Summary:", "").strip()
        html += f"""
    <div class="executive-summary">
        <h2>Executive Summary</h2>
        <p>{summary_content}</p>
    </div>
    """
    
    # Setup for categories as tabs
    categories = ["political", "economic", "social", "technological", "other"]
    available_categories = [c for c in categories if c in platform_data and platform_data[c] and platform_data[c] != f"No data available for this category."]
    
    if available_categories:
        # Create radio buttons for tabs
        html += "    <!-- Static tab implementation with CSS only -->\n"
        for i, category in enumerate(available_categories, 1):
            checked = ' checked' if i == 1 else ''
            html += f'    <input type="radio" id="tab{i}" name="tabs"{checked} style="display:none;">\n'
        
        # Create tab buttons
        html += '    <div class="tabs">\n'
        for i, category in enumerate(available_categories, 1):
            html += f'        <label for="tab{i}">{category.capitalize()}</label>\n'
        html += '    </div>\n'
        
        # Create tab content sections
        for i, category in enumerate(available_categories, 1):
            content = platform_data[category]
            html += f'    <div id="content{i}" class="tab-content">\n'
            html += f'        <h2>{category.capitalize()} Platform</h2>\n'
            
            # Check if content has sections like "1. Overview:"
            if content.startswith("1. "):
                # Split by numbered sections
                sections = []
                current_section = ""
                lines = content.split("\n")
                
                for line in lines:
                    if line.strip() and any(line.strip().startswith(f"{i}. ") for i in range(1, 10)):
                        if current_section:
                            sections.append(current_section)
                        current_section = line + "\n"
                    else:
                        current_section += line + "\n"
                
                if current_section:
                    sections.append(current_section)
                
                # Process each section with proper HTML formatting and collapsible sections
                for j, section in enumerate(sections, 1):
                    if section.strip():
                        # Extract section title
                        section_title = section.split("\n")[0].strip()
                        if ":" in section_title:
                            title, _ = section_title.split(":", 1)
                        else:
                            title = section_title
                        
                        # Create collapsible section
                        checked = ' checked' if j <= 2 else ''  # Open first two sections by default
                        html += f'        <input type="checkbox" id="section-{category}-{j}"{checked}>\n'
                        html += f'        <h3><label for="section-{category}-{j}">{title}</label></h3>\n'
                        
                        # Add section content
                        content_lines = section.split("\n")[1:]
                        content_text = "\n".join(line for line in content_lines if line.strip())
                        # Format paragraphs properly
                        formatted_content = ""
                        for paragraph in content_text.split("\n\n"):
                            if paragraph.strip():
                                formatted_content += f"<p>{paragraph}</p>\n"
                        
                        html += f'        <div class="section-content">\n'
                        html += f'            {formatted_content}\n'
                        html += '        </div>\n'
            else:
                # If content is not structured with numbered sections, just add it directly as paragraphs
                paragraphs = content.split("\n\n")
                for paragraph in paragraphs:
                    if paragraph.strip():
                        html += f'        <p>{paragraph}</p>\n'
            
            html += '    </div>\n'
    
    # Add footer
    html += """
    <hr>
    <div class="footer">
        <p>This political platform was generated based on analysis of multiple sources using AI-powered content extraction and synthesis.</p>
    </div>
"""
    
    # End HTML document
    html += """
</body>
</html>
"""
    
    return html

def save_markdown(markdown_content, output_path):
    """
    Save the Markdown content to a file.
    
    Args:
        markdown_content (str): Markdown content to save.
        output_path (str or Path): Path to save the Markdown file.
    """
    logger.info(f"Saving Markdown to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        logger.info("Markdown saved successfully")
    except Exception as e:
        logger.error(f"Error saving Markdown: {str(e)}")
        raise

def save_html(html_content, output_path):
    """
    Save the HTML content to a file.
    
    Args:
        html_content (str): HTML content to save.
        output_path (str or Path): Path to save the HTML file.
    """
    logger.info(f"Saving HTML to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info("HTML saved successfully")
    except Exception as e:
        logger.error(f"Error saving HTML: {str(e)}")
        raise

def main():
    """
    Main function to render the political platform as Markdown and HTML.
    """
    logger.info("Starting rendering process")
    
    # Load platform data
    platform_data = load_platform_data(PLATFORM_OUTPUT_PATH)
    
    # Render Markdown
    markdown_content = render_markdown(platform_data)
    
    # Save Markdown
    save_markdown(markdown_content, MARKDOWN_OUTPUT_PATH)
    logger.info(f"Markdown saved to {MARKDOWN_OUTPUT_PATH}")
    
    # Render HTML
    html_content = render_html(platform_data)
    
    # Save HTML
    save_html(html_content, HTML_OUTPUT_PATH)
    logger.info(f"HTML saved to {HTML_OUTPUT_PATH}")
    
    logger.info("Rendering process completed")
    return MARKDOWN_OUTPUT_PATH, HTML_OUTPUT_PATH

if __name__ == "__main__":
    main() 