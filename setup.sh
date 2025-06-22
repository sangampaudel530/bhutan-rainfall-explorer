#!/bin/bash

# Bhutan Rainfall Explorer - Setup Script
# This script sets up the project environment and dependencies

echo "🌄 Setting up Bhutan Rainfall Explorer..."
echo "======================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(sys.version_info[:2])")
echo "🐍 Python version detected: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check your Python environment."
    exit 1
fi

# Check if Streamlit is properly installed
if command -v streamlit &> /dev/null; then
    echo "🚀 Streamlit is ready!"
else
    echo "⚠️  Streamlit installation might have issues."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
echo "To start Jupyter notebook:"
echo "  jupyter notebook notebooks/"
echo ""
echo "Happy exploring! 🐉"
