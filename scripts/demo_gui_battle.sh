#!/bin/bash
# Demo: How to Run GUI Battles
# This shows the CORRECT way to add tanks to the GUI

echo "════════════════════════════════════════════════════════"
echo "  🎮 Tank Royale GUI Battle Demo"
echo "════════════════════════════════════════════════════════"
echo ""
echo "IMPORTANT: This script assumes the Tank Royale server is ALREADY RUNNING!"
echo ""
echo "If not running, start it first:"
echo "  1. Download from: https://github.com/robocode-dev/tank-royale/releases"
echo "  2. Run the server"
echo "  3. Open browser to http://localhost:8080"
echo ""
echo "Press Enter when server is ready, or Ctrl+C to cancel..."
read

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Step 1: Launching Tank 1 (FinalBoss GUI)"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Running: python Submissions/ClaudeCode/final_boss_tank_gui.py"
echo ""
echo "This tank will connect to the server and appear in your browser!"
echo ""

cd ~/Documents/RoboCode

# Launch tank in background
python Submissions/ClaudeCode/final_boss_tank_gui.py &
TANK1_PID=$!

echo "✓ Tank 1 launched (PID: $TANK1_PID)"
echo ""
sleep 2

echo "════════════════════════════════════════════════════════"
echo "  Step 2: Check Your Browser"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Go to: http://localhost:8080"
echo ""
echo "You should see 'FinalBossTankGUI' in the bot list!"
echo ""
echo "Press Enter to continue..."
read

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Step 3: Launch More Tanks (Optional)"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Want to add more tanks? (y/n)"
read -r ADD_MORE

if [ "$ADD_MORE" = "y" ]; then
    echo ""
    echo "Launching a simple demo opponent..."

    # Create simple opponent on the fly
    cat > /tmp/demo_bot.py << 'EOF'
import asyncio
from robocode_tank_royale.bot_api import BaseBot

class DemoBot(BaseBot):
    async def run(self):
        while True:
            self.forward(100)
            self.turn_right(30)
            self.turn_radar_right(45)
            await self.go()

    def on_scanned_bot(self, event):
        self.fire(2)

if __name__ == "__main__":
    import os
    os.environ['BOT_NAME'] = 'DemoBot'
    os.environ['BOT_VERSION'] = '1.0'
    os.environ['BOT_AUTHORS'] = 'Demo'
    bot = DemoBot()
    asyncio.run(bot.start())
EOF

    python /tmp/demo_bot.py &
    TANK2_PID=$!

    echo "✓ Demo opponent launched (PID: $TANK2_PID)"
    echo ""
    sleep 2
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Step 4: Start the Battle!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "In your browser (http://localhost:8080):"
echo "  1. Check the boxes next to the tanks you want"
echo "  2. Click 'Start Battle'"
echo "  3. WATCH THE ACTION! 🎮💥"
echo ""
echo "Press Enter when you want to stop all tanks..."
read

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Stopping Tanks..."
echo "════════════════════════════════════════════════════════"
echo ""

kill $TANK1_PID 2>/dev/null && echo "✓ Stopped Tank 1"
[ -n "$TANK2_PID" ] && kill $TANK2_PID 2>/dev/null && echo "✓ Stopped Tank 2"

echo ""
echo "Done! Run this script again anytime to demo GUI battles!"
echo ""
