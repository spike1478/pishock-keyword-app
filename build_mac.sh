#!/bin/bash
# Build script for Mac version of PiShock Universal App

echo "Building PiShock Universal App for Mac..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create build directory
mkdir -p build/mac
cd build/mac

# Copy source files
cp ../../pishock_app.py .
cp ../../requirements.txt .
cp ../../pishock_app_mac.spec .

# Build the app
echo "Building Mac app..."
pyinstaller pishock_app_mac.spec

# Check if build was successful
if [ -d "dist/PiShock Universal.app" ]; then
    echo "✅ Build successful!"
    echo "App created: build/mac/dist/PiShock Universal.app"
    echo ""
    echo "To run the app:"
    echo "open 'build/mac/dist/PiShock Universal.app'"
    echo ""
    echo "To create a DMG installer, use:"
    echo "hdiutil create -volname 'PiShock Universal' -srcfolder 'build/mac/dist/PiShock Universal.app' -ov -format UDZO 'PiShock Universal.dmg'"
else
    echo "❌ Build failed!"
    exit 1
fi
