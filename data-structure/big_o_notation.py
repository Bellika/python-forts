"""
Big O Notation - Time Complexity Demonstrations
"""

from typing import List


# O(1) - Constant Time
def access_by_index(data: List[int], index: int) -> int:
    """Always takes the same time regardless of list size"""
    return data[index]


# O(n) - Linear Time
def linear_search(data: List[int], target: int) -> bool:
    """Time grows linearly with input size"""
    for item in data:
        if item == target:
            return True
    return False


# O(n²) - Quadratic Time
def find_all_pairs(data: List[int]) -> List[tuple]:
    """Nested loops - gets slow quickly"""
    pairs = []
    for i in data:
        for j in data:
            pairs.append((i, j))
    return pairs


# O(log n) - Logarithmic Time
def binary_search(sorted_data: List[int], target: int) -> int:
    """Cuts search space in half each iteration"""
    left, right = 0, len(sorted_data) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_data[mid] == target:
            return mid
        elif sorted_data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# O(n log n) - Linearithmic Time
def merge_sort(data: List[int]) -> List[int]:
    """Efficient sorting - divides and conquers"""
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def demonstrate():
    data = list(range(1000))

    # O(1)
    result = access_by_index(data, 500)
    print(f"O(1) - Access index 500: {result}")

    # O(log n)
    result = binary_search(data, 750)
    print(f"O(log n) - Binary search for 750: found at index {result}")

    # O(n)
    result = linear_search(data, 999)
    print(f"O(n) - Linear search for 999: {result}")

    # O(n log n)
    unsorted = [5, 2, 8, 1, 9]
    result = merge_sort(unsorted)
    print(f"O(n log n) - Merge sort {unsorted}: {result}")

    # O(n²)
    small_data = [1, 2, 3]
    result = find_all_pairs(small_data)
    print(f"O(n²) - All pairs of {small_data}: {result}")


if __name__ == "__main__":
    demonstrate()
