"""
Collections Module - Specialized Data Structures
Demonstrates defaultdict, Counter, namedtuple, and deque
"""

from collections import defaultdict, Counter, namedtuple, deque


# defaultdict - Never raises KeyError
def defaultdict_example():
    """Provides default value for missing keys"""
    # Regular dict requires checking if key exists
    regular_dict = {}
    for word in ["apple", "banana", "apple"]:
        if word not in regular_dict:
            regular_dict[word] = 0
        regular_dict[word] += 1

    # defaultdict handles missing keys automatically
    word_count = defaultdict(int)  # int() returns 0
    for word in ["apple", "banana", "apple"]:
        word_count[word] += 1

    # Group items by category
    students_by_grade = defaultdict(list)
    students_by_grade["A"].append("Alice")
    students_by_grade["B"].append("Bob")
    students_by_grade["A"].append("Anna")

    return dict(word_count), dict(students_by_grade)


# Counter - Counting made easy
def counter_example():
    """Specialized dict for counting hashable objects"""
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

    # Count occurrences
    counts = Counter(words)

    # Most common items
    top_2 = counts.most_common(2)

    # Add more counts
    more_words = ["banana", "date", "apple"]
    counts.update(more_words)

    # Subtract counts
    removed = Counter(["apple", "banana"])
    counts.subtract(removed)

    return counts, top_2


# namedtuple - Lightweight class alternative
def namedtuple_example():
    """Immutable data structure with named fields"""
    # Define structure
    Point = namedtuple("Point", ["x", "y"])
    Person = namedtuple("Person", ["name", "age", "city"])

    # Create instances
    p1 = Point(10, 20)
    p2 = Point(x=5, y=15)

    person = Person("Alice", 30, "Stockholm")

    # Access by name or index
    x_coord = p1.x
    name = person[0]

    # Convert to dict
    person_dict = person._asdict()

    # Unpack like tuple
    x, y = p1

    return p1, person, person_dict


# deque - Double-ended queue
def deque_example():
    """Efficient operations at both ends"""
    # Create deque
    d = deque([1, 2, 3])

    # Add to both ends
    d.append(4)        # Add right: [1, 2, 3, 4]
    d.appendleft(0)    # Add left: [0, 1, 2, 3, 4]

    # Remove from both ends
    right = d.pop()         # Remove right: 4
    left = d.popleft()      # Remove left: 0

    # Rotate
    d.rotate(1)   # Rotate right: [3, 1, 2]
    d.rotate(-1)  # Rotate left: [1, 2, 3]

    # Limited size deque (circular buffer)
    recent = deque(maxlen=3)
    for i in range(5):
        recent.append(i)  # Keeps only last 3: [2, 3, 4]

    return list(d), list(recent)


# Practical use case: Recent history
def recent_history_tracker(max_size: int = 5):
    """Track last N actions"""
    history = deque(maxlen=max_size)

    def add_action(action: str):
        history.append(action)
        return list(history)

    add_action("login")
    add_action("view_profile")
    add_action("edit_settings")
    add_action("save_changes")
    add_action("logout")
    add_action("login_again")  # Oldest action dropped - login

    return list(history)


# Practical use case: Word frequency
def analyze_text(text: str):
    """Count word frequency in text"""
    words = text.lower().split()
    word_freq = Counter(words)

    most_common = word_freq.most_common(3)
    total_words = sum(word_freq.values())
    unique_words = len(word_freq)

    return {
        "most_common": most_common,
        "total_words": total_words,
        "unique_words": unique_words
    }


def demonstrate():
    print("=== defaultdict ===")
    counts, students = defaultdict_example()
    print(f"Word counts: {counts}")
    print(f"Students by grade: {students}")

    print("\n=== Counter ===")
    counts, top_2 = counter_example()
    print(f"Counts: {counts}")
    print(f"Top 2: {top_2}")

    print("\n=== namedtuple ===")
    point, person, person_dict = namedtuple_example()
    print(f"Point: {point}")
    print(f"Person: {person}")
    print(f"As dict: {person_dict}")

    print("\n=== deque ===")
    deque_result, recent = deque_example()
    print(f"Deque: {deque_result}")
    print(f"Recent (maxlen=3): {recent}")

    print("\n=== Recent History ===")
    history = recent_history_tracker()
    print(f"Last 5 actions: {history}")

    print("\n=== Text Analysis ===")
    text = "python is great python is powerful python is fun"
    analysis = analyze_text(text)
    print(f"Analysis: {analysis}")


if __name__ == "__main__":
    demonstrate()
