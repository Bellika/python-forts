"""
Entry point for running DataLab as a module.

This file enables:
    python -m datalab

It's a standard Python pattern for making packages executable.
"""

from datalab.main import run

if __name__ == "__main__":
    run()
