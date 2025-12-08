"""
Utils package for DataLab.

This package demonstrates organizing related functionality into submodules.
Instead of one large utils.py, we split into:
- logger.py: Logging functionality using standard library 'logging'
- formatting.py: Number and text formatting utilities
"""

# Import from submodules to maintain backward compatibility
from datalab.utils.logger import log, debug, info, warning, error
from datalab.utils.formatting import format_number, format_currency, format_percentage

# Export public API
__all__ = [
    # Logging
    'log',
    'debug',
    'info',
    'warning',
    'error',
    # Formatting
    'format_number',
    'format_currency',
    'format_percentage',
]
