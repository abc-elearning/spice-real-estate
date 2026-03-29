"""Shared utilities for SpiceRE decision scripts.

Provides JSON output helpers, error handling, and input validation.
All scripts import from here for consistent CLI behavior.
"""

import json
import sys


def json_output(status="success", **data):
    """Print JSON to stdout with status and all kwargs."""
    result = {"status": status, **data}
    print(json.dumps(result))


def json_error(message):
    """Print error JSON to stdout and exit with code 1."""
    print(json.dumps({"status": "error", "message": message}))
    sys.exit(1)


def validate_positive(name, value):
    """Exit with error if value is not positive."""
    if value <= 0:
        json_error(f"{name} must be positive")


def validate_range(name, value, min_val, max_val):
    """Exit with error if value is outside [min_val, max_val]."""
    if value < min_val or value > max_val:
        json_error(f"{name} must be between {min_val} and {max_val}")


def validate_choice(name, value, choices):
    """Exit with error if value is not in the allowed choices."""
    if value not in choices:
        json_error(f"{name} must be one of {choices}")
