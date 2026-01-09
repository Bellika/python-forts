"""
Test suite for DataLab I/O functions.

Demonstrates:
- Testing file operations with temporary files
- Using fixtures from conftest.py
- Mocking file system operations
- Testing error handling for file operations
"""

import pytest
import json
from pathlib import Path
from datalab.io.module_io import load_json, save_json, load_csv, save_csv


# ============================================================================
# JSON TESTS
# ============================================================================

def test_load_json_success(sample_json_file):
    """
    Test loading a JSON file.

    Demonstrates:
    - Using fixture from conftest.py (sample_json_file)
    - Testing file reading operations
    """
    data = load_json(sample_json_file)

    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["name"] == "Alice"
    assert data[1]["score"] == 92


def test_save_and_load_json_roundtrip(temp_dir):
    """
    Test saving and loading JSON (roundtrip test).

    Demonstrates:
    - Testing write and read together
    - Verifying data integrity
    """
    original_data = {
        "users": ["Alice", "Bob"],
        "count": 2,
        "active": True
    }

    file_path = temp_dir / "output.json"

    # Save data
    save_json(original_data, file_path)

    # Verify file exists
    assert file_path.exists()

    # Load it back
    loaded_data = load_json(file_path)

    # Verify data matches
    assert loaded_data == original_data


def test_load_json_file_not_found():
    """
    Test that loading non-existent file raises FileNotFoundError.

    Demonstrates:
    - Testing error conditions
    - Expecting specific exceptions
    """
    with pytest.raises(FileNotFoundError):
        load_json("nonexistent_file.json")


def test_save_json_creates_file(temp_dir):
    """Test that save_json creates a new file."""
    data = {"test": "value"}
    file_path = temp_dir / "new_file.json"

    assert not file_path.exists()

    save_json(data, file_path)

    assert file_path.exists()


def test_save_json_pretty_formatting(temp_dir):
    """
    Test that saved JSON is properly formatted.

    Demonstrates:
    - Testing implementation details when they matter
    - Reading raw file content
    """
    data = {"key": "value", "number": 42}
    file_path = temp_dir / "formatted.json"

    save_json(data, file_path)

    # Read raw content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Should be indented (pretty-printed)
    assert "    " in content  # Check for indentation
    assert "\n" in content  # Check for newlines


# ============================================================================
# CSV TESTS
# ============================================================================

def test_load_csv_success(sample_csv_file):
    """
    Test loading a CSV file.

    Demonstrates:
    - CSV loading returns list of dictionaries
    - Each row becomes a dict with column names as keys
    """
    data = load_csv(sample_csv_file)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[0]["age"] == "30"  # CSV values are strings
    assert data[1]["city"] == "Göteborg"


def test_save_and_load_csv_roundtrip(temp_dir):
    """Test saving and loading CSV (roundtrip test)."""
    original_data = [
        {"name": "Alice", "age": "30", "city": "Stockholm"},
        {"name": "Bob", "age": "25", "city": "Malmö"},
    ]

    file_path = temp_dir / "output.csv"

    # Save data
    save_csv(original_data, file_path)

    # Verify file exists
    assert file_path.exists()

    # Load it back
    loaded_data = load_csv(file_path)

    # Verify data matches
    assert loaded_data == original_data


def test_save_csv_with_custom_fieldnames(temp_dir):
    """
    Test saving CSV with specific field order.

    Demonstrates:
    - Controlling CSV column order
    - Using optional parameters
    """
    data = [
        {"name": "Alice", "age": "30", "city": "Stockholm"},
        {"name": "Bob", "age": "25", "city": "Malmö"},
    ]

    file_path = temp_dir / "ordered.csv"

    # Save with specific field order
    save_csv(data, file_path, fieldnames=["age", "name", "city"])

    # Read back and verify column order
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        assert first_line == "age,name,city"


def test_save_csv_empty_data_raises_error(temp_dir):
    """
    Test that saving empty data raises ValueError.

    Demonstrates:
    - Testing precondition validation
    - Proper error handling
    """
    file_path = temp_dir / "empty.csv"

    with pytest.raises(ValueError, match="Cannot save empty data"):
        save_csv([], file_path)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

def test_load_json_invalid_json(temp_dir):
    """Test that loading invalid JSON raises appropriate error."""
    file_path = temp_dir / "invalid.json"

    # Create file with invalid JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{ invalid json }")

    with pytest.raises(json.JSONDecodeError):
        load_json(file_path)


def test_save_json_unicode_handling(temp_dir):
    """
    Test that Unicode characters are handled correctly.

    Demonstrates:
    - Testing internationalization concerns
    - Ensuring proper encoding
    """
    data = {
        "swedish": "Hej världen! åäö ÅÄÖ",
        "emoji": "🎉 🚀",
        "chinese": "你好"
    }

    file_path = temp_dir / "unicode.json"
    save_json(data, file_path)

    loaded_data = load_json(file_path)

    assert loaded_data == data
    assert loaded_data["swedish"] == "Hej världen! åäö ÅÄÖ"


@pytest.mark.parametrize("extension", [".json", ".txt", ""])
def test_save_json_different_extensions(temp_dir, extension):
    """
    Test that save_json works with different file extensions.

    Demonstrates:
    - Parametrized testing with file extensions
    - Flexibility testing
    """
    data = {"test": "value"}
    file_path = temp_dir / f"test{extension}"

    save_json(data, file_path)

    assert file_path.exists()
    loaded_data = load_json(file_path)
    assert loaded_data == data


# ============================================================================
# INTEGRATION WITH PATHLIB
# ============================================================================

def test_load_json_accepts_string_path(temp_dir):
    """
    Test that functions accept both Path objects and strings.

    Demonstrates:
    - API flexibility
    - Path/string interoperability
    """
    data = {"test": "value"}
    file_path = temp_dir / "test.json"

    save_json(data, file_path)

    # Load with string path
    loaded_data = load_json(str(file_path))

    assert loaded_data == data


def test_csv_with_missing_optional_fields(temp_dir):
    """
    Test CSV handling when some rows have missing fields.

    Demonstrates:
    - Handling incomplete data gracefully
    - Real-world data scenarios
    """
    # Create CSV with missing values
    import csv
    file_path = temp_dir / "sparse.csv"

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerow({"name": "Alice", "age": "30", "city": "Stockholm"})
        writer.writerow({"name": "Bob", "age": "25"})  # Missing city

    data = load_csv(file_path)

    assert len(data) == 2
    assert data[1]["city"] == ""  # DictReader uses empty string for missing values
