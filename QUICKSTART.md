# Quick Start Guide 🚀

Get up and running with the Self-Debugging CLI Tool in 5 minutes!

## 1. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

## 2. Set Up OpenAI API Key

```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

## 3. Test the Installation

```bash
# Run the demo script
python test_demo.py
```

## 4. Use with Your Own Code

### Option A: Decorator Method
```python
from self_debug_cli import self_debug

@self_debug
def my_function():
    # Your code here
    result = 10 / 0  # This will trigger GPT-4 analysis
    return result

my_function()
```

### Option B: CLI Method
```bash
# Run any Python script with self-debugging
python self_debug_cli.py your_script.py

# Or use the wrapper
python debug_wrapper.py your_script.py
```

## 5. What You'll See

When an error occurs, you'll get:
- 🚨 Error notification
- 🔍 GPT-4 analysis with explanation
- 💡 Suggested fixes
- 🎯 Confidence level
- ❓ Option to apply the fix

## Common Issues

**"OpenAI package not installed"**
```bash
pip install openai
```

**"OPENAI_API_KEY not set"**
- Check your `.env` file
- Make sure the API key is valid

**"Error calling GPT-4"**
- Check your internet connection
- Verify your API key has credits

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try the [examples](examples/) for more complex scenarios
- Customize the tool for your specific needs

Happy debugging! 🐛✨ 