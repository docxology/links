"""
Demo script to show the improved logging with emojis and progress bars.

This script demonstrates the various logging levels and progress bar display.
"""

import time
import sys
import random
from tqdm.auto import tqdm
from src.utils.logger import get_logger, log_with_emoji, EMOJI

# Set up logger
logger = get_logger("demo", "demo.log")

def demo_logger():
    """Demonstrate various logging levels with emojis."""
    print("\n=== LOGGING DEMO ===\n")
    
    # Demo different log levels
    log_with_emoji(logger, 'INFO', 'START', "Starting demo of improved logging")
    log_with_emoji(logger, 'INFO', 'INFO', "This is a regular info message")
    log_with_emoji(logger, 'WARNING', 'WARNING', "This is a warning message")
    log_with_emoji(logger, 'ERROR', 'ERROR', "This is an error message")
    log_with_emoji(logger, 'DEBUG', 'DEBUG', "This is a debug message (may not show depending on log level)")
    
    # Demo process-specific emojis
    log_with_emoji(logger, 'INFO', 'LOADING', "Loading data from a file")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'PROCESSING', "Processing the loaded data")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'SCRAPING', "Scraping website content")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'EXTRACTING', "Extracting concepts from text")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'ANALYZING', "Analyzing extracted concepts")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'GENERATING', "Generating a platform from analysis")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'RENDERING', "Rendering platform as markdown")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'SAVING', "Saving results to disk")
    time.sleep(0.5)
    log_with_emoji(logger, 'INFO', 'SUCCESS', "Task completed successfully")
    log_with_emoji(logger, 'INFO', 'FAILED', "Task failed (demo only)")
    log_with_emoji(logger, 'INFO', 'SKIPPED', "Task skipped (demo only)")
    log_with_emoji(logger, 'INFO', 'COMPLETE', "All demo tasks completed")

def demo_progress_bar():
    """Demonstrate improved progress bars with emojis."""
    print("\n=== PROGRESS BAR DEMO ===\n")
    
    log_with_emoji(logger, 'INFO', 'START', "Starting progress bar demo")
    
    # Define progress bar format
    progress_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    
    # Demo simple progress bar
    total_items = 20
    progress_bar = tqdm(
        total=total_items,
        desc=f"{EMOJI['PROCESSING']}Processing items",
        bar_format=progress_format,
        ncols=100
    )
    
    # Process items
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for i in range(total_items):
        # Simulate processing
        time.sleep(0.25)
        
        # Simulate random outcomes
        outcome = random.choices(['success', 'error', 'skipped'], [0.7, 0.2, 0.1])[0]
        
        if outcome == 'success':
            success_count += 1
        elif outcome == 'error':
            error_count += 1
        else:
            skipped_count += 1
        
        # Update progress bar description
        progress_bar.set_description(
            f"{EMOJI['PROCESSING']}Processing: {success_count} success, {error_count} errors, {skipped_count} skipped"
        )
        
        # Update progress
        progress_bar.update(1)
    
    # Close progress bar
    progress_bar.close()
    
    log_with_emoji(logger, 'INFO', 'COMPLETE', f"Progress bar demo completed: {success_count} success, {error_count} errors, {skipped_count} skipped")

def demo_pipeline():
    """Demonstrate a simplified pipeline with logging and progress bars."""
    print("\n=== PIPELINE DEMO ===\n")
    
    log_with_emoji(logger, 'INFO', 'START', "Starting demo pipeline")
    
    # Stage 1: Data Loading
    log_with_emoji(logger, 'INFO', 'LOADING', "Stage 1: Loading data")
    time.sleep(1)
    log_with_emoji(logger, 'INFO', 'COMPLETE', "Stage 1 completed")
    
    # Stage 2: Data Processing with progress bar
    log_with_emoji(logger, 'INFO', 'PROCESSING', "Stage 2: Processing data")
    
    progress_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    items = range(10)
    
    # Create and run progress bar
    with tqdm(
        total=len(items),
        desc=f"{EMOJI['PROCESSING']}Processing items",
        bar_format=progress_format,
        ncols=100
    ) as pbar:
        for _ in items:
            # Simulate processing
            time.sleep(0.5)
            pbar.update(1)
    
    log_with_emoji(logger, 'INFO', 'COMPLETE', "Stage 2 completed")
    
    # Stage 3: Analysis
    log_with_emoji(logger, 'INFO', 'ANALYZING', "Stage 3: Analyzing data")
    time.sleep(1.5)
    log_with_emoji(logger, 'INFO', 'COMPLETE', "Stage 3 completed")
    
    # Stage 4: Results Generation
    log_with_emoji(logger, 'INFO', 'GENERATING', "Stage 4: Generating results")
    time.sleep(1)
    log_with_emoji(logger, 'INFO', 'COMPLETE', "Stage 4 completed")
    
    # Final completion message
    log_with_emoji(logger, 'INFO', 'COMPLETE', "Pipeline demo completed successfully")

if __name__ == "__main__":
    demo_logger()
    demo_progress_bar()
    demo_pipeline() 