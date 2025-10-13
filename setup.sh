#!/bin/bash

# ICETEX Petition Classifier - Setup Script
# This script helps you set up the project quickly

echo "🎓 ICETEX Petition Classifier - Setup Script"
echo "=============================================="
echo ""

# Check Python version
echo "📍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check Tesseract
echo "📍 Checking Tesseract OCR..."
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract is not installed."
    echo "   macOS: brew install tesseract tesseract-lang"
    echo "   Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-spa"
else
    TESSERACT_VERSION=$(tesseract --version | head -n 1)
    echo "✅ Found $TESSERACT_VERSION"
fi
echo ""

# Check Poppler
echo "📍 Checking Poppler..."
if ! command -v pdfinfo &> /dev/null; then
    echo "⚠️  Poppler is not installed."
    echo "   macOS: brew install poppler"
    echo "   Ubuntu: sudo apt-get install poppler-utils"
else
    echo "✅ Poppler is installed"
fi
echo ""

# Create virtual environment
echo "📍 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "📍 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check for .env file
echo "📍 Checking environment configuration..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "⚠️  .env file not found"
    echo ""
    echo "Please create a .env file with your OpenAI API key:"
    echo ""
    echo "OPENAI_API_KEY=sk-your-api-key-here"
    echo "OPENAI_MODEL=gpt-4-turbo"
    echo ""
    read -p "Would you like to create it now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your OpenAI API key: " api_key
        echo "OPENAI_API_KEY=$api_key" > .env
        echo "OPENAI_MODEL=gpt-4-turbo" >> .env
        echo "✅ .env file created"
    fi
fi
echo ""

# Setup complete
echo "=============================================="
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the server: python main.py"
echo "  3. Open your browser: http://localhost:8000"
echo ""
echo "For more information, see README.md"
echo "=============================================="

