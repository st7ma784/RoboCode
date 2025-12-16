#!/bin/bash
# Start the Tank Royale GUI

echo "════════════════════════════════════════════════════════"
echo "  🎮 Starting Tank Royale GUI"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Launching GUI application..."
echo ""

# Start the GUI
/opt/robocode-tank-royale-gui/bin/Robocode\ Tank\ Royale\ GUI &

GUI_PID=$!

echo "✅ GUI started (PID: $GUI_PID)"
echo ""
echo "The GUI should open in a window."
echo "If it doesn't appear, check that X11/display is configured."
echo ""
echo "To stop the GUI, run: kill $GUI_PID"
echo ""
echo "════════════════════════════════════════════════════════"
