"""
Main entry point for DataLab application.

Demonstrates:
- Composing functionality from multiple modules
- Creating a main application flow
- Clean separation between library code and application code
- Using new report and file operation features
"""

from datalab.utils import log, info, warning
from datalab.analysis.processing import analyze_json_data, analyze_csv_data
from datalab.output.reports import create_analysis_report, save_report_to_file, timed_operation
from datalab.io.file_ops import list_directory_contents


def run():
    """
    Main application function.

    This is the entry point that orchestrates the entire application.
    It can be called from:
    - CLI: datalab (after pip install)
    - Module: python -m datalab
    - Direct: python main.py (if __name__ == '__main__')

    Now includes:
    - Performance timing with time module
    - Report generation with datetime module
    - File operations with os/pathlib modules
    """
    log("Welcome to DataLab - Data Analysis Tool")
    info("Version 0.2.0 - Now with enhanced reporting!")
    print()

    # Show data directory contents (demonstrates file_ops)
    info("Scanning data directory...")
    contents = list_directory_contents()
    log(f"Found {len(contents['files'])} data files")
    print()

    # Analyze JSON data with timing
    log("=" * 60)
    json_results, json_time = timed_operation(analyze_json_data)
    json_report = create_analysis_report(json_results, "JSON Data Analysis")
    print(json_report)
    info(f"Analysis completed in {json_time:.3f} seconds")
    print()

    # Analyze CSV data with timing
    log("=" * 60)
    csv_results, csv_time = timed_operation(analyze_csv_data)
    csv_report = create_analysis_report(csv_results, "CSV Data Analysis")
    print(csv_report)
    info(f"Analysis completed in {csv_time:.3f} seconds")
    print()

    # Generate and save detailed report
    log("=" * 60)
    info("Generating detailed report...")

    # Create report for CSV data (more interesting than JSON)
    report_content = create_analysis_report(csv_results, "DataLab CSV Analysis Report")

    # Save report to file
    try:
        report_path = save_report_to_file(report_content)
        log(f"Detailed report available at: {report_path}")
    except Exception as e:
        warning(f"Could not save report: {e}")

    print()
    log("=" * 60)
    log("Analysis complete! Check reports/ directory for detailed output.")


if __name__ == '__main__':
    # This allows the module to be run directly for testing
    run()
