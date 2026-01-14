"""
Comparison of Asyncio, Threading, and Multiprocessing

This module provides side-by-side comparisons to demonstrate when to use
each concurrency approach: asyncio, threading, or multiprocessing.
"""

import asyncio
import threading
import multiprocessing
import time
from typing import Callable


# ============================================================================
# I/O-BOUND TASK: Simulated network requests
# Best for: Asyncio > Threading > Sequential
# ============================================================================

def simulate_io_request(request_id: int) -> str:
    """Simulates an I/O-bound task (e.g., network request)."""
    time.sleep(0.5)  # Blocking sleep
    return f"Response {request_id}"


async def simulate_io_request_async(request_id: int) -> str:
    """Async version of I/O request simulation."""
    await asyncio.sleep(0.5)  # Non-blocking sleep
    return f"Response {request_id}"


def io_bound_sequential():
    """Sequential execution of I/O-bound tasks."""
    print("\n--- I/O-Bound: Sequential ---")
    start = time.time()

    results = [simulate_io_request(i) for i in range(10)]

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    return elapsed


def io_bound_threading():
    """Threading for I/O-bound tasks."""
    print("\n--- I/O-Bound: Threading ---")
    start = time.time()

    results = []
    threads = []

    def worker(request_id: int):
        result = simulate_io_request(request_id)
        results.append(result)

    # Create and start threads
    for i in range(10):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    return elapsed


async def io_bound_asyncio():
    """Asyncio for I/O-bound tasks."""
    print("\n--- I/O-Bound: Asyncio ---")
    start = time.time()

    # Run all requests concurrently
    tasks = [simulate_io_request_async(i) for i in range(10)]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    return elapsed


def io_bound_multiprocessing():
    """Multiprocessing for I/O-bound tasks (not recommended)."""
    print("\n--- I/O-Bound: Multiprocessing ---")
    start = time.time()

    # Use process pool
    with multiprocessing.Pool(processes=10) as pool:
        results = pool.map(simulate_io_request, range(10))

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    return elapsed


# ============================================================================
# CPU-BOUND TASK: Heavy computation
# Best for: Multiprocessing > Sequential > Threading
# ============================================================================

def cpu_intensive_task(n: int) -> int:
    """CPU-intensive computation."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def cpu_bound_sequential():
    """Sequential execution of CPU-bound tasks."""
    print("\n--- CPU-Bound: Sequential ---")
    start = time.time()

    n = 5_000_000
    results = [cpu_intensive_task(n) for _ in range(4)]

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    return elapsed


def cpu_bound_threading():
    """Threading for CPU-bound tasks (limited by GIL)."""
    print("\n--- CPU-Bound: Threading ---")
    start = time.time()

    n = 5_000_000
    threads = []

    def worker():
        cpu_intensive_task(n)

    # Create and start threads
    for _ in range(4):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s (slower due to GIL!)")
    return elapsed


def cpu_bound_multiprocessing():
    """Multiprocessing for CPU-bound tasks (bypasses GIL)."""
    print("\n--- CPU-Bound: Multiprocessing ---")
    start = time.time()

    n = 5_000_000
    tasks = [n] * 4

    # Use process pool
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(cpu_intensive_task, tasks)

    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s (true parallelism!)")
    return elapsed


# ============================================================================
# COMPARISON SUMMARIES
# ============================================================================

def compare_io_bound():
    """
    Compares all approaches for I/O-bound tasks.
    Expected ranking: Asyncio ≈ Threading >> Sequential > Multiprocessing
    """
    print("\n" + "=" * 60)
    print("COMPARISON: I/O-BOUND TASKS (10 simulated network requests)")
    print("=" * 60)

    seq_time = io_bound_sequential()
    thread_time = io_bound_threading()
    mp_time = io_bound_multiprocessing()

    # Asyncio needs to be run in async context
    async_time = asyncio.run(io_bound_asyncio())

    print("\n--- RESULTS ---")
    print(f"Sequential:      {seq_time:.2f}s (baseline)")
    print(f"Threading:       {thread_time:.2f}s ({seq_time/thread_time:.1f}x faster)")
    print(f"Asyncio:         {async_time:.2f}s ({seq_time/async_time:.1f}x faster)")
    print(f"Multiprocessing: {mp_time:.2f}s ({seq_time/mp_time:.1f}x faster)")

    print("\nRECOMMENDATION: Use Asyncio or Threading for I/O-bound tasks")
    print("- Asyncio: Best for many concurrent I/O operations")
    print("- Threading: Good alternative, easier to integrate with sync code")
    print("- Multiprocessing: Overhead too high for I/O tasks")


def compare_cpu_bound():
    """
    Compares all approaches for CPU-bound tasks.
    Expected ranking: Multiprocessing >> Sequential > Threading
    """
    print("\n" + "=" * 60)
    print("COMPARISON: CPU-BOUND TASKS (4 heavy computations)")
    print("=" * 60)

    seq_time = cpu_bound_sequential()
    thread_time = cpu_bound_threading()
    mp_time = cpu_bound_multiprocessing()

    print("\n--- RESULTS ---")
    print(f"Sequential:      {seq_time:.2f}s (baseline)")
    print(f"Threading:       {thread_time:.2f}s ({seq_time/thread_time:.1f}x speedup)")
    print(f"Multiprocessing: {mp_time:.2f}s ({seq_time/mp_time:.1f}x faster)")

    print("\nRECOMMENDATION: Use Multiprocessing for CPU-bound tasks")
    print("- Multiprocessing: True parallelism, bypasses GIL")
    print("- Threading: Actually SLOWER due to GIL and context switching")
    print("- Sequential: Better than threading for CPU-bound work!")


# ============================================================================
# DECISION GUIDE
# ============================================================================

def print_decision_guide():
    """Prints a decision guide for choosing concurrency approach."""
    print("\n" + "=" * 60)
    print("DECISION GUIDE: When to Use What?")
    print("=" * 60)

    guide = """
1. ASYNCIO
   Use when:
   - Many I/O-bound tasks (network, file operations)
   - Need high concurrency (thousands of connections)
   - Modern async libraries available (aiohttp, asyncpg)

   Advantages:
   - Very lightweight (single thread)
   - Excellent for high concurrency
   - Low memory overhead

   Disadvantages:
   - Requires async/await throughout codebase
   - Can't use blocking libraries
   - Not for CPU-bound tasks

2. THREADING
   Use when:
   - I/O-bound tasks with existing blocking code
   - Need to integrate with sync libraries
   - Moderate concurrency requirements

   Advantages:
   - Works with existing blocking code
   - Easy to understand and implement
   - Good for I/O-bound tasks

   Disadvantages:
   - Limited by GIL for CPU-bound tasks
   - Thread safety concerns (need locks)
   - Higher memory than asyncio

3. MULTIPROCESSING
   Use when:
   - CPU-bound tasks (computation, data processing)
   - Need true parallelism
   - Can split work into independent chunks

   Advantages:
   - Bypasses GIL
   - True parallelism on multiple cores
   - Isolated memory per process

   Disadvantages:
   - High overhead (process creation)
   - No shared memory (need IPC)
   - More complex than threading

SUMMARY TABLE:
┌─────────────────┬──────────┬───────────┬────────────────┐
│ Task Type       │ Asyncio  │ Threading │ Multiprocess   │
├─────────────────┼──────────┼───────────┼────────────────┤
│ I/O-Bound       │ ⭐⭐⭐    │ ⭐⭐⭐     │ ⭐             │
│ CPU-Bound       │ ❌       │ ❌        │ ⭐⭐⭐          │
│ Mixed           │ ⭐⭐     │ ⭐⭐      │ ⭐⭐           │
│ High Concur.    │ ⭐⭐⭐    │ ⭐⭐      │ ⭐             │
│ Simplicity      │ ⭐⭐     │ ⭐⭐⭐     │ ⭐⭐           │
└─────────────────┴──────────┴───────────┴────────────────┘
"""
    print(guide)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main function that runs all comparisons.
    """
    print("=" * 60)
    print("CONCURRENCY COMPARISON")
    print("Asyncio vs Threading vs Multiprocessing")
    print("=" * 60)

    # Run comparisons
    compare_io_bound()
    compare_cpu_bound()

    # Print decision guide
    print_decision_guide()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("- I/O-bound: Use asyncio or threading")
    print("- CPU-bound: Use multiprocessing")
    print("- When in doubt: Profile and measure!")
    print("=" * 60)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
