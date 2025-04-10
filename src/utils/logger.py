"""
Logging utility for the project.

This module provides a consistent way to log messages across all components.
"""

import os
import logging
from pathlib import Path
from src.utils.config import LOGS_DIR, LOG_LEVEL

def get_logger(name, log_file=None):
    """
    Get a logger with the specified name and configuration.
    
    Args:
        name (str): Name of the logger (typically the module name)
        log_file (str, optional): Name of the log file. If None, only console logging is used.
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Remove existing handlers to avoid duplicates when reusing loggers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is provided
    if log_file:
        # Create logs directory if it doesn't exist
        LOGS_DIR.mkdir(exist_ok=True)
        
        # Create file handler
        file_handler = logging.FileHandler(
            LOGS_DIR / log_file,
            mode='a',
            encoding='utf-8'
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger 