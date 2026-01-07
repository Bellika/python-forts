"""
Optimization - Main Entry Point
Demonstrates all optimization techniques
"""

import profiling
import memory_profiling
import generators
import comprehensions
import memoization
import numpy_optimization
import common_mistakes


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def main():
    print_section("1. PROFILING - Finding Bottlenecks")
    profiling.demonstrate()

    print_section("2. MEMORY PROFILING - Memory Optimization")
    memory_profiling.demonstrate()

    print_section("3. GENERATORS - Lazy Evaluation")
    generators.demonstrate()

    print_section("4. COMPREHENSIONS - Performance Comparison")
    comprehensions.demonstrate()

    print_section("5. MEMOIZATION - Caching with @lru_cache")
    memoization.demonstrate()

    print_section("6. NUMPY - Fast Numerical Operations")
    numpy_optimization.demonstrate()

    print_section("7. COMMON MISTAKES - Performance Pitfalls")
    common_mistakes.demonstrate()

    print("\n" + "=" * 70)
    print(" All demonstrations completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
