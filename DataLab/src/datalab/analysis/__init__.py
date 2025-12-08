"""
Analysis package for DataLab.

This package handles data analysis and statistics including:
- Data processing and analysis (processing)
- Statistical calculations (statistics)

Demonstrates:
- Organizing analytical functions into packages
- Separation of data transformation and calculation logic
"""

from datalab.analysis.processing import analyze_json_data, analyze_csv_data
from datalab.analysis.statistics import (
    calculate_average,
    calculate_sum,
    count_by_field,
    get_min_max
)

__all__ = [
    # Processing functions
    'analyze_json_data',
    'analyze_csv_data',
    # Statistical functions
    'calculate_average',
    'calculate_sum',
    'count_by_field',
    'get_min_max',
]
