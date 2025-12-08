"""
Report generation module for DataLab.

Demonstrates:
- datetime module for timestamps and dates
- time module for performance measurement
- String formatting and templates
- File writing with timestamps
- Creating structured reports
"""

import datetime
import time
from pathlib import Path
from datalab import config
from datalab.utils import log
from datalab.utils.formatting import format_number, format_currency, format_percentage


def generate_timestamp(format_str='%Y-%m-%d %H:%M:%S'):
    """
    Generate a formatted timestamp.

    Demonstrates:
    - datetime.datetime.now() to get current time
    - strftime() for custom formatting

    Args:
        format_str: Format string (default: YYYY-MM-DD HH:MM:SS)

    Returns:
        Formatted timestamp string

    Example:
        >>> generate_timestamp('%Y%m%d_%H%M%S')
        '20241207_143022'
    """
    return datetime.datetime.now().strftime(format_str)


def get_date_range(days_back=7):
    """
    Get a date range from N days ago until today.

    Demonstrates:
    - datetime.date.today() for current date
    - datetime.timedelta for date arithmetic

    Args:
        days_back: Number of days to go back

    Returns:
        Tuple of (start_date, end_date)

    Example:
        >>> start, end = get_date_range(7)
        >>> print(f"Last week: {start} to {end}")
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_back)
    return start_date, end_date


def format_duration(seconds):
    """
    Format a duration in seconds to human-readable string.

    Demonstrates:
    - Conditional logic for formatting
    - Number formatting

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "2.5s", "1m 30s", "1h 5m")
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def create_analysis_report(analysis_data, report_name="DataLab Analysis Report"):
    """
    Create a formatted text report from analysis data.

    Demonstrates:
    - String building with multiple lines
    - Combining different formatting functions
    - Working with dictionaries

    Args:
        analysis_data: Dictionary with analysis results
        report_name: Name of the report

    Returns:
        Formatted report as string
    """
    lines = []
    lines.append("=" * 70)
    lines.append(f" {report_name}")
    lines.append("=" * 70)
    lines.append(f"Generated: {generate_timestamp()}")
    lines.append("")

    # File info
    if 'file' in analysis_data:
        lines.append(f"Data Source: {analysis_data['file']}")

    if 'records' in analysis_data:
        lines.append(f"Total Records: {analysis_data['records']}")

    lines.append("")
    lines.append("-" * 70)
    lines.append(" Statistical Summary")
    lines.append("-" * 70)

    # Age statistics
    if 'average_age' in analysis_data:
        lines.append(f"Average Age: {format_number(analysis_data['average_age'], 1)} years")

    # Salary statistics
    if 'average_salary' in analysis_data:
        lines.append(f"Average Salary: {format_currency(analysis_data['average_salary'], 'SEK', 0)}")

    if 'salary_range' in analysis_data:
        min_sal, max_sal = analysis_data['salary_range']
        lines.append(f"Salary Range: {format_currency(min_sal, 'SEK', 0)} - {format_currency(max_sal, 'SEK', 0)}")

    # City distribution
    if 'city_distribution' in analysis_data:
        lines.append("")
        lines.append("-" * 70)
        lines.append(" City Distribution")
        lines.append("-" * 70)

        total = analysis_data['records']
        for city, count in sorted(analysis_data['city_distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = format_percentage(count, total)
            lines.append(f"  {city:.<20} {count:>5} ({percentage:>6})")

    lines.append("=" * 70)

    return "\n".join(lines)


def save_report_to_file(report_content, filename=None, reports_dir=None):
    """
    Save a report to a file with timestamp in filename.

    Demonstrates:
    - pathlib for directory creation
    - File writing
    - Dynamic filename generation with timestamps

    Args:
        report_content: Report text to save
        filename: Custom filename (generates timestamped name if None)
        reports_dir: Directory for reports (uses PROJECT_ROOT/reports if None)

    Returns:
        Path to saved report file
    """
    # Setup reports directory
    if reports_dir is None:
        reports_dir = config.PROJECT_ROOT / 'reports'
    else:
        reports_dir = Path(reports_dir)

    # Create directory if it doesn't exist
    reports_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp if not provided
    if filename is None:
        timestamp = generate_timestamp('%Y%m%d_%H%M%S')
        filename = f"report_{timestamp}.txt"

    filepath = reports_dir / filename

    # Write report to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)

    log(f"Report saved to: {filepath}")
    return filepath


def timed_operation(func, *args, **kwargs):
    """
    Execute a function and measure its execution time.

    Demonstrates:
    - time.time() for performance measurement
    - Function execution with *args, **kwargs
    - Returning multiple values

    Args:
        func: Function to execute
        *args, **kwargs: Arguments for the function

    Returns:
        Tuple of (result, duration_seconds)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start_time
    return result, duration


def create_performance_summary(operations):
    """
    Create a summary of operation performance metrics.

    Args:
        operations: List of tuples (operation_name, duration_seconds)

    Returns:
        Formatted performance report string
    """
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append(" Performance Summary")
    lines.append("=" * 70)

    total_time = sum(duration for _, duration in operations)

    for operation, duration in operations:
        percentage = format_percentage(duration, total_time)
        lines.append(f"  {operation:.<40} {format_duration(duration):>10} ({percentage:>6})")

    lines.append("-" * 70)
    lines.append(f"  {'Total Time':.<40} {format_duration(total_time):>10}")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Test the reports module."""
    print("=" * 60)
    print("DataLab Reports Module")
    print("=" * 60)

    print("\n=== Timestamp Generation ===")
    print(f"Default format: {generate_timestamp()}")
    print(f"Date only: {generate_timestamp('%Y-%m-%d')}")
    print(f"Time only: {generate_timestamp('%H:%M:%S')}")
    print(f"Filename format: {generate_timestamp('%Y%m%d_%H%M%S')}")

    print("\n=== Date Range ===")
    start, end = get_date_range(7)
    print(f"Last 7 days: {start} to {end}")
    start, end = get_date_range(30)
    print(f"Last 30 days: {start} to {end}")

    print("\n=== Duration Formatting ===")
    print(f"1.5 seconds: {format_duration(1.5)}")
    print(f"90 seconds: {format_duration(90)}")
    print(f"3661 seconds: {format_duration(3661)}")

    print("\n=== Sample Report ===")
    sample_data = {
        'file': 'people.csv',
        'records': 7,
        'average_age': 27.86,
        'average_salary': 47714.29,
        'salary_range': (38000, 55000),
        'city_distribution': {
            'Stockholm': 3,
            'Gothenburg': 2,
            'Malmö': 1,
            'Uppsala': 1
        }
    }

    report = create_analysis_report(sample_data)
    print(report)

    print("\n=== Performance Measurement ===")
    operations = [
        ("Load CSV data", 0.012),
        ("Calculate statistics", 0.008),
        ("Generate report", 0.003),
    ]
    perf_summary = create_performance_summary(operations)
    print(perf_summary)


if __name__ == '__main__':
    main()
