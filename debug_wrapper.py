#!/usr/bin/env python3
"""
Simple wrapper script to run any Python script with self-debugging enabled.

Usage:
    python debug_wrapper.py your_script.py [args...]
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from self_debug_cli import main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_wrapper.py <script.py> [args...]")
        print("Example: python debug_wrapper.py my_script.py arg1 arg2")
        sys.exit(1)
    
    # Remove the wrapper script name from argv
    sys.argv = sys.argv[1:]
    
    # Run the main CLI function
    main() 