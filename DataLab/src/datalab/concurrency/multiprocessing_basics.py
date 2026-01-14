"""
Multiprocessing Basics - True Parallelism in Python

This module demonstrates multiprocessing for CPU-bound tasks.
Each process has its own Python interpreter and memory space, bypassing the GIL.
"""

import multiprocessing
import time
from typing import List


# 1. CPU-bound task example
def compute_sum_of_squares(n: int) -> int:
    """
    A CPU-intensive task that computes sum of squares.

    Args:
        n: Upper limit for computation

    Returns:
        Sum of squares from 1 to n
    """
    print(f"[Process {multiprocessing.current_process().name}] Computing sum for n={n}")
    total = sum(i * i for i in range(n))
    print(f"[Process {multiprocessing.current_process().name}] Completed")
    return total


def basic_multiprocessing():
    """
    Demonstrates creating and running processes manually.
    """
    print("\n=== Basic Multiprocessing ===")
    start = time.time()

    # Note: We can't easily get return values with basic Process
    # So we'll just run the computations
    processes: List[multiprocessing.Process] = []

    for i in range(3):
        process = multiprocessing.Process(
            target=compute_sum_of_squares,
            args=(10_000_000,)
        )
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    elapsed = time.time() - start
    print(f"All processes completed in {elapsed:.2f}s")


# 2. Using Process Pool for easier management
def process_number(n: int) -> int:
    """
    A simple CPU-bound function that processes a number.

    Args:
        n: Number to process

    Returns:
        Result of computation
    """
    result = sum(i * i for i in range(n))
    return result


def pool_example():
    """
    Demonstrates using a Pool to manage multiple processes.
    Pool makes it easy to distribute work and collect results.
    """
    print("\n=== Process Pool ===")
    start = time.time()

    numbers = [10_000_000, 15_000_000, 12_000_000, 18_000_000]

    # Create a pool with 4 worker processes
    with multiprocessing.Pool(processes=4) as pool:
        # Map work to processes and collect results
        results = pool.map(process_number, numbers)

    elapsed = time.time() - start
    print(f"Processed {len(numbers)} tasks in {elapsed:.2f}s")
    print(f"Results (first 100 chars): {str(results)[:100]}...")


# 3. CPU-bound: Multiprocessing vs Sequential
def sequential_computation():
    """
    Runs CPU-bound tasks sequentially for comparison.
    """
    print("\n=== Sequential Computation ===")
    start = time.time()

    numbers = [10_000_000, 15_000_000, 12_000_000, 18_000_000]
    results = [process_number(n) for n in numbers]

    elapsed = time.time() - start
    print(f"Processed {len(numbers)} tasks in {elapsed:.2f}s")
    print(f"Results (first 100 chars): {str(results)[:100]}...")


def parallel_computation():
    """
    Runs CPU-bound tasks in parallel using multiprocessing.
    """
    print("\n=== Parallel Computation ===")
    start = time.time()

    numbers = [10_000_000, 15_000_000, 12_000_000, 18_000_000]

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(process_number, numbers)

    elapsed = time.time() - start
    print(f"Processed {len(numbers)} tasks in {elapsed:.2f}s")
    print(f"Results (first 100 chars): {str(results)[:100]}...")


# 4. Sharing data between processes using Queue
def producer(queue: multiprocessing.Queue, items: List[int]):
    """
    Producer process that puts items into a queue.

    Args:
        queue: Shared queue for communication
        items: Items to produce
    """
    print(f"[Producer] Starting...")
    for item in items:
        print(f"[Producer] Producing: {item}")
        queue.put(item)
        time.sleep(0.1)
    queue.put(None)  # Sentinel value to signal completion
    print(f"[Producer] Done")


def consumer(queue: multiprocessing.Queue):
    """
    Consumer process that gets items from a queue.

    Args:
        queue: Shared queue for communication
    """
    print(f"[Consumer] Starting...")
    while True:
        item = queue.get()
        if item is None:  # Sentinel value
            break
        print(f"[Consumer] Consumed: {item}")
        time.sleep(0.2)
    print(f"[Consumer] Done")


def queue_communication():
    """
    Demonstrates inter-process communication using Queue.
    """
    print("\n=== Process Communication with Queue ===")

    queue: multiprocessing.Queue = multiprocessing.Queue()
    items = [1, 2, 3, 4, 5]

    # Create producer and consumer processes
    prod = multiprocessing.Process(target=producer, args=(queue, items))
    cons = multiprocessing.Process(target=consumer, args=(queue,))

    # Start both processes
    prod.start()
    cons.start()

    # Wait for both to complete
    prod.join()
    cons.join()

    print("Communication completed")


# 5. Using Pool.apply_async for non-blocking results
def slow_square(x: int) -> int:
    """
    A slow function that squares a number.

    Args:
        x: Number to square

    Returns:
        Square of x
    """
    time.sleep(0.5)
    return x * x


def async_pool_example():
    """
    Demonstrates non-blocking pool operations with apply_async.
    """
    print("\n=== Async Pool Operations ===")
    start = time.time()

    with multiprocessing.Pool(processes=4) as pool:
        # Submit tasks asynchronously
        results = [pool.apply_async(slow_square, (i,)) for i in range(8)]

        # Do other work while tasks are running
        print("Tasks submitted, doing other work...")
        time.sleep(0.2)

        # Get results (will block until each result is ready)
        output = [result.get() for result in results]

    elapsed = time.time() - start
    print(f"Results: {output}")
    print(f"Completed in {elapsed:.2f}s")


# 6. Process Pool with different worker counts
def compare_worker_counts():
    """
    Compares performance with different numbers of worker processes.
    """
    print("\n=== Comparing Worker Counts ===")

    numbers = [8_000_000] * 8  # 8 identical tasks

    for num_workers in [1, 2, 4, 8]:
        start = time.time()

        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.map(process_number, numbers)

        elapsed = time.time() - start
        print(f"Workers: {num_workers}, Time: {elapsed:.2f}s")


# Main entry point
def main():
    """
    Main function that runs all multiprocessing demonstrations.
    """
    print("=" * 60)
    print("MULTIPROCESSING BASICS - True Parallelism in Python")
    print("=" * 60)

    basic_multiprocessing()
    pool_example()

    print("\n--- Sequential vs Parallel Comparison ---")
    sequential_computation()
    parallel_computation()

    queue_communication()
    async_pool_example()
    compare_worker_counts()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("- Multiprocessing is best for CPU-bound tasks")
    print("- Each process has its own memory space (no shared state)")
    print("- Bypasses the GIL for true parallelism")
    print("- Higher overhead than threading (process creation cost)")
    print("- Use Pool for easy distribution of work")
    print("=" * 60)


if __name__ == "__main__":
    # Required for Windows compatibility
    multiprocessing.freeze_support()
    main()
