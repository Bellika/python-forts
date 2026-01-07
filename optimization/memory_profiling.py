"""
Memory Profiling - Understanding Memory Usage
Comparing memory usage of different approaches
"""

import sys


# Compare memory usage
def get_size(obj):
    """Get size of object in bytes"""
    return sys.getsizeof(obj)


# List vs Generator
def list_approach():
    """Stores all items in memory"""
    return [i**2 for i in range(10000)]


def generator_approach():
    """Generates items on demand"""
    return (i**2 for i in range(10000))


def compare_memory():
    """Compare memory usage"""
    my_list = list_approach()
    my_gen = generator_approach()

    print(f"List size: {get_size(my_list):,} bytes")
    print(f"Generator size: {get_size(my_gen):,} bytes")
    print(f"Difference: {get_size(my_list) - get_size(my_gen):,} bytes")


# String concatenation vs join
def string_concat_memory():
    """Memory inefficient - creates many intermediate strings"""
    result = ""
    for i in range(1000):
        result += str(i)
    return result


def string_join_memory():
    """Memory efficient - builds list then joins once"""
    parts = [str(i) for i in range(1000)]
    return "".join(parts)


# Slot optimization for classes
class RegularClass:
    """Regular class - uses dict for attributes"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SlottedClass:
    """Slotted class - uses less memory"""
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def compare_class_memory():
    """Compare memory usage of classes"""
    regular = RegularClass(1, 2, 3)
    slotted = SlottedClass(1, 2, 3)

    print(f"Regular class: {get_size(regular)} bytes")
    print(f"Slotted class: {get_size(slotted)} bytes")

    # Create many instances
    regular_list = [RegularClass(i, i, i) for i in range(1000)]
    slotted_list = [SlottedClass(i, i, i) for i in range(1000)]

    regular_total = sum(get_size(obj) for obj in regular_list)
    slotted_total = sum(get_size(obj) for obj in slotted_list)

    print(f"\n1000 regular instances: {regular_total:,} bytes")
    print(f"1000 slotted instances: {slotted_total:,} bytes")


# Iterator vs loading all data
def process_large_file_bad(filename):
    """Loads entire file into memory"""
    with open(filename) as f:
        lines = f.readlines()  # All lines in memory
        for line in lines:
            process_line(line)


def process_large_file_good(filename):
    """Processes file line by line"""
    with open(filename) as f:
        for line in f:  # One line at a time
            process_line(line)


def process_line(line):
    """Dummy processing"""
    return line.strip()


def demonstrate():
    print("=== List vs Generator Memory ===")
    compare_memory()

    print("\n=== Class Memory (__slots__) ===")
    compare_class_memory()

    print("\n=== Data Structure Sizes ===")
    empty_list = []
    empty_dict = {}
    empty_set = set()
    empty_tuple = ()

    print(f"Empty list: {get_size(empty_list)} bytes")
    print(f"Empty dict: {get_size(empty_dict)} bytes")
    print(f"Empty set: {get_size(empty_set)} bytes")
    print(f"Empty tuple: {get_size(empty_tuple)} bytes")

    numbers = list(range(100))
    print(f"\nList of 100 numbers: {get_size(numbers)} bytes")
    print(f"Average per item: {get_size(numbers) / 100:.1f} bytes")


if __name__ == "__main__":
    demonstrate()
