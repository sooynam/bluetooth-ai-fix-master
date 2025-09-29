#!/bin/bash

echo "🚀 Installing Bluetooth AI Fix Master..."
echo "==========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt update && sudo apt install python3 python3-pip -y
fi

# Create virtual environment
echo "📦 Setting up environment..."
python3 -m venv bluetooth-ai-env
source bluetooth-ai-env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install flask

echo ""
echo "✅ Installation complete!"
echo "🚀 Usage:"
echo "   source bluetooth-ai-env/bin/activate"
echo "   python main.py --gui    # Desktop app"
echo "   python main.py --web    # Web interface"
echo "==========================================="
