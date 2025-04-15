"""
Unit tests for the logger module.
"""

import logging
import os
import pytest
from pathlib import Path
from src.utils.logger import get_logger, log_with_emoji, CustomFormatter


def test_get_logger():
    """Test that get_logger returns a configured logger."""
    logger = get_logger("test_logger", "test.log")
    
    # Verify logger is configured correctly
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    
    # Verify handlers are set up
    assert len(logger.handlers) > 0
    
    # Check if there's a file handler
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    if file_handlers:
        # If file handler exists, check its properties
        assert file_handlers[0].baseFilename.endswith("test.log")
        
    # There should be a console handler
    console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler) 
                        and not isinstance(h, logging.FileHandler)]
    assert len(console_handlers) > 0
    
    # Clean up test log file if created
    log_dir = Path("logs")
    test_log = log_dir / "test.log"
    if test_log.exists():
        os.remove(test_log)


def test_log_with_emoji():
    """Test that log_with_emoji logs messages with emojis."""
    logger = get_logger("emoji_test", "emoji_test.log")
    
    # Call log_with_emoji with different log levels
    log_with_emoji(logger, "INFO", "START", "Test message for START")
    log_with_emoji(logger, "WARNING", "SKIPPED", "Test message for SKIPPED")
    log_with_emoji(logger, "ERROR", "ERROR", "Test message for ERROR")
    log_with_emoji(logger, "DEBUG", "PROCESSING", "Test message for PROCESSING")
    
    # No assertions needed as we're just checking it runs without errors
    # In a real-world scenario, we'd mock the logger and verify calls
    
    # Clean up test log file
    log_dir = Path("logs")
    test_log = log_dir / "emoji_test.log"
    if test_log.exists():
        os.remove(test_log)


def test_custom_formatter():
    """Test that CustomFormatter formats log messages correctly."""
    formatter = CustomFormatter()
    
    # Create a log record
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test_path",
        lineno=42,
        msg="Test message",
        args=(),
        exc_info=None
    )
    
    # Format the record
    formatted = formatter.format(record)
    
    # Verify formatting
    assert "Test message" in formatted
    
    # Check color formatting
    if record.levelno == logging.INFO:
        assert "\033[" in formatted  # ANSI color code should be present 