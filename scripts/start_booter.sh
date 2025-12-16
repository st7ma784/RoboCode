#!/bin/bash
# Proper way to launch Python bots for Tank Royale GUI

echo "════════════════════════════════════════════════════════"
echo "  🚀 Tank Royale Booter - Python Bot Launcher"
echo "════════════════════════════════════════════════════════"
echo ""
echo "IMPORTANT: Tank Royale Python bots need the BOOTER!"
echo ""
echo "The Booter:"
echo "  • Discovers bots in directories"
echo "  • Makes them visible to the GUI"
echo "  • Manages bot lifecycle"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""

# Start the booter
echo "Starting Booter..."
/opt/robocode-tank-royale-booter/bin/Robocode\ Tank\ Royale\ Booter &

BOOTER_PID=$!

echo "✅ Booter started (PID: $BOOTER_PID)"
echo ""
echo "The Booter will scan for bot directories."
echo ""
echo "Bot Directory Setup:"
echo "  1. Each bot needs its own directory"
echo "  2. Directory contains: .py file + .json file"
echo "  3. Booter discovers bots from configured paths"
echo ""
echo "To stop: kill $BOOTER_PID"
echo "════════════════════════════════════════════════════════"
