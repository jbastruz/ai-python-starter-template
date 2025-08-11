"""Logging configuration module using Loguru.

This module provides setup and configuration for structured logging using Loguru
with colored console output, ISO timestamps, and rotating file logs.
"""

import os
import sys
from pathlib import Path
from typing import Any

from loguru import logger

# Remove default handler
logger.remove()


def setup_logger(level: str = "INFO") -> None:
    """Configure loguru logger with console and file outputs.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Ensure logs directory exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Console handler with colors and ISO time format
    logger.add(
        sys.stderr,
        level=level.upper(),
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # File handler with rotation and retention
    logger.add(
        "logs/app.log",
        level=level.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    logger.info(f"Logger configured with level: {level.upper()}")


def get_logger() -> Any:
    """Get a configured logger instance.
    
    Returns:
        Configured loguru logger instance based on settings.log_level
    """
    try:
        # Import here to avoid circular imports
        from .config import settings
        
        # Setup logger if not already configured
        if not logger._core.handlers:
            setup_logger(settings.log_level)
        
        return logger
    except ImportError:
        # Fallback if config module is not available
        if not logger._core.handlers:
            setup_logger("INFO")
        return logger


# Export the configured logger
__all__ = ["setup_logger", "get_logger", "logger"]
