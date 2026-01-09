"""
Test suite for DataLab statistics functions.

Demonstrates:
- Pytest basic testing
- Fixtures for mock data
- Parametrized tests
- Exception testing
- Setup and teardown with decorators
"""

import pytest
from datalab.analysis.statistics import (
    calculate_average,
    calculate_sum,
    count_by_field,
    get_min_max
)


# ============================================================================
# FIXTURES - Reusable test data
# ============================================================================

@pytest.fixture
def sample_data():
    """
    Fixture providing standard test data.

    Fixtures run automatically when used as test parameters.
    This is a fundamental pytest concept.
    """
    return [
        {"name": "Alice", "age": 30, "city": "Stockholm", "salary": 45000},
        {"name": "Bob", "age": 25, "city": "Göteborg", "salary": 38000},
        {"name": "Charlie", "age": 35, "city": "Stockholm", "salary": 52000},
        {"name": "Diana", "age": 28, "city": "Malmö", "salary": 41000},
    ]


@pytest.fixture
def empty_data():
    """Fixture for empty data - useful for edge case testing."""
    return []


@pytest.fixture
def data_with_missing_fields():
    """Fixture with incomplete data for testing error handling."""
    return [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "city": "Stockholm"}, 
    ]


# ============================================================================
# BASIC TESTS - Fundamental testing
# ============================================================================

def test_calculate_average_basic(sample_data):
    """
    Test basic average calculation.

    Demonstrates:
    - Using fixtures
    - Simple assertions
    """
    result = calculate_average(sample_data, 'age')
    expected = (30 + 25 + 35 + 28) / 4
    assert result == expected, "Average age should be correct"


def test_calculate_average_salary(sample_data):
    """Test that average works for different fields."""
    result = calculate_average(sample_data, 'salary')
    expected = (45000 + 38000 + 52000 + 41000) / 4
    assert result == expected


def test_calculate_sum_basic(sample_data):
    """Test summation of fields."""
    result = calculate_sum(sample_data, 'salary')
    expected = 45000 + 38000 + 52000 + 41000
    assert result == expected


# ============================================================================
# PARAMETRIZED TESTS - Tests with multiple data points
# ============================================================================

@pytest.mark.parametrize("field,expected", [
    ("age", 29.5),  # (30 + 25 + 35 + 28) / 4
    ("salary", 44000),  # (45000 + 38000 + 52000 + 41000) / 4
])
def test_calculate_average_parametrized(sample_data, field, expected):
    """
    Parametrized test - runs same test with different inputs.

    Demonstrates:
    - @pytest.mark.parametrize decorator
    - Efficient way to test multiple scenarios
    """
    result = calculate_average(sample_data, field)
    assert result == expected


@pytest.mark.parametrize("data,field,expected", [
    ([{"x": 10}, {"x": 20}], "x", 15.0),
    ([{"y": 5}, {"y": 15}, {"y": 10}], "y", 10.0),
    ([{"z": 100}], "z", 100.0),
])
def test_calculate_average_various_datasets(data, field, expected):
    """Parametrized test with completely different datasets."""
    result = calculate_average(data, field)
    assert result == expected


# ============================================================================
# EXCEPTION TESTING - Test that errors are raised correctly
# ============================================================================

def test_calculate_average_empty_data_raises_error(empty_data):
    """
    Test that function raises correct exception for empty data.

    Demonstrates:
    - pytest.raises context manager
    - Testing exceptions is important for robust code
    """
    with pytest.raises(ValueError, match="Cannot calculate average of empty dataset"):
        calculate_average(empty_data, 'age')


def test_calculate_average_missing_field_raises_error(sample_data):
    """Test that invalid field name raises ValueError."""
    with pytest.raises(ValueError, match="Field 'nonexistent' not found"):
        calculate_average(sample_data, 'nonexistent')


def test_calculate_average_non_numeric_raises_error():
    """Test that non-numeric values raise ValueError."""
    data = [{"name": "Alice", "age": "thirty"}]  # String instead of number
    with pytest.raises(ValueError, match="contains non-numeric data"):
        calculate_average(data, 'age')


def test_get_min_max_empty_raises_error(empty_data):
    """Test that get_min_max raises error for empty data."""
    with pytest.raises(ValueError, match="Cannot find min/max of empty dataset"):
        get_min_max(empty_data, 'age')


# ============================================================================
# TESTS WITH MARKS/DECORATORS
# ============================================================================

@pytest.mark.slow
def test_large_dataset_performance():
    """
    Test marked as 'slow' - can be skipped with pytest -m "not slow".

    Demonstrates:
    - Custom markers
    - Performance testing
    """
    # Create large dataset
    large_data = [{"value": i} for i in range(10000)]
    result = calculate_average(large_data, 'value')
    assert result == 4999.5  # Average of 0 to 9999


@pytest.mark.skip(reason="Example of skipping a test")
def test_future_feature():
    """This test is not run - useful for TDD or features under development."""
    assert False, "This test is not implemented yet"


@pytest.mark.xfail(reason="Known bug - will fix in next sprint")
def test_known_bug():
    """Test expected to fail - useful for documenting known bugs."""
    # This represents a known bug
    data = [{"x": None}]
    result = calculate_average(data, 'x')
    assert result == 0  # Expected behavior when bug is fixed


# ============================================================================
# EDGE CASES AND ROBUSTNESS
# ============================================================================

def test_count_by_field_basic(sample_data):
    """Test counting field values."""
    result = count_by_field(sample_data, 'city')
    expected = {"Stockholm": 2, "Göteborg": 1, "Malmö": 1}
    assert result == expected


def test_count_by_field_all_same():
    """Test when all values are the same."""
    data = [{"city": "Stockholm"} for _ in range(5)]
    result = count_by_field(data, 'city')
    assert result == {"Stockholm": 5}


def test_get_min_max_single_value():
    """Test min/max with only one value."""
    data = [{"x": 42}]
    min_val, max_val = get_min_max(data, 'x')
    assert min_val == 42
    assert max_val == 42


def test_get_min_max_negative_values():
    """Test min/max with negative values."""
    data = [{"temp": -5}, {"temp": -10}, {"temp": 3}]
    min_val, max_val = get_min_max(data, 'temp')
    assert min_val == -10
    assert max_val == 3


def test_calculate_sum_empty_returns_zero(empty_data):
    """Test that sum of empty data is 0."""
    result = calculate_sum(empty_data, 'value')
    assert result == 0.0


# ============================================================================
# INTEGRATION-LIKE TESTS
# ============================================================================

def test_statistics_workflow(sample_data):
    """
    Test combining multiple functions - more integration-like.

    Demonstrates:
    - Testing functions together
    - Verifying related calculations
    """
    # Calculate different statistics
    avg_salary = calculate_average(sample_data, 'salary')
    sum_salary = calculate_sum(sample_data, 'salary')
    min_salary, max_salary = get_min_max(sample_data, 'salary')

    # Verify relationships between statistics
    assert sum_salary == avg_salary * len(sample_data)
    assert min_salary <= avg_salary <= max_salary
    assert min_salary == 38000
    assert max_salary == 52000


# ============================================================================
# TESTS WITH SETUP AND TEARDOWN
# ============================================================================

class TestWithSetup:
    """
    Test class demonstrating setup/teardown.

    Useful when multiple tests share the same preparations.
    """

    def setup_method(self):
        """Runs before each test method in the class."""
        self.test_data = [
            {"value": 10},
            {"value": 20},
            {"value": 30},
        ]

    def teardown_method(self):
        """Runs after each test method in the class."""
        # In real tests: close files, clean databases, etc.
        self.test_data = None

    def test_with_setup_data(self):
        """Test using data from setup_method."""
        result = calculate_average(self.test_data, 'value')
        assert result == 20

    def test_another_with_setup_data(self):
        """Another test with same setup."""
        result = calculate_sum(self.test_data, 'value')
        assert result == 60
