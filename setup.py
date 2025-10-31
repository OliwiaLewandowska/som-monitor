"""
Setup script for SOM Monitor
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="som-monitor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Share of Model (SOM) tracking system for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/som-monitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "pandas>=2.0.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "scipy>=1.11.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "som-monitor=main:main",
        ],
    },
)
