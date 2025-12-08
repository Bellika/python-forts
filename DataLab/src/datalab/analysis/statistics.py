"""
Statistical analysis functions for DataLab.

Demonstrates:
- Working with list of dictionaries (common Python data structure)
- Type conversion and data validation
- Reusable statistical functions
- Using collections.Counter from standard library
"""

from collections import Counter


def calculate_average(data, field):
    """
    Calculate the average of a numeric field in a dataset.

    Args:
        data: List of dictionaries
        field: Field name to average

    Returns:
        Average value as float

    Raises:
        ValueError: If field doesn't exist or contains non-numeric data
    """
    if not data:
        raise ValueError("Cannot calculate average of empty dataset")

    values = []
    for record in data:
        if field not in record:
            raise ValueError(f"Field '{field}' not found in data")

        try:
            values.append(float(record[field]))
        except (ValueError, TypeError):
            raise ValueError(f"Field '{field}' contains non-numeric data")

    return sum(values) / len(values)


def calculate_sum(data, field):
    """
    Calculate the sum of a numeric field.

    Args:
        data: List of dictionaries
        field: Field name to sum

    Returns:
        Sum as float
    """
    if not data:
        return 0.0

    values = [float(record[field]) for record in data]
    return sum(values)


def count_by_field(data, field):
    """
    Count occurrences of each unique value in a field.

    Demonstrates:
    - Using collections.Counter from standard library
    - More elegant than manual counting with dict

    Args:
        data: List of dictionaries
        field: Field name to count

    Returns:
        Dictionary mapping values to counts
    """
    # Extract values from field
    values = [record.get(field) for record in data]

    # Counter makes counting easy!
    # Old way: counts = {}; for v in values: counts[v] = counts.get(v, 0) + 1
    # New way: use Counter!
    return dict(Counter(values))


def get_min_max(data, field):
    """
    Find minimum and maximum values of a numeric field.

    Args:
        data: List of dictionaries
        field: Field name

    Returns:
        Tuple of (min_value, max_value)
    """
    if not data:
        raise ValueError("Cannot find min/max of empty dataset")

    values = [float(record[field]) for record in data]
    return min(values), max(values)
