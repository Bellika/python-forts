"""
File operations module for DataLab.

Demonstrates:
- os module for operating system interactions
- shutil module for high-level file operations
- pathlib module (modern path handling - already used in config)
- glob module for pattern matching
- File and directory management
"""

import os
import shutil
import glob
from pathlib import Path
from datalab import config
from datalab.utils import log


def list_directory_contents(directory=None):
    """
    List contents of a directory.

    Demonstrates:
    - os.listdir() to list files
    - os.path operations
    - Distinguishing files from directories

    Args:
        directory: Directory path (uses data dir if None)

    Returns:
        Dictionary with 'files' and 'directories' lists
    """
    if directory is None:
        directory = config.DATA_DIR

    directory = Path(directory)

    if not directory.exists():
        log(f"Directory does not exist: {directory}")
        return {'files': [], 'directories': []}

    files = []
    directories = []

    # Using os.listdir
    for item in os.listdir(directory):
        full_path = directory / item
        if full_path.is_file():
            files.append(item)
        elif full_path.is_dir():
            directories.append(item)

    return {
        'files': sorted(files),
        'directories': sorted(directories)
    }


def get_file_info(filepath):
    """
    Get detailed information about a file.

    Demonstrates:
    - os.path.getsize() for file size
    - os.path.getmtime() for modification time
    - os.path.exists() for checking existence
    - Converting timestamps to readable dates

    Args:
        filepath: Path to file

    Returns:
        Dictionary with file information
    """
    import datetime

    filepath = Path(filepath)

    if not filepath.exists():
        return {'exists': False}

    # Get file stats
    stat_info = filepath.stat()

    return {
        'exists': True,
        'name': filepath.name,
        'size_bytes': stat_info.st_size,
        'size_kb': stat_info.st_size / 1024,
        'modified': datetime.datetime.fromtimestamp(stat_info.st_mtime),
        'is_file': filepath.is_file(),
        'is_directory': filepath.is_dir(),
        'extension': filepath.suffix,
    }


def find_files_by_pattern(pattern, directory=None):
    """
    Find files matching a glob pattern.

    Demonstrates:
    - glob module for pattern matching
    - Working with wildcards (*, **, ?)

    Args:
        pattern: Glob pattern (e.g., '*.json', '**/*.csv')
        directory: Directory to search (uses data dir if None)

    Returns:
        List of matching file paths

    Examples:
        find_files_by_pattern('*.json')  # All JSON files
        find_files_by_pattern('**/*.csv')  # CSV files in all subdirectories
    """
    if directory is None:
        directory = config.DATA_DIR

    directory = Path(directory)
    matches = list(directory.glob(pattern))

    # Return only files, not directories
    return [str(f) for f in matches if f.is_file()]


def copy_file(source, destination, create_backup=True):
    """
    Copy a file to a new location.

    Demonstrates:
    - shutil.copy2() for copying files with metadata
    - Creating backup copies
    - Path handling

    Args:
        source: Source file path
        destination: Destination file path
        create_backup: If True and destination exists, create backup first

    Returns:
        Path to copied file
    """
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    # Create backup if destination exists
    if destination.exists() and create_backup:
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = destination.parent / f"{destination.stem}_backup_{timestamp}{destination.suffix}"
        shutil.copy2(destination, backup_path)
        log(f"Created backup: {backup_path}")

    # Copy file with metadata (timestamps, permissions)
    shutil.copy2(source, destination)
    log(f"Copied {source.name} to {destination}")

    return destination


def create_backup(file_path, backup_dir=None):
    """
    Create a timestamped backup of a file.

    Demonstrates:
    - Creating backup copies with timestamps
    - Directory creation
    - File copying

    Args:
        file_path: File to backup
        backup_dir: Backup directory (uses PROJECT_ROOT/backups if None)

    Returns:
        Path to backup file
    """
    import datetime

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Setup backup directory
    if backup_dir is None:
        backup_dir = config.PROJECT_ROOT / 'backups'
    else:
        backup_dir = Path(backup_dir)

    backup_dir.mkdir(exist_ok=True)

    # Create backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    backup_path = backup_dir / backup_name

    # Copy file
    shutil.copy2(file_path, backup_path)
    log(f"Backup created: {backup_path}")

    return backup_path


def get_directory_size(directory):
    """
    Calculate total size of a directory.

    Demonstrates:
    - os.walk() for traversing directory tree
    - Calculating cumulative file sizes
    - Working with nested directories

    Args:
        directory: Directory path

    Returns:
        Total size in bytes
    """
    directory = Path(directory)
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = Path(dirpath) / filename
            try:
                total_size += filepath.stat().st_size
            except (OSError, FileNotFoundError):
                # Skip files we can't access
                pass

    return total_size


def cleanup_old_backups(backup_dir, keep_count=5):
    """
    Remove old backup files, keeping only the N most recent.

    Demonstrates:
    - Listing files by modification time
    - Deleting files
    - os.path operations

    Args:
        backup_dir: Directory containing backups
        keep_count: Number of recent backups to keep

    Returns:
        List of deleted file paths
    """
    backup_dir = Path(backup_dir)

    if not backup_dir.exists():
        return []

    # Get all backup files sorted by modification time (newest first)
    backup_files = []
    for file in backup_dir.glob('*_backup_*'):
        if file.is_file():
            backup_files.append((file, file.stat().st_mtime))

    backup_files.sort(key=lambda x: x[1], reverse=True)

    # Delete old backups (keep only keep_count newest)
    deleted = []
    for file, _ in backup_files[keep_count:]:
        file.unlink()
        deleted.append(str(file))
        log(f"Deleted old backup: {file.name}")

    return deleted


def ensure_directory_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.

    Demonstrates:
    - Path.mkdir() with exist_ok parameter
    - parents=True for creating parent directories

    Args:
        directory: Directory path to ensure exists

    Returns:
        Path object to directory
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def main():
    """Test the file operations module."""
    print("=" * 60)
    print("DataLab File Operations Module")
    print("=" * 60)

    print("\n=== Directory Listing ===")
    contents = list_directory_contents()
    print(f"Files: {contents['files']}")
    print(f"Directories: {contents['directories']}")

    print("\n=== File Information ===")
    if contents['files']:
        first_file = config.DATA_DIR / contents['files'][0]
        info = get_file_info(first_file)
        print(f"File: {info['name']}")
        print(f"Size: {info['size_kb']:.2f} KB")
        print(f"Modified: {info['modified']}")
        print(f"Extension: {info['extension']}")

    print("\n=== Find Files by Pattern ===")
    json_files = find_files_by_pattern('*.json')
    print(f"JSON files: {[Path(f).name for f in json_files]}")

    csv_files = find_files_by_pattern('*.csv')
    print(f"CSV files: {[Path(f).name for f in csv_files]}")

    print("\n=== Directory Size ===")
    data_size = get_directory_size(config.DATA_DIR)
    print(f"Data directory size: {data_size / 1024:.2f} KB")

    print("\n=== Environment Info (os module) ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Platform: {os.name}")

    if os.name == 'posix':  # Linux/Mac
        print(f"User: {os.environ.get('USER', 'unknown')}")
        print(f"Home: {os.environ.get('HOME', 'unknown')}")
    elif os.name == 'nt':  # Windows
        print(f"User: {os.environ.get('USERNAME', 'unknown')}")
        print(f"Home: {os.environ.get('USERPROFILE', 'unknown')}")

    print("\n" + "=" * 60)
    print("Note: File copy and backup operations not run in demo")
    print("to avoid modifying the file system.")
    print("=" * 60)


if __name__ == '__main__':
    main()
