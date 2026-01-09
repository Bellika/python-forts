"""
Utils package for DataLab.

This package demonstrates organizing related functionality into submodules.
Instead of one large utils.py, we split into:
- logger.py: Logging functionality using standard library 'logging'
- formatting.py: Number and text formatting utilities
"""

from datalab.utils.formatting import format_currency, format_number, format_percentage

# Import from submodules to maintain backward compatibility
from datalab.utils.logger import debug, error, info, log, warning

# Export public API
__all__ = [
    # Logging
    "log",
    "debug",
    "info",
    "warning",
    "error",
    # Formatting
    "format_number",
    "format_currency",
    "format_percentage",
]
