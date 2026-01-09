"""
I/O operations package for DataLab.

This package handles all file input/output operations including:
- JSON and CSV file handling (module_io)
- File system operations (file_ops)

Demonstrates:
- Organizing related functionality into packages
- Clean separation of I/O concerns
"""

from datalab.io.file_ops import (
    cleanup_old_backups,
    copy_file,
    create_backup,
    ensure_directory_exists,
    find_files_by_pattern,
    get_directory_size,
    get_file_info,
    list_directory_contents,
)
from datalab.io.module_io import load_csv, load_json, save_csv, save_json

__all__ = [
    # JSON/CSV operations
    "load_json",
    "save_json",
    "load_csv",
    "save_csv",
    # File operations
    "list_directory_contents",
    "copy_file",
    "create_backup",
    "get_file_info",
    "find_files_by_pattern",
    "get_directory_size",
    "cleanup_old_backups",
    "ensure_directory_exists",
]
