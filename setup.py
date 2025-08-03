#!/usr/bin/env python3
"""
Setup script for the Self-Debugging CLI Tool.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="self-debug-cli",
    version="1.0.0",
    author="Self-Debug CLI Team",
    author_email="your-email@example.com",
    description="A CLI template that wraps any Python function and auto-invokes GPT-4 to explain errors and suggest fixes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/self-healing-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "self-debug=self_debug_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.example"],
    },
    keywords="debugging cli gpt-4 openai python error-handling",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/self-healing-cli/issues",
        "Source": "https://github.com/yourusername/self-healing-cli",
        "Documentation": "https://github.com/yourusername/self-healing-cli#readme",
    },
) 