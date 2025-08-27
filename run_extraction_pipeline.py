#!/usr/bin/env python3
"""
Convenience script to run the complete extraction pipeline for Principles, Policies, Values, and Goals.

This script runs:
1. Extraction of categories from scraped sites
2. Organization into site-specific and compiled formats
3. Generation of overview essays
4. Generation of images from essays

Usage:
    python run_extraction_pipeline.py

Or with specific stages:
    python run_extraction_pipeline.py --only-extract
    python run_extraction_pipeline.py --only-organize-extractions
    python run_extraction_pipeline.py --only-essays
    python run_extraction_pipeline.py --only-essay-images
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Run the extraction pipeline with all stages."""
    project_root = Path(__file__).resolve().parent

    # Change to project directory
    os.chdir(project_root)

    # Activate virtual environment if it exists
    venv_path = project_root / "venv" / "bin" / "activate"
    if venv_path.exists():
        activate_cmd = f"source {venv_path}"
        python_cmd = f"{project_root}/venv/bin/python"
    else:
        activate_cmd = ""
        python_cmd = sys.executable

    # Build the command
    if activate_cmd:
        cmd = f"{activate_cmd} && {python_cmd} -m src.main"
    else:
        cmd = f"{python_cmd} -m src.main"

    # Get command line arguments (excluding the script name)
    args = sys.argv[1:]
    if not args:
        # Run all new stages by default
        args = [
            "--skip-organize",
            "--skip-scrape",
            "--skip-analyze",
            "--skip-render",
            "--skip-images"
        ]

    full_cmd = f"{cmd} {' '.join(args)}"

    print("🚀 Running Extraction Pipeline")
    print(f"Command: {full_cmd}")
    print("-" * 50)

    # Run the command
    result = subprocess.run(full_cmd, shell=True, capture_output=False)

    if result.returncode == 0:
        print("\n✅ Pipeline completed successfully!")
        print("\n📁 Output locations:")
        print(f"   Site-specific files: {project_root}/output/site_specific/")
        print(f"   Compiled data: {project_root}/output/compiled/")
        print(f"   Essays: {project_root}/output/essays/")
        print(f"   Essay images: {project_root}/output/essay_images/")
    else:
        print(f"\n❌ Pipeline failed with exit code {result.returncode}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
