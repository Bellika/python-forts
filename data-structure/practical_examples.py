"""
Practical Examples - Real-world use cases
Demonstrates when the right data structure makes a difference
"""

from collections import defaultdict, Counter, deque
import heapq


# Example 1: URL shortener
class URLShortener:
    """Using dict for O(1) lookups"""
    def __init__(self):
        self.url_map = {}
        self.counter = 1000

    def shorten(self, long_url: str) -> str:
        short_code = f"short.ly/{self.counter}"
        self.url_map[short_code] = long_url
        self.counter += 1
        return short_code

    def expand(self, short_url: str) -> str:
        return self.url_map.get(short_url, "URL not found")


# Example 2: Cache with size limit
class LRUCache:
    """Least Recently Used cache using deque"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.access_order = deque()

    def get(self, key: str):
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def put(self, key: str, value):
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.access_order.popleft()
            del self.cache[oldest]

        self.cache[key] = value
        self.access_order.append(key)


# Example 3: Group data by category
def group_by_category(items: list) -> dict:
    """Using defaultdict to avoid key checking"""
    grouped = defaultdict(list)

    for item in items:
        category = item.get("category", "uncategorized")
        grouped[category].append(item)

    return dict(grouped)


# Example 4: Find most common elements
def find_most_popular(items: list, top_n: int = 3) -> list:
    """Using Counter for frequency analysis"""
    counts = Counter(items)
    return counts.most_common(top_n)


# Example 5: Task scheduler with priorities
class TaskScheduler:
    """Using heapq for priority-based scheduling"""
    def __init__(self):
        self.tasks = []
        self.task_id = 0

    def add_task(self, priority: int, description: str):
        # Lower priority number = higher priority
        heapq.heappush(self.tasks, (priority, self.task_id, description))
        self.task_id += 1

    def get_next_task(self):
        if self.tasks:
            priority, task_id, description = heapq.heappop(self.tasks)
            return description
        return None


# Example 6: Remove duplicates while preserving order
def remove_duplicates_ordered(items: list) -> list:
    """Using set for O(1) membership check"""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# Example 7: Find intersection of lists
def find_common_elements(list1: list, list2: list) -> set:
    """Using sets for efficient intersection"""
    return set(list1) & set(list2)


# Example 8: Sliding window maximum
def sliding_window_max(nums: list, k: int) -> list:
    """Using deque for efficient window tracking"""
    if not nums or k == 0:
        return []

    result = []
    window = deque()

    for i, num in enumerate(nums):
        # Remove elements outside window
        while window and window[0] <= i - k:
            window.popleft()

        # Remove smaller elements (they won't be max)
        while window and nums[window[-1]] < num:
            window.pop()

        window.append(i)

        # Add to result once window is full
        if i >= k - 1:
            result.append(nums[window[0]])

    return result


# Example 9: Graph with adjacency list
def build_graph(edges: list) -> dict:
    """Using defaultdict(list) for graph representation"""
    graph = defaultdict(list)
    for source, destination in edges:
        graph[source].append(destination)
    return dict(graph)


# Example 10: Top K frequent words
def top_k_frequent_words(words: list, k: int) -> list:
    """Combining Counter and heapq"""
    counts = Counter(words)
    return heapq.nlargest(k, counts.items(), key=lambda x: x[1])


def demonstrate():
    print("=== URL Shortener ===")
    shortener = URLShortener()
    short = shortener.shorten("https://example.com/very/long/url")
    print(f"Shortened: {short}")
    print(f"Expanded: {shortener.expand(short)}")

    print("\n=== LRU Cache ===")
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.put("d", 4)  # Evicts "a"
    print(f"Get 'a': {cache.get('a')}")  # None (evicted)
    print(f"Get 'b': {cache.get('b')}")  # 2

    print("\n=== Group by Category ===")
    items = [
        {"name": "Apple", "category": "Fruit"},
        {"name": "Carrot", "category": "Vegetable"},
        {"name": "Banana", "category": "Fruit"},
    ]
    grouped = group_by_category(items)
    print(f"Grouped: {grouped}")

    print("\n=== Most Popular ===")
    clicks = ["home", "about", "home", "contact", "home", "about"]
    popular = find_most_popular(clicks, 2)
    print(f"Top 2 pages: {popular}")

    print("\n=== Task Scheduler ===")
    scheduler = TaskScheduler()
    scheduler.add_task(2, "Send email")
    scheduler.add_task(1, "Fix critical bug")
    scheduler.add_task(3, "Update docs")
    print(f"Next task: {scheduler.get_next_task()}")
    print(f"Next task: {scheduler.get_next_task()}")

    print("\n=== Remove Duplicates (preserve order) ===")
    items = [1, 2, 3, 2, 4, 1, 5]
    unique = remove_duplicates_ordered(items)
    print(f"Original: {items}")
    print(f"Unique: {unique}")

    print("\n=== Common Elements ===")
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]
    common = find_common_elements(list1, list2)
    print(f"Common: {common}")

    print("\n=== Sliding Window Maximum ===")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    result = sliding_window_max(nums, k=3)
    print(f"Array: {nums}")
    print(f"Max in each window of 3: {result}")

    print("\n=== Build Graph ===")
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    graph = build_graph(edges)
    print(f"Graph: {graph}")

    print("\n=== Top K Frequent Words ===")
    words = ["python", "java", "python", "javascript", "python", "java"]
    top_2 = top_k_frequent_words(words, 2)
    print(f"Top 2 frequent: {top_2}")


if __name__ == "__main__":
    demonstrate()
