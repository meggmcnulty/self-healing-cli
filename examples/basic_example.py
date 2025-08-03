#!/usr/bin/env python3
"""
Basic example demonstrating the self-debugging CLI tool.

This script contains intentional errors to showcase the debugging capabilities.
"""

from self_debug_cli import self_debug


@self_debug
def divide_numbers(a, b):
    """Divide two numbers - will fail with division by zero."""
    return a / b


@self_debug
def access_list_element(lst, index):
    """Access a list element - will fail with index out of range."""
    return lst[index]


@self_debug
def open_nonexistent_file(filename):
    """Open a file - will fail with file not found."""
    with open(filename, 'r') as f:
        return f.read()


@self_debug
def call_undefined_function():
    """Call an undefined function - will fail with NameError."""
    return undefined_function()


@self_debug
def process_data(data):
    """Process data with potential type errors."""
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, list):
        return sum(data)
    else:
        # This will cause an AttributeError for some types
        return data.nonexistent_method()


def main():
    """Main function to demonstrate various error scenarios."""
    print("🧪 Self-Debugging CLI Tool - Basic Example")
    print("=" * 50)
    
    # Example 1: Division by zero
    print("\n1. Testing division by zero...")
    try:
        result = divide_numbers(10, 0)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught: {e}")
    
    # Example 2: Index out of range
    print("\n2. Testing index out of range...")
    try:
        result = access_list_element([1, 2, 3], 10)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught: {e}")
    
    # Example 3: File not found
    print("\n3. Testing file not found...")
    try:
        result = open_nonexistent_file("nonexistent_file.txt")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught: {e}")
    
    # Example 4: NameError
    print("\n4. Testing undefined function...")
    try:
        result = call_undefined_function()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught: {e}")
    
    # Example 5: AttributeError
    print("\n5. Testing attribute error...")
    try:
        result = process_data(42)  # int has no 'nonexistent_method'
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught: {e}")
    
    print("\n✅ All examples completed!")


if __name__ == "__main__":
    main() 