#!/bin/bash

echo "🌱 KhetSetGo Smart Farming System - Linux/macOS Setup"
echo "=================================================="

echo ""
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version is installed"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

node_version=$(node --version)
echo "✅ Node.js $node_version is installed"

echo ""
echo "🚀 Starting automated setup..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Setup failed. Please check the errors above."
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the application, run:"
echo "   python3 run_app.py"
echo ""
echo "📱 Then visit: http://localhost:3000"
echo ""
