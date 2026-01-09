"""
Logging utilities for DataLab.

Demonstrates:
- Using Python's built-in 'logging' module (standardbibliotek!)
- Different log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Logging to both console and file
- Custom formatters with timestamps
- Creating reusable logger configuration

This replaces simple print() with proper logging infrastructure.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from datalab import config


# === LOGGER SETUP ===
def _setup_logger():
    """
    Configure and return the DataLab logger.

    Demonstrates:
    - Creating a named logger
    - Adding multiple handlers (console + file)
    - Setting different log levels
    - Custom formatting with datetime

    Returns:
        Configured logger instance
    """
    # Create logger with specific name
    logger = logging.getLogger("datalab")
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # === CONSOLE HANDLER ===
    # This prints to terminal - for user-facing messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Only INFO and above to console

    # Simple format for console (no timestamps, cleaner output)
    console_format = logging.Formatter("[DataLab] %(message)s")
    console_handler.setFormatter(console_format)

    logger.addHandler(console_handler)

    # === FILE HANDLER ===
    # This writes to file - for debugging and audit trail
    try:
        # Create logs directory if needed
        log_dir = config.PROJECT_ROOT / "logs"
        log_dir.mkdir(exist_ok=True)

        # Create log file with date in filename
        log_filename = f"datalab_{datetime.now().strftime('%Y%m%d')}.log"
        log_file = log_dir / log_filename

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Everything to file

        # Detailed format for file (includes timestamps, level, line numbers)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)

        logger.addHandler(file_handler)
    except Exception as e:
        # If file logging fails, continue with console only
        logger.warning(f"Could not setup file logging: {e}")

    return logger


# Create module-level logger instance
_logger = _setup_logger()


# === PUBLIC API FUNCTIONS ===
# These provide a simple interface for other modules to use


def log(msg):
    """
    Log an info message (backward compatible with old utils.log).

    Args:
        msg: Message to log
    """
    _logger.info(msg)


def debug(msg):
    """
    Log a debug message (detailed info for developers).

    Args:
        msg: Debug message
    """
    _logger.debug(msg)


def info(msg):
    """
    Log an info message (normal operation).

    Args:
        msg: Info message
    """
    _logger.info(msg)


def warning(msg):
    """
    Log a warning message (something unexpected but not critical).

    Args:
        msg: Warning message
    """
    _logger.warning(msg)


def error(msg):
    """
    Log an error message (something failed).

    Args:
        msg: Error message
    """
    _logger.error(msg)


def critical(msg):
    """
    Log a critical message (severe error, possible shutdown).

    Args:
        msg: Critical error message
    """
    _logger.critical(msg)


# === DEMONSTRATION FUNCTION ===
def demo_logging_levels():
    """
    Demonstrate different log levels.

    Notice:
    - DEBUG won't appear in console (only in file)
    - INFO and above appear in both console and file
    """
    print("\n=== Logging Levels Demo ===\n")
    print("Note: DEBUG messages only go to log file, not console\n")

    debug("This is DEBUG - detailed developer info (file only)")
    info("This is INFO - normal operation message")
    warning("This is WARNING - something unusual happened")
    error("This is ERROR - something failed")
    critical("This is CRITICAL - severe problem!")

    print("\nCheck the logs/ directory for the complete log file with all levels.")


def main():
    """Test the logging module."""
    print("=" * 60)
    print("DataLab Logger Module")
    print("=" * 60)

    demo_logging_levels()

    print("\n" + "=" * 60)
    print("Log Levels Explained:")
    print("=" * 60)
    print("DEBUG    - Detailed information for diagnosing problems")
    print("INFO     - Confirmation that things work as expected")
    print("WARNING  - Something unexpected, but we continue")
    print("ERROR    - A serious problem, some function failed")
    print("CRITICAL - Very serious error, program may not continue")
    print("=" * 60)


if __name__ == "__main__":
    main()
