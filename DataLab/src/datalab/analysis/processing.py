"""
Data processing functions for DataLab.

Demonstrates:
- Absolute imports from multiple modules
- Using centralized config
- Composing functions from other modules
- Working with different data formats
"""

from datalab import config
from datalab.analysis.statistics import calculate_average, count_by_field, get_min_max
from datalab.io.module_io import load_csv, load_json
from datalab.utils import log
from datalab.utils.formatting import format_number


def analyze_json_data(filename=None):
    """
    Load and analyze JSON data.

    Args:
        filename: JSON filename (uses default if None)

    Returns:
        Dictionary with analysis results
    """
    if filename is None:
        filename = config.DEFAULT_JSON_FILE

    filepath = config.get_data_path(filename)
    data = load_json(filepath)

    avg_age = calculate_average(data, "age")

    return {
        "file": filename,
        "records": len(data),
        "average_age": avg_age,
    }


def analyze_csv_data(filename=None):
    """
    Load and analyze CSV data.

    Demonstrates working with CSV files and performing
    multiple statistical analyses.

    Args:
        filename: CSV filename (uses default if None)

    Returns:
        Dictionary with analysis results
    """
    if filename is None:
        filename = config.DEFAULT_CSV_FILE

    filepath = config.get_data_path(filename)
    data = load_csv(filepath)

    # Perform various analyses
    avg_age = calculate_average(data, "age")
    avg_salary = calculate_average(data, "salary")
    city_distribution = count_by_field(data, "city")
    min_salary, max_salary = get_min_max(data, "salary")

    return {
        "file": filename,
        "records": len(data),
        "average_age": avg_age,
        "average_salary": avg_salary,
        "city_distribution": city_distribution,
        "salary_range": (min_salary, max_salary),
    }
