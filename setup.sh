#!/bin/bash

# Instagram DP Changer - Local Development Setup Script

echo "🚀 Setting up Instagram DP Changer for local development..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Create assets/images directory if it doesn't exist
echo "🖼️  Ensuring assets/images directory exists..."
mkdir -p assets/images

# Check for environment variables
echo "🔍 Checking configuration..."
if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
    echo "⚠️  Environment variables not set!"
    echo "   Please set USERNAME and PASSWORD environment variables:"
    echo "   export USERNAME='your_instagram_username'"
    echo "   export PASSWORD='your_instagram_password'"
    echo ""
    echo "   Or create a .env file with:"
    echo "   USERNAME=your_instagram_username"
    echo "   PASSWORD=your_instagram_password"
else
    echo "✅ Environment variables configured"
fi

# Check for images
image_count=$(find assets/images -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | wc -l)
if [ "$image_count" -eq 0 ]; then
    echo "⚠️  No images found in assets/images/"
    echo "   Please add your profile pictures (1.png, 2.png, etc.)"
else
    echo "✅ Found $image_count images in assets/images/"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Set environment variables (if not done already)"
echo "  3. Run: python src/main.py"
echo ""
echo "For GitHub Actions deployment, ensure secrets are configured in your repository."