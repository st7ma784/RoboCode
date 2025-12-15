#!/bin/bash
# Start Tank Royale Server

echo "════════════════════════════════════════════════════════"
echo "  🎮 Starting Tank Royale Server"
echo "════════════════════════════════════════════════════════"
echo ""

# Check if installed
if command -v robocode-tank-royale-server &> /dev/null; then
    echo "✓ Server found! Starting..."
    echo ""
    robocode-tank-royale-server
elif command -v docker &> /dev/null; then
    echo "Server not installed, but Docker found!"
    echo "Starting server with Docker..."
    echo ""
    docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
else
    echo "❌ Server not installed!"
    echo ""
    echo "Install options:"
    echo ""
    echo "1. Install from .deb package:"
    echo "   cd ~/Downloads"
    echo "   sudo dpkg -i robocode-tank-royale-server_0.34.2_amd64.deb"
    echo ""
    echo "2. Use Docker:"
    echo "   docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server"
    echo ""
    exit 1
fi
