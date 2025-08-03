#!/usr/bin/env python3
"""
Self-Debugging CLI Tool

A CLI template that wraps any Python function and, on error, auto-invokes GPT-4
to explain the traceback and suggest a fix.
"""

import os
import sys
import traceback
import inspect
import json
from typing import Any, Callable, Optional, Dict, List
from functools import wraps
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.prompt import Confirm
from dotenv import load_dotenv

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables
load_dotenv()

console = Console()

class SelfDebugCLI:
    """Main class for the self-debugging CLI tool."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        self.debug_mode = os.getenv("SELF_DEBUG_MODE", "true").lower() == "true"
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                console.print(f"[red]Warning: Failed to initialize OpenAI client: {e}[/red]")
        elif not OPENAI_AVAILABLE:
            console.print("[yellow]Warning: OpenAI package not installed. Install with: pip install openai[/yellow]")
        elif not self.api_key:
            console.print("[yellow]Warning: OPENAI_API_KEY not set. Set it in your environment or .env file[/yellow]")
    
    def debug_function(self, func: Callable) -> Callable:
        """
        Decorator that wraps a function with self-debugging capabilities.
        
        Args:
            func: The function to wrap
            
        Returns:
            Wrapped function with error handling
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if self.debug_mode and self.client:
                    self._handle_error(e, func, args, kwargs)
                else:
                    # Re-raise the exception if debugging is disabled or no OpenAI client
                    raise
        return wrapper
    
    def _handle_error(self, error: Exception, func: Callable, args: tuple, kwargs: dict):
        """Handle an error by analyzing it with GPT-4 and suggesting fixes."""
        console.print("\n[red]🚨 Error occurred![/red]")
        console.print(f"[red]Function: {func.__name__}[/red]")
        console.print(f"[red]Error: {type(error).__name__}: {str(error)}[/red]")
        
        # Get the full traceback
        tb = traceback.format_exc()
        
        # Get function source code if available
        try:
            source = inspect.getsource(func)
        except (OSError, TypeError):
            source = "Source code not available"
        
        # Prepare context for GPT-4
        context = self._prepare_context(error, func, args, kwargs, tb, source)
        
        # Analyze with GPT-4
        analysis = self._analyze_with_gpt4(context)
        
        if analysis:
            self._display_analysis(analysis)
            
            # Ask user if they want to apply the suggested fix
            if Confirm.ask("Would you like to apply the suggested fix?", default=False):
                self._apply_fix(analysis, func, args, kwargs)
        else:
            console.print("[yellow]Could not analyze error with GPT-4. Re-raising original exception.[/yellow]")
            raise error
    
    def _prepare_context(self, error: Exception, func: Callable, args: tuple, 
                        kwargs: dict, traceback_str: str, source: str) -> Dict[str, Any]:
        """Prepare context information for GPT-4 analysis."""
        return {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "function_name": func.__name__,
            "function_source": source,
            "function_args": str(args),
            "function_kwargs": str(kwargs),
            "traceback": traceback_str,
            "python_version": sys.version,
            "working_directory": os.getcwd()
        }
    
    def _analyze_with_gpt4(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze the error using GPT-4."""
        try:
            prompt = self._create_analysis_prompt(context)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python debugging expert. Analyze the error and provide clear explanations and fixes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as JSON, fallback to text
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "explanation": content,
                    "suggested_fix": "Manual review required",
                    "confidence": "medium"
                }
                
        except Exception as e:
            console.print(f"[red]Error calling GPT-4: {e}[/red]")
            return None
    
    def _create_analysis_prompt(self, context: Dict[str, Any]) -> str:
        """Create the prompt for GPT-4 analysis."""
        return f"""
Please analyze this Python error and provide a detailed explanation and fix.

Error Information:
- Error Type: {context['error_type']}
- Error Message: {context['error_message']}
- Function: {context['function_name']}
- Arguments: {context['function_args']}
- Keyword Arguments: {context['function_kwargs']}

Function Source Code:
```python
{context['function_source']}
```

Full Traceback:
```
{context['traceback']}
```

Environment:
- Python Version: {context['python_version']}
- Working Directory: {context['working_directory']}

Please provide your analysis in the following JSON format:
{{
    "explanation": "Clear explanation of what went wrong",
    "root_cause": "The underlying cause of the error",
    "suggested_fix": "Specific code fix or workaround",
    "confidence": "high/medium/low",
    "additional_notes": "Any additional helpful information"
}}
"""
    
    def _display_analysis(self, analysis: Dict[str, Any]):
        """Display the GPT-4 analysis in a formatted way."""
        console.print("\n[bold blue]🔍 GPT-4 Analysis[/bold blue]")
        
        # Explanation
        if "explanation" in analysis:
            console.print(Panel(
                analysis["explanation"],
                title="[bold]Explanation[/bold]",
                border_style="blue"
            ))
        
        # Root cause
        if "root_cause" in analysis:
            console.print(Panel(
                analysis["root_cause"],
                title="[bold]Root Cause[/bold]",
                border_style="yellow"
            ))
        
        # Suggested fix
        if "suggested_fix" in analysis:
            console.print(Panel(
                Syntax(analysis["suggested_fix"], "python", theme="monokai"),
                title="[bold]Suggested Fix[/bold]",
                border_style="green"
            ))
        
        # Confidence level
        if "confidence" in analysis:
            confidence_color = {
                "high": "green",
                "medium": "yellow", 
                "low": "red"
            }.get(analysis["confidence"], "white")
            
            console.print(f"[{confidence_color}]Confidence: {analysis['confidence']}[/{confidence_color}]")
        
        # Additional notes
        if "additional_notes" in analysis:
            console.print(Panel(
                analysis["additional_notes"],
                title="[bold]Additional Notes[/bold]",
                border_style="cyan"
            ))
    
    def _apply_fix(self, analysis: Dict[str, Any], func: Callable, args: tuple, kwargs: dict):
        """Apply the suggested fix (placeholder for now)."""
        console.print("[yellow]⚠️  Auto-fix feature is not yet implemented.[/yellow]")
        console.print("[yellow]Please manually apply the suggested fix from the analysis above.[/yellow]")
    
    def run_cli(self, func: Callable, *args, **kwargs):
        """Run a function with CLI interface and self-debugging."""
        decorated_func = self.debug_function(func)
        return decorated_func(*args, **kwargs)


# Global instance
debug_cli = SelfDebugCLI()


def self_debug(func: Callable) -> Callable:
    """
    Decorator to enable self-debugging for any function.
    
    Usage:
        @self_debug
        def my_function():
            # Your code here
            pass
    """
    return debug_cli.debug_function(func)


@click.command()
@click.option('--api-key', envvar='OPENAI_API_KEY', help='OpenAI API key')
@click.option('--debug/--no-debug', default=True, help='Enable/disable self-debugging')
@click.argument('script', type=click.Path(exists=True))
@click.argument('args', nargs=-1)
def main(api_key: str, debug: bool, script: str, args: tuple):
    """Run a Python script with self-debugging enabled."""
    # Update debug mode
    debug_cli.debug_mode = debug
    
    # Set API key if provided
    if api_key:
        debug_cli.api_key = api_key
        if OPENAI_AVAILABLE:
            debug_cli.client = OpenAI(api_key=api_key)
    
    # Load and run the script
    script_path = Path(script)
    
    # Read the script content
    with open(script_path, 'r') as f:
        script_content = f.read()
    
    # Create a namespace for the script
    script_globals = {
        '__name__': '__main__',
        '__file__': str(script_path),
        'self_debug': self_debug,
        'debug_cli': debug_cli
    }
    
    # Add command line arguments
    script_globals['sys.argv'] = [script] + list(args)
    
    console.print(f"[bold green]🚀 Running {script} with self-debugging enabled[/bold green]")
    
    try:
        # Execute the script
        exec(script_content, script_globals)
    except Exception as e:
        if debug and debug_cli.client:
            # Create a dummy function to wrap the error
            def dummy_func():
                raise e
            
            debug_cli._handle_error(e, dummy_func, (), {})
        else:
            raise


if __name__ == "__main__":
    main() 