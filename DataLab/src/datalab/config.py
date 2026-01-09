"""
Configuration module for DataLab.

This module centralizes all configuration, paths, and constants.
Demonstrates proper path handling using __file__ and pathlib.
"""

from pathlib import Path

# === PATH CONFIGURATION ===
# Using __file__ makes paths work regardless of where the script is run from
PACKAGE_DIR = Path(__file__).parent  # Directory where this file lives
PROJECT_ROOT = PACKAGE_DIR.parent.parent  # DataLab root
DATA_DIR = PROJECT_ROOT / "data"  # Data directory in project root

# === FILE DEFAULTS ===
DEFAULT_JSON_FILE = "data.json"
DEFAULT_CSV_FILE = "people.csv"

# === APPLICATION SETTINGS ===
LOG_PREFIX = "[DataLab]"
DECIMAL_PLACES = 2


def get_data_path(filename):
    """
    Get full path to a data file.

    This ensures we always reference data files correctly,
    regardless of the current working directory.

    Args:
        filename: Name of file in data directory

    Returns:
        Path object to the file
    """
    return DATA_DIR / filename


def main():
    """Display current configuration (useful for debugging)."""
    print("=" * 60)
    print("DataLab Configuration")
    print("=" * 60)
    print(f"Package directory:  {PACKAGE_DIR}")
    print(f"Project root:       {PROJECT_ROOT}")
    print(f"Data directory:     {DATA_DIR}")
    print(f"\nDefault files:")
    print(f"  JSON: {get_data_path(DEFAULT_JSON_FILE)}")
    print(f"  CSV:  {get_data_path(DEFAULT_CSV_FILE)}")
    print(f"\nSettings:")
    print(f"  Log prefix:       {LOG_PREFIX}")
    print(f"  Decimal places:   {DECIMAL_PLACES}")
    print("=" * 60)


if __name__ == "__main__":
    main()
