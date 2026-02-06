#!/bin/bash
# One-click Mouse Macro Recorder Installation

echo "🖱️ Installing Mouse Macro Recorder..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 required but not installed"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To run:"
echo "  cd mouse-macro-recorder"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or run directly:"
echo "  python3 main.py"
