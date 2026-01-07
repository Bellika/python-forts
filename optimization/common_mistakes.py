"""
Common Performance Mistakes
Examples of performance pitfalls and how to avoid them
"""

import time


# Mistake 1: String concatenation in loops
def bad_string_concat():
    """BAD: Creates new string object each iteration"""
    result = ""
    for i in range(1000):
        result += str(i)  # Creates new string each time
    return result


def good_string_join():
    """GOOD: Build list then join once"""
    parts = [str(i) for i in range(1000)]
    return "".join(parts)


# Mistake 2: Checking membership in list
def bad_membership_list():
    """BAD: O(n) for each lookup"""
    valid_users = ["user1", "user2", "user3"] * 100
    return "user500" in valid_users  # Linear search


def good_membership_set():
    """GOOD: O(1) for each lookup"""
    valid_users = set(["user1", "user2", "user3"] * 100)
    return "user500" in valid_users  # Constant time


# Mistake 3: Growing list from left
def bad_insert_at_start():
    """BAD: O(n) for each insert"""
    result = []
    for i in range(1000):
        result.insert(0, i)  # Shifts all elements
    return result


def good_append_and_reverse():
    """GOOD: O(1) append, then reverse once"""
    result = []
    for i in range(1000):
        result.append(i)
    return result[::-1]


# Mistake 4: Repeatedly calling len() in loop
def bad_len_in_loop(items):
    """BAD: Calls len() every iteration"""
    for i in range(len(items)):
        if i < len(items) - 1:  # Unnecessary len() call
            print(items[i])


def good_cache_len(items):
    """GOOD: Calculate len() once"""
    length = len(items)
    for i in range(length):
        if i < length - 1:
            print(items[i])


# Mistake 5: Not using dict.get() with default
def bad_dict_access(counts, key):
    """BAD: Multiple lookups"""
    if key not in counts:
        counts[key] = 0
    counts[key] += 1


def good_dict_get(counts, key):
    """GOOD: Single lookup"""
    counts[key] = counts.get(key, 0) + 1


# Mistake 6: Creating unnecessary lists
def bad_sum_with_list():
    """BAD: Creates entire list in memory"""
    return sum([x**2 for x in range(10000)])


def good_sum_with_generator():
    """GOOD: Uses generator"""
    return sum(x**2 for x in range(10000))


# Mistake 7: Nested loops for lookups
def bad_find_common(list1, list2):
    """BAD: O(n*m)"""
    common = []
    for item in list1:
        if item in list2:  # O(m) for each item
            common.append(item)
    return common


def good_find_common(list1, list2):
    """GOOD: O(n+m)"""
    set2 = set(list2)  # O(m)
    common = []
    for item in list1:  # O(n)
        if item in set2:  # O(1)
            common.append(item)
    return common


# Mistake 8: Not using built-in functions
def bad_manual_max(numbers):
    """BAD: Manual implementation"""
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val


def good_builtin_max(numbers):
    """GOOD: Use built-in"""
    return max(numbers)


# Mistake 9: Copying lists unnecessarily
def bad_list_copy(items):
    """BAD: Unnecessary copy"""
    temp = items[:]  # Full copy
    return sum(temp)


def good_no_copy(items):
    """GOOD: No copy needed"""
    return sum(items)


# Mistake 10: Not using enumerate
def bad_index_tracking(items):
    """BAD: Manual index tracking"""
    i = 0
    for item in items:
        print(f"{i}: {item}")
        i += 1


def good_enumerate(items):
    """GOOD: Use enumerate"""
    for i, item in enumerate(items):
        print(f"{i}: {item}")


# Performance comparison
def compare_mistakes():
    """Compare performance of mistakes vs fixes"""
    iterations = 100

    print("=== String Concatenation ===")
    start = time.perf_counter()
    for _ in range(iterations):
        bad_string_concat()
    time_bad = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(iterations):
        good_string_join()
    time_good = time.perf_counter() - start

    print(f"BAD (+=): {time_bad*1000:.3f} ms")
    print(f"GOOD (join): {time_good*1000:.3f} ms")
    print(f"Speedup: {time_bad/time_good:.1f}x")

    print("\n=== Membership Check ===")
    start = time.perf_counter()
    for _ in range(iterations):
        bad_membership_list()
    time_bad = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(iterations):
        good_membership_set()
    time_good = time.perf_counter() - start

    print(f"BAD (list): {time_bad*1000:.3f} ms")
    print(f"GOOD (set): {time_good*1000:.3f} ms")
    print(f"Speedup: {time_bad/time_good:.1f}x")


def demonstrate():
    print("=== Common Performance Mistakes ===\n")

    print("1. String concatenation in loops")
    print("   BAD:  result += str(i)")
    print("   GOOD: ''.join([str(i) for i in range(n)])")

    print("\n2. Membership checks in lists")
    print("   BAD:  if item in my_list:")
    print("   GOOD: if item in my_set:")

    print("\n3. Growing list from left")
    print("   BAD:  result.insert(0, item)")
    print("   GOOD: result.append(item) then reverse")

    print("\n4. Repeated len() calls")
    print("   BAD:  for i in range(len(items)): if i < len(items):")
    print("   GOOD: length = len(items); for i in range(length):")

    print("\n5. Dictionary access")
    print("   BAD:  if key not in dict: dict[key] = 0")
    print("   GOOD: dict[key] = dict.get(key, 0)")

    print("\n6. Unnecessary lists")
    print("   BAD:  sum([x**2 for x in range(n)])")
    print("   GOOD: sum(x**2 for x in range(n))")

    print("\n7. Nested loops for lookups")
    print("   BAD:  for item in list1: if item in list2:")
    print("   GOOD: set2 = set(list2); if item in set2:")

    print("\n8. Not using built-ins")
    print("   BAD:  Manual max implementation")
    print("   GOOD: max(numbers)")

    print("\n9. Unnecessary copies")
    print("   BAD:  temp = items[:]; sum(temp)")
    print("   GOOD: sum(items)")

    print("\n10. Manual index tracking")
    print("   BAD:  i = 0; for item in items: ... i += 1")
    print("   GOOD: for i, item in enumerate(items):")

    print("\n" + "=" * 50)
    compare_mistakes()


if __name__ == "__main__":
    demonstrate()
