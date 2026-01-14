"""
Asyncio Basics - Asynchronous Programming in Python

This module demonstrates the fundamentals of asyncio for I/O-bound tasks.
Asyncio uses cooperative multitasking with a single thread.
"""

import asyncio
import time


# 1. Basic async function (coroutine)
async def greet(name: str, delay: float) -> str:
    """
    An async function that simulates an I/O operation with a delay.

    Args:
        name: Name to greet
        delay: Simulated I/O delay in seconds

    Returns:
        Greeting message
    """
    print(f"[asyncio] Starting greeting for {name}...")
    await asyncio.sleep(delay)  # Simulates I/O operation (non-blocking)
    message = f"Hello, {name}!"
    print(f"[asyncio] Completed greeting for {name}")
    return message


# 2. Running multiple coroutines concurrently
async def greet_multiple():
    """
    Demonstrates running multiple coroutines concurrently using asyncio.gather().
    All greetings run concurrently in a single thread.
    """
    print("\n=== Running Multiple Coroutines ===")
    start = time.time()

    # asyncio.gather() runs coroutines concurrently
    results = await asyncio.gather(
        greet("Alice", 2),
        greet("Bob", 1),
        greet("Charlie", 1.5)
    )

    elapsed = time.time() - start
    print(f"Results: {results}")
    print(f"Total time: {elapsed:.2f}s (concurrent, not sequential!)")


# 3. Async with sequential execution
async def greet_sequential():
    """
    Demonstrates sequential execution of async functions.
    Each await waits for the previous one to complete.
    """
    print("\n=== Sequential Execution ===")
    start = time.time()

    # Each await blocks until the coroutine completes
    result1 = await greet("Alice", 2)
    result2 = await greet("Bob", 1)
    result3 = await greet("Charlie", 1.5)

    elapsed = time.time() - start
    print(f"Results: {[result1, result2, result3]}")
    print(f"Total time: {elapsed:.2f}s (sequential)")


# 4. Practical example: Simulated API calls
async def fetch_user_data(user_id: int) -> dict:
    """
    Simulates fetching user data from an API.
    In real scenarios, this would be an HTTP request.
    """
    print(f"[asyncio] Fetching data for user {user_id}...")
    await asyncio.sleep(1)  # Simulate network delay
    return {"id": user_id, "name": f"User{user_id}", "active": True}


async def fetch_all_users():
    """
    Fetches multiple user records concurrently.
    This is much faster than fetching them one by one.
    """
    print("\n=== Fetching Multiple Users ===")
    start = time.time()

    user_ids = [1, 2, 3, 4, 5]

    # Create tasks for all users
    tasks = [fetch_user_data(user_id) for user_id in user_ids]

    # Run all tasks concurrently
    users = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"Fetched {len(users)} users in {elapsed:.2f}s")
    for user in users:
        print(f"  - {user}")


# 5. Using asyncio.create_task() for background tasks
async def background_task_example():
    """
    Demonstrates creating background tasks that run concurrently.
    """
    print("\n=== Background Tasks ===")

    # Create tasks (they start running immediately)
    task1 = asyncio.create_task(greet("Task1", 1))
    task2 = asyncio.create_task(greet("Task2", 2))

    print("Tasks created, doing other work...")
    await asyncio.sleep(0.5)
    print("Still doing other work...")

    # Wait for tasks to complete
    results = await asyncio.gather(task1, task2)
    print(f"Tasks completed: {results}")


# Main entry point
async def main():
    """
    Main function that runs all asyncio demonstrations.
    """
    print("=" * 60)
    print("ASYNCIO BASICS - Asynchronous Programming")
    print("=" * 60)

    # Run demonstrations
    await greet_multiple()
    await greet_sequential()
    await fetch_all_users()
    await background_task_example()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS:")
    print("- Asyncio is best for I/O-bound tasks (network, files)")
    print("- Uses a single thread with cooperative multitasking")
    print("- 'await' yields control to other coroutines")
    print("- Not suitable for CPU-bound tasks")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
