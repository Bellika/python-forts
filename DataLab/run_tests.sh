#!/bin/bash
# Simple test runner script for DataLab

echo "================================"
echo "DataLab Test Runner"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -d "tests" ]; then
    echo "Error: tests/ directory not found"
    echo "Please run this script from the DataLab directory"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Installing..."
    pip install pytest pytest-cov pytest-mock
fi

# Set PYTHONPATH to find datalab module
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Parse command line arguments
if [ "$1" == "quick" ]; then
    echo "Running quick tests (no coverage, no slow tests)..."
    pytest tests/ -v -m "not slow" --no-cov
elif [ "$1" == "coverage" ]; then
    echo "Running tests with full coverage report..."
    pytest tests/ -v --cov=src/datalab --cov-report=html --cov-report=term
    echo ""
    echo "HTML coverage report generated in htmlcov/"
    echo "Open htmlcov/index.html in a browser to view"
elif [ "$1" == "file" ]; then
    if [ -z "$2" ]; then
        echo "Usage: ./run_tests.sh file <test_file>"
        exit 1
    fi
    echo "Running tests in $2..."
    pytest "tests/$2" -v
elif [ "$1" == "help" ]; then
    echo "Usage: ./run_tests.sh [option]"
    echo ""
    echo "Options:"
    echo "  (none)      Run all tests with coverage"
    echo "  quick       Run tests quickly without coverage or slow tests"
    echo "  coverage    Run tests with detailed coverage report"
    echo "  file <name> Run specific test file"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh"
    echo "  ./run_tests.sh quick"
    echo "  ./run_tests.sh file test_statistics.py"
else
    echo "Running all tests with coverage..."
    pytest tests/ -v --cov=src/datalab --cov-report=term-missing
fi

echo ""
echo "================================"
echo "Tests complete!"
echo "================================"
