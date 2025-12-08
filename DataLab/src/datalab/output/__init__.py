"""
Output package for DataLab.

This package handles output generation including:
- Report generation and formatting (reports)

Demonstrates:
- Organizing output/presentation logic into packages
- Separation of business logic from output formatting
"""

from datalab.output.reports import (
    generate_timestamp,
    get_date_range,
    format_duration,
    create_analysis_report,
    save_report_to_file,
    timed_operation,
    create_performance_summary
)

__all__ = [
    'generate_timestamp',
    'get_date_range',
    'format_duration',
    'create_analysis_report',
    'save_report_to_file',
    'timed_operation',
    'create_performance_summary',
]
