"""
Profiling - Finding Performance Bottlenecks
Using cProfile to identify slow code
"""

import cProfile
import pstats
from io import StringIO


# Slow function to profile
def slow_function():
    """Intentionally slow operations"""
    total = 0
    for i in range(1000):
        total += sum(range(1000))
    return total


# Function with multiple operations
def process_data():
    """Multiple operations to profile"""
    # String concatenation (slow)
    result = ""
    for i in range(1000):
        result += str(i)

    # List operations
    numbers = [i**2 for i in range(1000)]

    # Dictionary operations
    mapping = {i: i**2 for i in range(1000)}

    return result, numbers, mapping


# Profile a single function
def profile_function(func):
    """Profile a function and show results"""
    profiler = cProfile.Profile()
    profiler.enable()

    func()

    profiler.disable()

    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10


# Profile with context manager style
def profile_with_stats():
    """Show how to get detailed stats"""
    profiler = cProfile.Profile()
    profiler.enable()

    slow_function()

    profiler.disable()

    # Get stats as string
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(5)

    print(s.getvalue())


# Compare two approaches
def slow_string_concat():
    """Slow: string concatenation in loop"""
    result = ""
    for i in range(10000):
        result += str(i)
    return result


def fast_string_join():
    """Fast: join with list"""
    parts = []
    for i in range(10000):
        parts.append(str(i))
    return "".join(parts)


def compare_approaches():
    """Profile and compare different approaches"""
    print("=== Slow String Concatenation ===")
    profile_function(slow_string_concat)

    print("\n=== Fast String Join ===")
    profile_function(fast_string_join)


def demonstrate():
    print("=== Profiling slow_function ===")
    profile_function(slow_function)

    print("\n=== Profiling process_data ===")
    profile_function(process_data)


if __name__ == "__main__":
    demonstrate()
