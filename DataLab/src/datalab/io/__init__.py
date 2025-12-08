"""
I/O operations package for DataLab.

This package handles all file input/output operations including:
- JSON and CSV file handling (module_io)
- File system operations (file_ops)

Demonstrates:
- Organizing related functionality into packages
- Clean separation of I/O concerns
"""

from datalab.io.module_io import load_json, save_json, load_csv, save_csv
from datalab.io.file_ops import (
    list_directory_contents,
    copy_file,
    create_backup,
    get_file_info,
    find_files_by_pattern,
    get_directory_size,
    cleanup_old_backups,
    ensure_directory_exists
)

__all__ = [
    # JSON/CSV operations
    'load_json',
    'save_json',
    'load_csv',
    'save_csv',
    # File operations
    'list_directory_contents',
    'copy_file',
    'create_backup',
    'get_file_info',
    'find_files_by_pattern',
    'get_directory_size',
    'cleanup_old_backups',
    'ensure_directory_exists',
]
