"""
Logging utility for the project.

This module provides a consistent way to log messages across all components.
With added emoji support and cleaner formatting for terminal output.
"""

import os
import logging
from pathlib import Path
import sys
from src.utils.config import LOGS_DIR, LOG_LEVEL

# Emoji mapping for different log levels and process stages
EMOJI = {
    'INFO': '✅ ',
    'WARNING': '⚠️ ',
    'ERROR': '❌ ',
    'DEBUG': '🔍 ',
    'CRITICAL': '🔥 ',
    # Process stages
    'START': '🚀 ',
    'COMPLETE': '🏁 ',
    'PROCESSING': '⏳ ',
    'SUCCESS': '✅ ',
    'FAILED': '❌ ',
    'SKIPPED': '⏭️ ',
    'SAVING': '💾 ',
    'LOADING': '📂 ',
    'SCRAPING': '🔎 ',
    'EXTRACTING': '🔮 ',
    'ANALYZING': '🧠 ',
    'GENERATING': '✨ ',
    'RENDERING': '🎨 ',
}

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors and emojis to log messages for terminal output
    """
    # ANSI color codes
    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
    }
    
    # Map log levels to colors
    LEVEL_COLORS = {
        'DEBUG': COLORS['BLUE'],
        'INFO': COLORS['GREEN'],
        'WARNING': COLORS['YELLOW'],
        'ERROR': COLORS['RED'],
        'CRITICAL': COLORS['MAGENTA'],
    }
    
    def format(self, record):
        # Get the original formatted message
        msg = super().format(record)
        level_name = record.levelname
        
        # Add emoji based on log level
        emoji = EMOJI.get(level_name, '')
        
        # Add color based on log level for terminal output
        if sys.stdout.isatty():  # Only use colors in real terminals, not in logs
            color = self.LEVEL_COLORS.get(level_name, self.COLORS['RESET'])
            return f"{color}{emoji}{msg}{self.COLORS['RESET']}"
        else:
            return f"{emoji}{msg}"

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
    
    # Create formatters
    # Cleaner and more concise formatter for console output
    console_formatter = ColoredFormatter(
        '%(message)s'  # Just show the message for cleaner console output
    )
    
    # More detailed formatter for file output
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(console_formatter)
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
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_with_emoji(logger, level, emoji_key, message):
    """
    Log a message with a specific emoji.
    
    Args:
        logger: The logger instance
        level: Log level (INFO, WARNING, etc.)
        emoji_key: Key for the emoji in the EMOJI dictionary
        message: Message to log
    """
    emoji = EMOJI.get(emoji_key, '')
    if level == 'INFO':
        logger.info(f"{emoji}{message}")
    elif level == 'WARNING':
        logger.warning(f"{emoji}{message}")
    elif level == 'ERROR':
        logger.error(f"{emoji}{message}")
    elif level == 'DEBUG':
        logger.debug(f"{emoji}{message}")
    elif level == 'CRITICAL':
        logger.critical(f"{emoji}{message}") 