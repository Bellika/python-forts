"""
DataLab - Data Analysis Laboratory!
===================================

A teaching project demonstrating Python best practices and standard library usage.

Basic Usage:
    >>> from datalab import analyze_csv_data, analyze_json_data
    >>> results = analyze_csv_data()
    >>> print(results)

Modules:
    - config: Configuration and path management
    - utils: Utility package (logging, formatting)
        - utils.logger: Logging with standard library 'logging' module
        - utils.formatting: Number and text formatting utilities
    - io: I/O operations package
        - io.module_io: File I/O operations (JSON, CSV)
        - io.file_ops: File operations with os, shutil, pathlib
    - analysis: Analysis package
        - analysis.statistics: Statistical analysis with collections.Counter
        - analysis.processing: High-level data processing
    - output: Output package
        - output.reports: Report generation with datetime module
    - main: Application entry point

New in this version:
    - Refactored utils into a package with submodules
    - Added proper logging with logging module
    - Added report generation with datetime/time modules
    - Added file operations demonstrating os/shutil/pathlib
"""

# Package metadata
__version__ = "0.2.0"

from datalab import config
from datalab.analysis.processing import analyze_csv_data, analyze_json_data
from datalab.analysis.statistics import calculate_average, calculate_sum, count_by_field
from datalab.io.module_io import load_csv, load_json, save_csv, save_json
from datalab.output.reports import (
    create_analysis_report,
    generate_timestamp,
    save_report_to_file,
)

# Import key functions for easy access
# This allows users to do: from datalab import log, analyze_csv_data
# instead of: from datalab.utils import log; from datalab.processing import analyze_csv_data
from datalab.utils import log
from datalab.utils.formatting import format_currency, format_number, format_percentage

# Define what gets exported with "from datalab import *"
# (Though explicit imports are preferred!)
__all__ = [
    # Utils - Logging
    "log",
    # Utils - Formatting
    "format_number",
    "format_currency",
    "format_percentage",
    # Processing
    "analyze_json_data",
    "analyze_csv_data",
    # I/O
    "load_json",
    "save_json",
    "load_csv",
    "save_csv",
    # Statistics
    "calculate_average",
    "calculate_sum",
    "count_by_field",
    # Reports
    "create_analysis_report",
    "save_report_to_file",
    "generate_timestamp",
    # Config
    "config",
]
