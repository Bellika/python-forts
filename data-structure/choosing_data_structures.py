"""
Choosing the Right Data Structure
Comparison of list, set, dict, and deque
"""

from collections import deque
from typing import List, Set, Dict


# List - Use when order matters and you need indexing
def list_operations():
    """Lists: ordered, indexed, allows duplicates"""
    users = ["Alice", "Bob", "Charlie", "Alice"]

    users.append("David")              # O(1) - add to end
    first_user = users[0]              # O(1) - access by index
    users.insert(0, "Eve")             # O(n) - insert at beginning
    users.remove("Alice")              # O(n) - remove first occurrence

    # Good for: ordered data, frequent indexing, allowing duplicates
    return users


# Set - Use when you need unique items and fast membership testing
def set_operations():
    """Sets: unordered, unique items, fast lookup"""
    tags = {"python", "coding", "tutorial"}

    tags.add("python")                 # O(1) - duplicates ignored
    tags.add("django")                 # O(1) - add item
    has_python = "python" in tags      # O(1) - check membership
    tags.remove("coding")              # O(1) - remove item

    # Good for: uniqueness, membership tests, set operations
    return tags


# Dict - Use when you need key-value pairs and fast lookup
def dict_operations():
    """Dicts: key-value pairs, fast lookup by key"""
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}

    scores["David"] = 88               # O(1) - add/update
    alice_score = scores.get("Alice")  # O(1) - get by key
    has_eve = "Eve" in scores          # O(1) - check if key exists
    del scores["Bob"]                  # O(1) - remove by key

    # Good for: lookups by key, counting
    return scores


# Deque - Use when you need fast operations at both ends
def deque_operations():
    """Deques: double-ended queue, fast at both ends"""
    queue = deque(["task1", "task2", "task3"])

    queue.append("task4")              # O(1) - add to right
    queue.appendleft("task0")          # O(1) - add to left
    first = queue.popleft()            # O(1) - remove from left
    last = queue.pop()                 # O(1) - remove from right

    # Good for: queues, sliding windows, recent items
    return queue


# Comparison: Finding duplicates
def find_duplicates_list(data: List[int]) -> List[int]:
    """Using list - O(n²) - inefficient"""
    duplicates = []
    for i, item in enumerate(data):
        if item in data[i+1:] and item not in duplicates:
            duplicates.append(item)
    return duplicates


def find_duplicates_set(data: List[int]) -> Set[int]:
    """Using set - O(n) - efficient"""
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates


# Comparison: Counting occurrences
def count_with_dict(words: List[str]) -> Dict[str, int]:
    """Dict is perfect for counting"""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


# Comparison: Queue vs List
def queue_with_list(items: List[str]) -> str:
    """Using list as queue - O(n) for pop(0)"""
    queue = items.copy()
    queue.append("new_item")
    first = queue.pop(0)  # Slow - shifts all elements
    return first


def queue_with_deque(items: List[str]) -> str:
    """Using deque as queue - O(1) for popleft()"""
    queue = deque(items)
    queue.append("new_item")
    first = queue.popleft()  # Fast - designed for this
    return first


def demonstrate():
    print("List:", list_operations())
    print("Set:", set_operations())
    print("Dict:", dict_operations())
    print("Deque:", deque_operations())

    # Show performance differences
    data = [1, 2, 3, 2, 4, 5, 3, 6]
    print(f"\nFind duplicates in {data}:")
    print("With list (slow):", find_duplicates_list(data))
    print("With set (fast):", find_duplicates_set(data))

    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    print(f"\nCount words {words}:")
    print("With dict:", count_with_dict(words))


if __name__ == "__main__":
    demonstrate()
