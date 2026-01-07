"""
Memoization - Caching for Performance
Using @lru_cache to avoid redundant calculations
"""

from functools import lru_cache
import time


# Fibonacci without caching - very slow
def fibonacci_slow(n):
    """Without cache - recalculates same values"""
    if n < 2:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)


# Fibonacci with caching - fast
@lru_cache(maxsize=None)
def fibonacci_cached(n):
    """With cache - calculates each value once"""
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


# Manual caching with dict
def fibonacci_manual():
    """Manual cache implementation"""
    cache = {}

    def fib(n):
        if n in cache:
            return cache[n]
        if n < 2:
            return n
        result = fib(n - 1) + fib(n - 2)
        cache[n] = result
        return result

    return fib


# Cache with limited size
@lru_cache(maxsize=128)
def expensive_computation(x, y):
    """Cache last 128 results"""
    time.sleep(0.1)  # Simulate expensive operation
    return x**2 + y**2


# Cache info
@lru_cache(maxsize=32)
def cached_function(n):
    """Function with cache info"""
    return n**2


def demonstrate_cache_info():
    """Show cache statistics"""
    for i in range(10):
        cached_function(i % 5)

    info = cached_function.cache_info()
    print(f"Hits: {info.hits}")
    print(f"Misses: {info.misses}")
    print(f"Size: {info.currsize}")
    print(f"Max size: {info.maxsize}")


# Clear cache
@lru_cache(maxsize=None)
def data_processor(data):
    """Cache can be cleared"""
    return [x**2 for x in data]


# Use case: API calls
@lru_cache(maxsize=100)
def fetch_user_data(user_id):
    """Cache API responses"""
    # Simulate API call
    time.sleep(0.01)
    return {"id": user_id, "name": f"User{user_id}"}


def time_comparison():
    """Compare cached vs uncached performance"""
    print("=== Fibonacci Performance ===")

    # Slow version
    start = time.perf_counter()
    result1 = fibonacci_slow(20)
    time1 = time.perf_counter() - start
    print(f"Without cache: {time1*1000:.3f} ms (result: {result1})")

    # Cached version
    start = time.perf_counter()
    result2 = fibonacci_cached(20)
    time2 = time.perf_counter() - start
    print(f"With cache: {time2*1000:.3f} ms (result: {result2})")

    print(f"Speedup: {time1/time2:.1f}x faster")


def demonstrate():
    print("=== Basic Caching ===")
    time_comparison()

    print("\n=== Cache Info ===")
    demonstrate_cache_info()

    print("\n=== Cached API Calls ===")
    start = time.perf_counter()
    for _ in range(3):
        fetch_user_data(1)  # Same user - cached
    time_cached = time.perf_counter() - start
    print(f"3 calls to same user: {time_cached*1000:.1f} ms")

    start = time.perf_counter()
    for i in range(3):
        fetch_user_data(i)  # Different users - not cached
    time_uncached = time.perf_counter() - start
    print(f"3 calls to different users: {time_uncached*1000:.1f} ms")


if __name__ == "__main__":
    demonstrate()
