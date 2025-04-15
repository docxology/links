#!/usr/bin/env python3
"""
Demo script to run the demo_logger module that showcases
the improved logging with emojis and progress bars.
"""

import os
import sys
from pathlib import Path

# Add the project directory to sys.path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_DIR))

# Import the demo logger
from src.utils.demo_logger import demo_logger, demo_progress_bar, demo_pipeline

if __name__ == "__main__":
    print("=== LOGGING SYSTEM DEMO ===")
    print("This demo showcases the improved logging system with emojis and progress bars.\n")
    
    # Run the individual demos
    demo_logger()
    demo_progress_bar()
    demo_pipeline()
    
    print("\nDemo complete! To run the full pipeline with improved logging, use:")
    print("python -m src.main") 