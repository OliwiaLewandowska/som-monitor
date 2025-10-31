#!/bin/bash

# SOM Monitor Setup Script

echo "======================================"
echo "SOM Monitor - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

if ! python3 -c 'import sys; assert sys.version_info >= (3,8)' 2>/dev/null; then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi
echo "✓ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Create directories
echo "Creating directories..."
mkdir -p data
mkdir -p logs
echo "✓ Directories created"
echo ""

# Setup environment file
echo "Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
else
    echo "✓ .env file already exists"
fi
echo ""

# Run tests
echo "Running tests..."
if python -m pytest tests/ -v; then
    echo "✓ All tests passed"
else
    echo "⚠️  Some tests failed (this is OK for initial setup)"
fi
echo ""

echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run a test survey: python main.py --categories general --runs 2"
echo "3. Launch dashboard: streamlit run app.py"
echo ""
echo "For help, see README.md"
