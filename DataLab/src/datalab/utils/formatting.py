"""
Formatting utilities for DataLab.

Demonstrates:
- Number formatting with f-strings and format specifiers
- Working with locale (for Swedish number formatting)
- String manipulation
- Reusable formatting functions
"""

from datalab import config


def format_number(number, decimals=None):
    """
    Format a number with specified decimal places.

    Args:
        number: Number to format
        decimals: Number of decimal places (uses config default if None)

    Returns:
        Formatted string

    Example:
        >>> format_number(1234.5678, 2)
        '1234.57'
    """
    if decimals is None:
        decimals = config.DECIMAL_PLACES
    return f'{number:.{decimals}f}'


def format_currency(amount, currency='SEK', decimals=0):
    """
    Format a number as currency.

    Demonstrates:
    - Number formatting
    - String concatenation
    - Default parameters

    Args:
        amount: Amount to format
        currency: Currency code (default: SEK)
        decimals: Decimal places (default: 0 for whole amounts)

    Returns:
        Formatted currency string

    Example:
        >>> format_currency(45000)
        '45,000 SEK'
        >>> format_currency(45000.50, 'EUR', 2)
        '45,000.50 EUR'
    """
    # Format with thousand separators
    formatted = f'{amount:,.{decimals}f}'
    return f'{formatted} {currency}'


def format_percentage(value, total, decimals=1):
    """
    Calculate and format a percentage.

    Args:
        value: Part value
        total: Total value
        decimals: Decimal places for percentage

    Returns:
        Formatted percentage string

    Example:
        >>> format_percentage(25, 100)
        '25.0%'
    """
    if total == 0:
        return '0.0%'

    percentage = (value / total) * 100
    return f'{percentage:.{decimals}f}%'


def format_list(items, separator=', ', final_separator=' and '):
    """
    Format a list as a human-readable string.

    Demonstrates:
    - List manipulation
    - String joining
    - Edge case handling

    Args:
        items: List of items to format
        separator: Separator between items
        final_separator: Separator before last item

    Returns:
        Formatted string

    Example:
        >>> format_list(['apple', 'banana', 'orange'])
        'apple, banana and orange'
    """
    if not items:
        return ''
    if len(items) == 1:
        return str(items[0])
    if len(items) == 2:
        return f'{items[0]}{final_separator}{items[1]}'

    return separator.join(str(item) for item in items[:-1]) + final_separator + str(items[-1])


def truncate_string(text, max_length=50, suffix='...'):
    """
    Truncate a string to maximum length.

    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string

    Example:
        >>> truncate_string('This is a very long string', 15)
        'This is a ve...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def main():
    """Test the formatting module."""
    print("=" * 60)
    print("DataLab Formatting Module")
    print("=" * 60)

    print("\n=== Number Formatting ===")
    print(f"format_number(1234.5678, 2): {format_number(1234.5678, 2)}")
    print(f"format_number(3.14159, 4): {format_number(3.14159, 4)}")

    print("\n=== Currency Formatting ===")
    print(f"format_currency(45000): {format_currency(45000)}")
    print(f"format_currency(45000.50, 'EUR', 2): {format_currency(45000.50, 'EUR', 2)}")
    print(f"format_currency(1234567, 'USD'): {format_currency(1234567, 'USD')}")

    print("\n=== Percentage Formatting ===")
    print(f"format_percentage(25, 100): {format_percentage(25, 100)}")
    print(f"format_percentage(3, 7): {format_percentage(3, 7)}")
    print(f"format_percentage(0, 100): {format_percentage(0, 100)}")

    print("\n=== List Formatting ===")
    print(f"format_list(['apple', 'banana']): {format_list(['apple', 'banana'])}")
    print(f"format_list(['a', 'b', 'c']): {format_list(['a', 'b', 'c'])}")
    cities = ['Stockholm', 'Göteborg', 'Malmö', 'Uppsala']
    print(f"format_list(cities): {format_list(cities)}")

    print("\n=== String Truncation ===")
    long_text = "This is a very long string that needs to be truncated"
    print(f"Original: {long_text}")
    print(f"Truncated (20): {truncate_string(long_text, 20)}")
    print(f"Truncated (30): {truncate_string(long_text, 30)}")


if __name__ == '__main__':
    main()
