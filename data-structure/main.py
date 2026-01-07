"""
Data Structures - Main Entry Point
Demonstrates all data structure concepts
"""

import big_o_notation
import choosing_data_structures
import collections_module
import heapq_priority_queues
import practical_examples


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def main():
    print_section("1. BIG O NOTATION - Time Complexity")
    big_o_notation.demonstrate()

    print_section("2. CHOOSING DATA STRUCTURES - List, Set, Dict, Deque")
    choosing_data_structures.demonstrate()

    print_section("3. COLLECTIONS MODULE - Specialized Structures")
    collections_module.demonstrate()

    print_section("4. HEAPQ - Priority Queues")
    heapq_priority_queues.demonstrate()

    print_section("5. PRACTICAL EXAMPLES - Real-world Use Cases")
    practical_examples.demonstrate()

    print("\n" + "=" * 70)
    print(" All demonstrations completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
