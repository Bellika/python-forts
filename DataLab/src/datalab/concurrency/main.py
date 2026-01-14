"""
Main entry point for Concurrency demonstrations.

This script provides an interactive menu to run different concurrency examples.
"""

import sys


def print_menu():
    """Prints the main menu."""
    print("\n" + "=" * 60)
    print("Python Concurrency Demonstrations")
    print("=" * 60)
    print("\n1. Asyncio Basics")
    print("2. Threading Basics")
    print("3. Multiprocessing Basics")
    print("4. Comparison (All Three Approaches)")
    print("5. Run All Demonstrations")
    print("0. Exit")
    print("\n" + "=" * 60)


def run_asyncio():
    """Runs asyncio demonstrations."""
    print("\n>>> Running Asyncio Basics...\n")
    from . import asyncio_basics
    import asyncio
    asyncio.run(asyncio_basics.main())


def run_threading():
    """Runs threading demonstrations."""
    print("\n>>> Running Threading Basics...\n")
    from . import threading_basics
    threading_basics.main()


def run_multiprocessing():
    """Runs multiprocessing demonstrations."""
    print("\n>>> Running Multiprocessing Basics...\n")
    from . import multiprocessing_basics
    multiprocessing_basics.main()


def run_comparison():
    """Runs comparison demonstrations."""
    print("\n>>> Running Comparison...\n")
    from . import comparison
    comparison.main()


def run_all():
    """Runs all demonstrations."""
    print("\n" + "=" * 60)
    print("Running All Demonstrations")
    print("=" * 60)

    run_asyncio()
    input("\nPress Enter to continue to Threading...")

    run_threading()
    input("\nPress Enter to continue to Multiprocessing...")

    run_multiprocessing()
    input("\nPress Enter to continue to Comparison...")

    run_comparison()

    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


def main():
    """Main entry point with interactive menu."""
    while True:
        print_menu()

        try:
            choice = input("Enter your choice (0-5): ").strip()

            if choice == "1":
                run_asyncio()
            elif choice == "2":
                run_threading()
            elif choice == "3":
                run_multiprocessing()
            elif choice == "4":
                run_comparison()
            elif choice == "5":
                run_all()
            elif choice == "0":
                print("\nExiting. Thank you!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please enter a number between 0 and 5.")

            input("\nPress Enter to return to menu...")

        except KeyboardInterrupt:
            print("\n\nExiting. Thank you!")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # Windows compatibility
    main()
