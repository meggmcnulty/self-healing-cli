# Self-Debugging CLI Tool 

A powerful CLI template that wraps any Python function and, on error, automatically invokes GPT-4 to explain the traceback and suggest fixes.  

## Features 

- **Automatic Error Analysis**: When a function fails, GPT-4 automatically analyzes the error and provides detailed explanations
- **Smart Fix Suggestions**: Get specific code fixes and workarounds for common Python errors
- **Rich Terminal Output**: Beautiful, formatted output with syntax highlighting and panels
- **Easy Integration**: Simple decorator-based approach - just add `@self_debug` to any function
- **Flexible Configuration**: Environment-based configuration with fallback options
- **CLI Interface**: Run any Python script with self-debugging enabled

## Installation 

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd self-healing-cli
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env and add your OpenAI API key
   # Get your key from: https://platform.openai.com/api-keys
   ```

## Quick Start 

### Method 1: Using the Decorator

```python
from self_debug_cli import self_debug

@self_debug
def my_function():
    # Your code here
    result = 10 / 0  # This will trigger the debugger
    return result

# Run your function normally
my_function()
```

### Method 2: Using the CLI Tool

```bash
# Run any Python script with self-debugging enabled
python self_debug_cli.py --debug your_script.py

# Or with custom API key
python self_debug_cli.py --api-key your_key your_script.py
```

## Examples 

### Basic Example

```python
from self_debug_cli import self_debug

@self_debug
def divide_numbers(a, b):
    return a / b

# This will trigger GPT-4 analysis when b = 0
result = divide_numbers(10, 0)
```

### Advanced Example

```python
from self_debug_cli import self_debug
import requests

@self_debug
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# This will analyze connection errors, HTTP errors, etc.
data = fetch_data("https://invalid-url.com")
```

## Configuration ⚙️

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `SELF_DEBUG_MODE` | Enable/disable debugging | `true` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |

### Command Line Options

```bash
python self_debug_cli.py [OPTIONS] SCRIPT [ARGS]...

Options:
  --api-key TEXT     OpenAI API key
  --debug / --no-debug  Enable/disable self-debugging [default: True]
  --help            Show this message and exit
```

## How It Works 🔧

1. **Function Wrapping**: The `@self_debug` decorator wraps your function with error handling
2. **Error Detection**: When an exception occurs, the tool captures the full context
3. **GPT-4 Analysis**: The error, traceback, and function source code are sent to GPT-4
4. **Smart Analysis**: GPT-4 provides:
   - Clear explanation of what went wrong
   - Root cause analysis
   - Specific code fixes
   - Confidence level
   - Additional helpful notes
5. **Rich Display**: Results are displayed in beautiful, formatted panels
6. **User Choice**: You can choose to apply the suggested fix or handle it manually

## Example Output 📊

When an error occurs, you'll see output like this:

```
🚨 Error occurred!
Function: divide_numbers
Error: ZeroDivisionError: division by zero

🔍 GPT-4 Analysis

┌─ Explanation ──────────────────────────────────────────────┐
│ The error occurs because you're trying to divide by zero.  │
│ In Python, division by zero is not allowed and raises a    │
│ ZeroDivisionError.                                          │
└─────────────────────────────────────────────────────────────┘

┌─ Root Cause ───────────────────────────────────────────────┐
│ The variable 'b' has a value of 0, which causes the        │
│ division operation to fail.                                 │
└─────────────────────────────────────────────────────────────┘

┌─ Suggested Fix ────────────────────────────────────────────┐
│ def divide_numbers(a, b):                                  │
│     if b == 0:                                             │
│         raise ValueError("Cannot divide by zero")          │
│     return a / b                                           │
└─────────────────────────────────────────────────────────────┘

Confidence: high

Would you like to apply the suggested fix? [y/N]:
```

## Advanced Usage 🎯

### Custom Error Handling

```python
from self_debug_cli import debug_cli

# Custom error handler
def custom_error_handler(error, func, args, kwargs):
    print(f"Custom handling for {error}")
    # Your custom logic here

# Override the default handler
debug_cli._handle_error = custom_error_handler
```

### Batch Processing

```python
from self_debug_cli import self_debug

@self_debug
def process_items(items):
    results = []
    for item in items:
        # Each error will be analyzed individually
        result = process_single_item(item)
        results.append(result)
    return results
```

## Error Types Supported 🛠️

The tool can analyze and provide fixes for:

- **Syntax Errors**: Missing colons, parentheses, etc.
- **Name Errors**: Undefined variables and functions
- **Type Errors**: Incorrect data types
- **Attribute Errors**: Missing methods and attributes
- **Index Errors**: Out of range access
- **Key Errors**: Missing dictionary keys
- **Value Errors**: Invalid values
- **File Errors**: File not found, permission issues
- **Network Errors**: Connection timeouts, HTTP errors
- **Import Errors**: Missing modules
- **And many more...**

## Best Practices 💡

1. **Use Sparingly**: Don't decorate every function - focus on critical paths
2. **Handle Expected Errors**: Use try/catch for expected errors, let the tool handle unexpected ones
3. **Review Suggestions**: Always review GPT-4 suggestions before applying
4. **Environment Setup**: Keep your `.env` file secure and never commit API keys
5. **Testing**: Test your functions with the debugger disabled in production

## Troubleshooting 🔧

### Common Issues

1. **"OpenAI package not installed"**
   ```bash
   pip install openai
   ```

2. **"OPENAI_API_KEY not set"**
   - Check your `.env` file
   - Verify the API key is valid
   - Ensure the environment variable is loaded

3. **"Error calling GPT-4"**
   - Check your internet connection
   - Verify your API key has sufficient credits
   - Check OpenAI service status

### Debug Mode

```bash
# Disable debugging temporarily
export SELF_DEBUG_MODE=false

# Or use command line
python self_debug_cli.py --no-debug your_script.py
```

## Contributing 

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License 

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 
- Terminal output powered by [Rich](https://rich.readthedocs.io/)
- CLI framework by [Click](https://click.palletsprojects.com/)

---

**Happy Debugging! 🐛✨** 
