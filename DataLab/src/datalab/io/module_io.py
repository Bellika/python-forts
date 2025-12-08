"""
File I/O operations for DataLab.

Demonstrates:
- Absolute imports (from datalab.config)
- Working with both JSON and CSV files
- Using config for paths
- Module testing
"""

import json
import csv
from datalab import config


def load_json(filepath):
    """
    Load data from a JSON file.

    Args:
        filepath: Path to JSON file (str or Path)

    Returns:
        Parsed JSON data (usually dict or list)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, filepath):
    """
    Save data to a JSON file with pretty formatting.

    Args:
        data: Data to save (must be JSON-serializable)
        filepath: Path to output file (str or Path)
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_csv(filepath):
    """
    Load data from a CSV file.

    Returns data as a list of dictionaries, where each dict
    represents a row with column names as keys.

    Args:
        filepath: Path to CSV file (str or Path)

    Returns:
        List of dictionaries
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(data, filepath, fieldnames=None):
    """
    Save data to a CSV file.

    Args:
        data: List of dictionaries to save
        filepath: Path to output file (str or Path)
        fieldnames: List of column names (inferred from data if None)
    """
    if not data:
        raise ValueError("Cannot save empty data to CSV")

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
