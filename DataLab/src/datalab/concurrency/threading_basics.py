"""
Threading Basics - Multithreading in Python

This module demonstrates threading for I/O-bound tasks.
Python threads run in parallel but are limited by the GIL (Global Interpreter Lock).
"""

import threading
import time
from typing import List


# 1. Basic thread creation and execution
def worker(name: str, duration: float):
    """
    A simple worker function that simulates work with a delay.

    Args:
        name: Worker name
        duration: Time to sleep (simulating I/O work)
    """
    print(f"[Thread {name}] Starting work...")
    time.sleep(duration)
    print(f"[Thread {name}] Finished work after {duration}s")


def basic_threading():
    """
    Demonstrates creating and starting threads manually.
    """
    print("\n=== Basic Threading ===")
    start = time.time()

    # Create threads
    thread1 = threading.Thread(target=worker, args=("A", 2))
    thread2 = threading.Thread(target=worker, args=("B", 1))
    thread3 = threading.Thread(target=worker, args=("C", 1.5))

    # Start threads (they run in parallel)
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    elapsed = time.time() - start
    print(f"All threads completed in {elapsed:.2f}s")


# 2. Race condition demonstration (UNSAFE)
counter = 0


def increment_unsafe(n: int):
    """
    Increments the global counter WITHOUT thread safety.
    This demonstrates a race condition.
    """
    global counter
    for _ in range(n):
        # This is NOT atomic! It's actually three operations:
        # 1. Read counter
        # 2. Add 1
        # 3. Write back
        counter += 1


def race_condition_demo():
    """
    Demonstrates a race condition where threads interfere with each other.
    """
    global counter
    print("\n=== Race Condition (UNSAFE) ===")

    counter = 0
    threads: List[threading.Thread] = []
    num_threads = 5
    increments_per_thread = 100000

    start = time.time()

    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(target=increment_unsafe, args=(increments_per_thread,))
        threads.append(thread)
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    elapsed = time.time() - start
    expected = num_threads * increments_per_thread
    print(f"Expected: {expected}")
    print(f"Actual: {counter}")
    print(f"Lost updates: {expected - counter}")
    print(f"Time: {elapsed:.2f}s")


# 3. Thread-safe counter with Lock
counter_safe = 0
counter_lock = threading.Lock()


def increment_safe(n: int):
    """
    Increments the global counter WITH thread safety using a Lock.
    """
    global counter_safe
    for _ in range(n):
        with counter_lock:  # Only one thread can execute this block at a time
            counter_safe += 1


def thread_safe_demo():
    """
    Demonstrates thread-safe operations using a Lock.
    """
    global counter_safe
    print("\n=== Thread-Safe Counter ===")

    counter_safe = 0
    threads: List[threading.Thread] = []
    num_threads = 5
    increments_per_thread = 100000

    start = time.time()

    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(target=increment_safe, args=(increments_per_thread,))
        threads.append(thread)
        thread.start()

    # Wait for all threads
    for thread in threads:
        thread.join()

    elapsed = time.time() - start
    expected = num_threads * increments_per_thread
    print(f"Expected: {expected}")
    print(f"Actual: {counter_safe}")
    print(f"Lost updates: {expected - counter_safe}")
    print(f"Time: {elapsed:.2f}s (slower due to lock overhead)")


# 4. Practical example: Parallel file downloads (simulated)
def download_file(file_id: int, lock: threading.Lock, results: list):
    """
    Simulates downloading a file.

    Args:
        file_id: File identifier
        lock: Lock for thread-safe access to results
        results: Shared list to store results
    """
    print(f"[Thread] Downloading file {file_id}...")
    time.sleep(1)  # Simulate download time

    # Thread-safe append to shared list
    with lock:
        results.append(f"file_{file_id}.dat")

    print(f"[Thread] Downloaded file {file_id}")


def parallel_downloads():
    """
    Demonstrates parallel downloads using threads.
    """
    print("\n=== Parallel File Downloads ===")

    results: List[str] = []
    results_lock = threading.Lock()
    threads: List[threading.Thread] = []

    start = time.time()

    # Start 5 download threads
    for file_id in range(1, 6):
        thread = threading.Thread(target=download_file, args=(file_id, results_lock, results))
        threads.append(thread)
        thread.start()

    # Wait for all downloads
    for thread in threads:
        thread.join()

    elapsed = time.time() - start
    print(f"Downloaded {len(results)} files in {elapsed:.2f}s")
    print(f"Files: {results}")


# 5. Thread with return value using a class
class WorkerThread(threading.Thread):
    """
    Custom thread class that can return a value.
    """

    def __init__(self, task_id: int, duration: float):
        super().__init__()
        self.task_id = task_id
        self.duration = duration
        self.result = None

    def run(self):
        """
        The method that runs when thread.start() is called.
        """
        print(f"[WorkerThread {self.task_id}] Processing...")
        time.sleep(self.duration)
        self.result = f"Task {self.task_id} completed"
        print(f"[WorkerThread {self.task_id}] Done")


def custom_thread_class():
    """
    Demonstrates using a custom Thread subclass.
    """
    print("\n=== Custom Thread Class ===")

    threads = [WorkerThread(i, 1) for i in range(3)]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait and collect results
    for thread in threads:
        thread.join()
        print(f"Result: {thread.result}")


# Main entry point
def main():
    """
    Main function that runs all threading demonstrations.
    """
    print("=" * 60)
    print("THREADING BASICS - Multithreading in Python")
    print("=" * 60)

    basic_threading()
    race_condition_demo()
    thread_safe_demo()
    parallel_downloads()
    custom_thread_class()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("- Threading is good for I/O-bound tasks")
    print("- GIL prevents true parallelism for CPU-bound tasks")
    print("- Always use locks for shared mutable state")
    print("- Race conditions are subtle and dangerous")
    print("=" * 60)


if __name__ == "__main__":
    main()
