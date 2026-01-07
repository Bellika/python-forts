"""
Heapq - Priority Queues
Efficient implementation of priority queue using min-heap
"""

import heapq
from typing import List, Tuple
from dataclasses import dataclass


# Basic heap operations
def basic_heap_operations():
    """Min-heap: smallest element always at index 0"""
    heap = []

    # Add items
    heapq.heappush(heap, 5)
    heapq.heappush(heap, 2)
    heapq.heappush(heap, 8)
    heapq.heappush(heap, 1)

    # Get smallest (doesn't remove)
    smallest = heap[0]

    # Remove and return smallest
    first = heapq.heappop(heap)   # Returns 1
    second = heapq.heappop(heap)  # Returns 2

    return heap, smallest, first, second


# Convert list to heap
def heapify_example():
    """Transform list into heap in-place"""
    numbers = [5, 2, 8, 1, 9, 3]
    heapq.heapify(numbers)  # O(n) - more efficient than n pushes
    return numbers


# N largest/smallest items
def find_extremes():
    """Find N largest or smallest items efficiently"""
    numbers = [34, 12, 78, 23, 56, 89, 45, 67]

    largest_3 = heapq.nlargest(3, numbers)
    smallest_3 = heapq.nsmallest(3, numbers)

    # Works with key function
    words = ["python", "is", "awesome", "and", "powerful"]
    longest_2 = heapq.nlargest(2, words, key=len)

    return largest_3, smallest_3, longest_2


# Priority queue with tuples
def priority_queue_tuples():
    """Lower number = higher priority"""
    tasks = []

    # (priority, task_name)
    heapq.heappush(tasks, (2, "medium_task"))
    heapq.heappush(tasks, (1, "high_priority"))
    heapq.heappush(tasks, (3, "low_priority"))
    heapq.heappush(tasks, (1, "also_high_priority"))

    # Process in priority order
    result = []
    while tasks:
        priority, task = heapq.heappop(tasks)
        result.append((priority, task))

    return result


# Priority queue with objects
@dataclass
class Task:
    """Task with priority and description"""
    priority: int
    name: str
    description: str

    def __lt__(self, other):
        """Required for heap comparison"""
        return self.priority < other.priority


def priority_queue_objects():
    """Priority queue with custom objects"""
    tasks = []

    task1 = Task(2, "Code Review", "Review PR #123")
    task2 = Task(1, "Bug Fix", "Fix critical bug")
    task3 = Task(3, "Documentation", "Update README")
    task4 = Task(1, "Deploy", "Deploy to production")

    heapq.heappush(tasks, task1)
    heapq.heappush(tasks, task2)
    heapq.heappush(tasks, task3)
    heapq.heappush(tasks, task4)

    result = []
    while tasks:
        task = heapq.heappop(tasks)
        result.append(f"Priority {task.priority}: {task.name}")

    return result


# Merge sorted sequences
def merge_sorted_sequences():
    """Efficiently merge multiple sorted sequences"""
    seq1 = [1, 4, 7, 10]
    seq2 = [2, 5, 8, 11]
    seq3 = [3, 6, 9, 12]

    merged = list(heapq.merge(seq1, seq2, seq3))
    return merged


# K-way merge
def merge_sorted_files(files: List[List[int]]) -> List[int]:
    """Merge K sorted lists efficiently"""
    return list(heapq.merge(*files))


# Find K smallest in stream
class KSmallest:
    """Track K smallest items in a stream"""
    def __init__(self, k: int):
        self.k = k
        self.heap = []

    def add(self, num: int):
        """Add number to stream"""
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, -num)  # Negative for max-heap behavior
        elif num < -self.heap[0]:
            heapq.heapreplace(self.heap, -num)

    def get_smallest(self) -> List[int]:
        """Get K smallest numbers"""
        return sorted([-x for x in self.heap])


def demonstrate():
    print("=== Basic Heap Operations ===")
    heap, smallest, first, second = basic_heap_operations()
    print(f"Heap: {heap}")
    print(f"Smallest: {smallest}, First popped: {first}, Second popped: {second}")

    print("\n=== Heapify ===")
    heap = heapify_example()
    print(f"Heapified: {heap}")

    print("\n=== Find Extremes ===")
    largest, smallest, longest = find_extremes()
    print(f"Largest 3: {largest}")
    print(f"Smallest 3: {smallest}")
    print(f"Longest 2 words: {longest}")

    print("\n=== Priority Queue (Tuples) ===")
    tasks = priority_queue_tuples()
    print(f"Tasks by priority: {tasks}")

    print("\n=== Priority Queue (Objects) ===")
    tasks = priority_queue_objects()
    for task in tasks:
        print(f"  {task}")

    print("\n=== Merge Sorted Sequences ===")
    merged = merge_sorted_sequences()
    print(f"Merged: {merged}")

    print("\n=== K Smallest in Stream ===")
    tracker = KSmallest(3)
    for num in [5, 2, 8, 1, 9, 3, 7]:
        tracker.add(num)
    print(f"3 smallest from stream: {tracker.get_smallest()}")


if __name__ == "__main__":
    demonstrate()
