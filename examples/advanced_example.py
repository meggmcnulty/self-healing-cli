#!/usr/bin/env python3
"""
Advanced example demonstrating the self-debugging CLI tool.

This script shows more complex scenarios including:
- Database connection errors
- API call failures
- Configuration issues
- Data processing errors
"""

import json
import requests
from datetime import datetime
from self_debug_cli import self_debug


@self_debug
def fetch_user_data(user_id):
    """Fetch user data from an API - will fail with connection error."""
    # Simulate API call to non-existent endpoint
    response = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
    response.raise_for_status()
    return response.json()


@self_debug
def process_json_data(json_string):
    """Process JSON data - will fail with malformed JSON."""
    data = json.loads(json_string)
    return data["name"]


@self_debug
def calculate_statistics(numbers):
    """Calculate statistics - will fail with empty list."""
    if not numbers:
        raise ValueError("Cannot calculate statistics on empty list")
    
    return {
        "mean": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "count": len(numbers)
    }


@self_debug
def validate_config(config):
    """Validate configuration - will fail with missing required fields."""
    required_fields = ["api_key", "base_url", "timeout"]
    
    for field in required_fields:
        if field not in config:
            raise KeyError(f"Missing required configuration field: {field}")
    
    if not config["api_key"]:
        raise ValueError("API key cannot be empty")
    
    return True


@self_debug
def format_date(date_string, format_spec="%Y-%m-%d"):
    """Format date string - will fail with invalid date format."""
    return datetime.strptime(date_string, format_spec).strftime("%B %d, %Y")


@self_debug
def database_query(query, connection_params):
    """Simulate database query - will fail with connection issues."""
    # Simulate database connection failure
    if connection_params.get("host") == "invalid_host":
        raise ConnectionError("Could not connect to database server")
    
    if connection_params.get("port") == 5432:
        raise Exception("PostgreSQL server is down")
    
    # Simulate successful query
    return {"status": "success", "rows": 5}


def main():
    """Main function to demonstrate advanced error scenarios."""
    print("🚀 Self-Debugging CLI Tool - Advanced Example")
    print("=" * 55)
    
    # Example 1: API call failure
    print("\n1. Testing API call failure...")
    try:
        result = fetch_user_data(123)
        print(f"User data: {result}")
    except Exception as e:
        print(f"API call failed: {e}")
    
    # Example 2: JSON parsing error
    print("\n2. Testing JSON parsing error...")
    try:
        malformed_json = '{"name": "John", "age": 30,}'  # Trailing comma
        result = process_json_data(malformed_json)
        print(f"Processed data: {result}")
    except Exception as e:
        print(f"JSON processing failed: {e}")
    
    # Example 3: Statistics calculation with empty data
    print("\n3. Testing statistics calculation...")
    try:
        result = calculate_statistics([])
        print(f"Statistics: {result}")
    except Exception as e:
        print(f"Statistics calculation failed: {e}")
    
    # Example 4: Configuration validation
    print("\n4. Testing configuration validation...")
    try:
        invalid_config = {
            "api_key": "",  # Empty API key
            "base_url": "https://api.example.com"
            # Missing timeout field
        }
        result = validate_config(invalid_config)
        print(f"Config validation: {result}")
    except Exception as e:
        print(f"Config validation failed: {e}")
    
    # Example 5: Date formatting error
    print("\n5. Testing date formatting...")
    try:
        result = format_date("2023-13-45")  # Invalid date
        print(f"Formatted date: {result}")
    except Exception as e:
        print(f"Date formatting failed: {e}")
    
    # Example 6: Database connection error
    print("\n6. Testing database connection...")
    try:
        connection_params = {"host": "invalid_host", "port": 5432}
        result = database_query("SELECT * FROM users", connection_params)
        print(f"Database result: {result}")
    except Exception as e:
        print(f"Database query failed: {e}")
    
    print("\n✅ All advanced examples completed!")


if __name__ == "__main__":
    main() 