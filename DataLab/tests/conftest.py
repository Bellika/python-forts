"""
Pytest configuration and shared fixtures.

conftest.py is a special file that pytest automatically loads.
Fixtures defined here are available to all test files without import.

Demonstrates:
- Shared fixtures across test files
- Pytest configuration
- Custom markers
"""

import pytest
import tempfile
import json
from pathlib import Path


def pytest_configure(config):
    """
    Configure custom markers.

    This allows us to use markers like @pytest.mark.slow
    without warnings from pytest.
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


@pytest.fixture
def temp_dir():
    """
    Fixture providing a temporary directory.

    Demonstrates:
    - Context manager fixtures
    - Automatic cleanup with yield
    - Working with temporary files in tests
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
    # Cleanup happens automatically when context exits


@pytest.fixture
def sample_json_file(temp_dir):
    """
    Fixture creating a temporary JSON file with test data.

    Useful for testing file I/O functions.
    """
    data = [
        {"id": 1, "name": "Alice", "score": 85},
        {"id": 2, "name": "Bob", "score": 92},
        {"id": 3, "name": "Charlie", "score": 78},
    ]

    file_path = temp_dir / "test_data.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return file_path


@pytest.fixture
def sample_csv_file(temp_dir):
    """
    Fixture creating a temporary CSV file with test data.

    Demonstrates creating CSV files for testing.
    """
    import csv

    data = [
        {"name": "Alice", "age": "30", "city": "Stockholm"},
        {"name": "Bob", "age": "25", "city": "Göteborg"},
    ]

    file_path = temp_dir / "test_data.csv"
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerows(data)

    return file_path


@pytest.fixture(scope="session")
def mock_config():
    """
    Session-scoped fixture for mock configuration.

    Scope="session" means this is created once per test session,
    not once per test. Useful for expensive setup.
    """
    return {
        "app_name": "DataLab Test",
        "version": "0.0.1",
        "debug": True,
    }
