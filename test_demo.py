#!/usr/bin/env python3
"""
Simple test script to demonstrate the self-debugging CLI tool.

This script can be run directly to see the tool in action.
"""

from self_debug_cli import self_debug


@self_debug
def simple_division(a, b):
    """Simple division function that will fail with division by zero."""
    return a / b


@self_debug
def list_access(my_list, index):
    """Access list element - will fail with index out of range."""
    return my_list[index]


@self_debug
def string_operation(text):
    """String operation that will fail with AttributeError."""
    return text.upper().lower().capitalize().nonexistent_method()


def main():
    """Main function to demonstrate the self-debugging tool."""
    print("🧪 Self-Debugging CLI Tool Demo")
    print("=" * 40)
    
    # Test 1: Division by zero
    print("\n1. Testing division by zero...")
    try:
        result = simple_division(10, 0)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error caught: {e}")
    
    # Test 2: Index out of range
    print("\n2. Testing index out of range...")
    try:
        result = list_access([1, 2, 3], 10)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error caught: {e}")
    
    # Test 3: Attribute error
    print("\n3. Testing attribute error...")
    try:
        result = string_operation("hello world")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error caught: {e}")
    
    print("\n✅ Demo completed!")
    print("\n💡 Tip: If you have an OpenAI API key set up, you should see")
    print("   detailed GPT-4 analysis for each error above.")


if __name__ == "__main__":
    main() 