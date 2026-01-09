"""
Security module for DataLab.

Demonstrates common security vulnerabilities and how to prevent them:
- Input validation and sanitization
- Path traversal attacks
- Command injection
- XSS (Cross-Site Scripting)
- Safe data handling

This module contains BOTH vulnerable and secure examples for teaching purposes.
"""

import html
import json
import os
import subprocess
from pathlib import Path

from datalab import config
from datalab.utils import log, warning

# ============================================================================
# 1. PATH TRAVERSAL ATTACKS
# ============================================================================


def load_file_unsafe(filename):
    """
    VULNERABLE: Path traversal attack possible!

    An attacker could provide: '../../../etc/passwd'
    This would read files outside the data directory.

    Args:
        filename: User-provided filename

    Returns:
        File contents

    Example attack:
        load_file_unsafe('../../../etc/passwd')
    """
    # DANGER: No validation of user input!
    filepath = f"data/{filename}"

    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"


def load_file_safe(filename):
    """
    SECURE: Path traversal prevented with validation.

    Uses Path.resolve() to get absolute path and validates
    that it's within the allowed directory.

    Args:
        filename: User-provided filename

    Returns:
        File contents

    Raises:
        ValueError: If path is outside allowed directory
    """
    # Get absolute path to data directory
    base_dir = config.DATA_DIR.resolve()

    # Resolve the requested file path
    requested_path = (base_dir / filename).resolve()

    # Check if the resolved path is inside base_dir
    if not requested_path.is_relative_to(base_dir):
        raise ValueError(f"Access denied: Path outside data directory")

    # Check if file exists
    if not requested_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    # Safe to read
    with open(requested_path, "r") as f:
        return f.read()


# ============================================================================
# 2. COMMAND INJECTION
# ============================================================================


def run_command_unsafe(user_input):
    """
    VULNERABLE: Command injection possible!

    Never use os.system() or shell=True with user input.

    Args:
        user_input: User-provided command argument

    Example attack:
        run_command_unsafe("data.json; rm -rf /")
        This would delete files!
    """
    # DANGER: User input directly in shell command
    command = f"{user_input}"

    warning("UNSAFE: Executing command with user input!")
    result = os.system(command)

    return result


def run_command_safe(filename):
    """
    SECURE: Using subprocess with argument list.

    Never uses shell=True, passes arguments as list.

    Args:
        filename: Filename to count lines in

    Returns:
        Number of lines
    """
    # Validate filename first
    base_dir = config.DATA_DIR.resolve()
    filepath = (base_dir / filename).resolve()

    if not filepath.is_relative_to(base_dir):
        raise ValueError("Invalid file path")

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    # Safe: Arguments passed as list, no shell interpretation
    result = subprocess.run(
        ["wc", "-l", str(filepath)], capture_output=True, text=True, timeout=5
    )

    return result.stdout.strip()


# ============================================================================
# 3. EVAL/EXEC INJECTION
# ============================================================================


def filter_data_unsafe(data, filter_expression):
    """
    VULNERABLE: Code injection via eval()!

    Never use eval() or exec() with user input.

    Args:
        data: List of records
        filter_expression: User-provided filter (e.g., "age > 25")

    Example attack:
        filter_data_unsafe(data, "__import__('os').system('rm -rf /')")
    """
    # DANGER: eval() executes arbitrary code!
    warning("UNSAFE: Using eval() with user input!")

    filtered = []
    for record in data:
        try:
            # This allows arbitrary code execution!
            if eval(filter_expression, {"record": record}):
                filtered.append(record)
        except Exception as e:
            warning(f"Filter error: {e}")

    return filtered


def filter_data_safe(data, field, operator, value):
    """
    SECURE: Structured filtering without eval().

    Only allows predefined operators, validates inputs.

    Args:
        data: List of records
        field: Field name to filter on
        operator: One of: '>', '<', '==', '!='
        value: Value to compare against

    Returns:
        Filtered list
    """
    # Whitelist of allowed operators
    allowed_operators = {
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
    }

    if operator not in allowed_operators:
        raise ValueError(f"Invalid operator. Allowed: {list(allowed_operators.keys())}")

    filtered = []
    for record in data:
        if field not in record:
            continue

        try:
            # Safe comparison using predefined operators
            if allowed_operators[operator](record[field], value):
                filtered.append(record)
        except (TypeError, KeyError):
            continue

    return filtered


# ============================================================================
# 4. XSS (Cross-Site Scripting) Prevention
# ============================================================================


def generate_html_report_unsafe(records):
    """
    VULNERABLE: XSS attack possible!

    If record data contains <script> tags or other HTML,
    it will be executed in the browser.

    Args:
        records: List of data records

    Returns:
        HTML string

    Example attack:
        Record with name: "<script>alert('XSS')</script>"
    """
    # DANGER: No HTML escaping!
    html_output = "<html><head><title>Report</title></head><body>\n"
    html_output += "<h1>Data Report</h1>\n"
    html_output += "<table border='1'>\n"
    html_output += "<tr><th>Name</th><th>Age</th></tr>\n"

    for record in records:
        # User data inserted directly into HTML!
        html_output += f"<tr><td>{record.get('name', 'N/A')}</td>"
        html_output += f"<td>{record.get('age', 'N/A')}</td></tr>\n"

    html_output += "</table>\n</body></html>"

    return html_output


def generate_html_report_safe(records):
    """
    SECURE: HTML escaped to prevent XSS.

    Uses html.escape() to convert special characters.

    Args:
        records: List of data records

    Returns:
        HTML string with escaped content
    """
    html_output = "<html><head><title>Report</title></head><body>\n"
    html_output += "<h1>Data Report</h1>\n"
    html_output += "<table border='1'>\n"
    html_output += "<tr><th>Name</th><th>Age</th></tr>\n"

    for record in records:
        # Safe: HTML special characters are escaped
        safe_name = html.escape(str(record.get("name", "N/A")))
        safe_age = html.escape(str(record.get("age", "N/A")))

        html_output += f"<tr><td>{safe_name}</td>"
        html_output += f"<td>{safe_age}</td></tr>\n"

    html_output += "</table>\n</body></html>"

    return html_output


# ============================================================================
# 5. INPUT VALIDATION
# ============================================================================


def parse_json_unsafe(json_string):
    """
    VULNERABLE: No validation of JSON structure.

    Could cause unexpected errors or security issues
    if the JSON structure is not what we expect.

    Args:
        json_string: JSON string from user

    Returns:
        Parsed data
    """
    # DANGER: No validation, assumes structure is correct
    data = json.loads(json_string)

    # Directly access fields without checking
    return data["records"]


def parse_json_safe(json_string, max_size=1024 * 1024):
    """
    SECURE: Validates JSON structure and size.

    Checks:
    - Size limit
    - Valid JSON syntax
    - Expected structure
    - Data types

    Args:
        json_string: JSON string from user
        max_size: Maximum allowed size in bytes

    Returns:
        Validated and parsed data

    Raises:
        ValueError: If validation fails
    """
    # Check size to prevent DoS
    if len(json_string) > max_size:
        raise ValueError(f"JSON too large (max {max_size} bytes)")

    # Parse JSON
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    # Validate structure
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object")

    if "records" not in data:
        raise ValueError("JSON must contain 'records' field")

    if not isinstance(data["records"], list):
        raise ValueError("'records' must be a list")

    # Validate each record
    for i, record in enumerate(data["records"]):
        if not isinstance(record, dict):
            raise ValueError(f"Record {i} must be an object")

        # Validate required fields
        if "name" in record and not isinstance(record["name"], str):
            raise ValueError(f"Record {i}: 'name' must be a string")

        if "age" in record and not isinstance(record["age"], (int, float)):
            raise ValueError(f"Record {i}: 'age' must be a number")

    return data["records"]


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================


def demo_path_traversal():
    """Demonstrate path traversal vulnerability and fix."""
    print("\n" + "=" * 60)
    print("PATH TRAVERSAL ATTACK DEMO")
    print("=" * 60)

    # Safe example
    print("\n1. SAFE: Loading legitimate file")
    try:
        content = load_file_safe("data.json")
        print(f"Success! Loaded {len(content)} bytes")
    except Exception as e:
        print(f"Error: {e}")

    # Attack example
    print("\n2. UNSAFE: Attempting path traversal attack")
    malicious_path = "../../../etc/passwd"
    print(f"Trying to load: {malicious_path}")

    try:
        content = load_file_safe(malicious_path)
        print("DANGER: Attack succeeded!")
    except ValueError as e:
        print(f"BLOCKED: {e}")


def demo_command_injection():
    """Demonstrate command injection vulnerability."""
    print("\n" + "=" * 60)
    print("COMMAND INJECTION DEMO")
    print("=" * 60)

    print("\n1. SAFE: Counting lines in data.json")
    try:
        result = run_command_safe("data.json")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n2. UNSAFE would allow: 'data.json; rm -rf /'")
    print("   (Not executing this for safety!)")


def demo_xss():
    """Demonstrate XSS vulnerability and fix."""
    print("\n" + "=" * 60)
    print("XSS (Cross-Site Scripting) DEMO")
    print("=" * 60)

    # Malicious data
    malicious_records = [
        {"name": "Alice", "age": 25},
        {"name": "<script>alert('XSS')</script>", "age": 30},
        {"name": "Bob", "age": 22},
    ]

    print("\n1. UNSAFE HTML (would execute script in browser):")
    unsafe_html = generate_html_report_unsafe(malicious_records)
    print(unsafe_html[:200] + "...")
    print("\nNotice: Script tag is present in HTML!")

    print("\n2. SAFE HTML (script escaped):")
    safe_html = generate_html_report_safe(malicious_records)
    print(safe_html[:200] + "...")
    print("\nNotice: Script tag is escaped (&lt;script&gt;)")


def demo_eval_injection():
    """Demonstrate eval injection vulnerability."""
    print("\n" + "=" * 60)
    print("EVAL INJECTION DEMO")
    print("=" * 60)

    test_data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 22},
    ]

    print("\n1. SAFE: Using structured filtering")
    result = filter_data_safe(test_data, "age", ">", 24)
    print(f"Filtered records (age > 24): {result}")

    print('\n2. UNSAFE eval() would allow: \'__import__("os").system("ls")\'')
    print("   (Not executing this for safety!)")


def main():
    """Run all security demonstrations."""
    print("=" * 60)
    print("DataLab Security Module - Educational Examples")
    print("=" * 60)
    print("\nThis module demonstrates common security vulnerabilities")
    print("and how to prevent them in Python applications.")

    demo_path_traversal()
    demo_command_injection()
    demo_xss()
    demo_eval_injection()

    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("1. NEVER trust user input - always validate and sanitize")
    print("2. Use Path.resolve() and is_relative_to() for file paths")
    print("3. Avoid eval(), exec(), os.system() with user input")
    print("4. Use html.escape() for HTML output")
    print("5. Validate JSON structure and data types")
    print("6. Use subprocess with argument lists, not shell=True")
    print("=" * 60)


if __name__ == "__main__":
    main()
