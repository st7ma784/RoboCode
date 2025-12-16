#!/bin/bash
# Complete step-by-step demo of Tank Royale with Python bots

clear

cat << 'EOF'
════════════════════════════════════════════════════════════════
  🎮 TANK ROYALE COMPLETE SETUP - STEP BY STEP
════════════════════════════════════════════════════════════════

This will walk you through setting up Tank Royale from scratch.

Tank Royale has 4 components:
  1. Server  - Manages battles (Port 7654)
  2. GUI     - Visual interface to watch battles
  3. Booter  - Discovers & launches Python bots
  4. Bots    - Your Python tank code

Let's check what's running and set up everything correctly...

EOF

echo "Press Enter to start..."
read

# Step 1: Check Server
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 1: Checking Tank Royale SERVER"
echo "═══════════════════════════════════════════════════════════"
echo ""

if pgrep -f "robocode-tank-royale-server" > /dev/null; then
    echo "✅ Server is RUNNING"
    echo "   Port 7654 is active for bot connections"
else
    echo "❌ Server is NOT running"
    echo ""
    echo "To start the server:"
    echo "   /opt/robocode-tank-royale-server/bin/Robocode\ Tank\ Royale\ Server &"
    echo ""
    echo "Press Enter to continue anyway..."
    read
fi

echo ""
echo "Press Enter for next step..."
read

# Step 2: Check GUI
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 2: Checking Tank Royale GUI"
echo "═══════════════════════════════════════════════════════════"
echo ""

if pgrep -f "robocode-tank-royale-gui" > /dev/null; then
    echo "✅ GUI is RUNNING"
    echo "   You should see a Tank Royale window open"
else
    echo "❌ GUI is NOT running"
    echo ""
    echo "Starting GUI now..."
    ./start_gui.sh
    sleep 2
fi

echo ""
echo "Press Enter for next step..."
read

# Step 3: Check Booter
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 3: Checking Tank Royale BOOTER (Critical for Python!)"
echo "═══════════════════════════════════════════════════════════"
echo ""

if pgrep -f "robocode-tank-royale-booter" > /dev/null; then
    echo "✅ Booter is RUNNING"
    echo "   Python bots can be discovered"
else
    echo "❌ Booter is NOT running"
    echo ""
    echo "The Booter is ESSENTIAL for Python bots!"
    echo ""
    echo "Starting Booter now..."
    ./start_booter.sh
    sleep 2
    
    echo ""
    echo "✅ Booter started!"
fi

echo ""
echo "Press Enter for next step..."
read

# Step 4: Configure Bot Directories
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 4: CONFIGURE Bot Directories in Booter"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "NOW DO THIS MANUALLY:"
echo ""
echo "1. Look for the 'Robocode Tank Royale Booter' window"
echo "2. Find Settings/Preferences/Configuration menu"
echo "3. Add these bot directories:"
echo ""
echo "   📁 $(pwd)/Samples"
echo "   📁 $(pwd)/Tutorials/Week1_MyFirstTank"
echo "   📁 $(pwd)/Tutorials/Week2_Trigonometry"
echo "   📁 $(pwd)/Tutorials/Week5_AdvancedTargeting"
echo "   📁 $(pwd)/Submissions/ClaudeCode"
echo ""
echo "4. Click 'Rescan' or 'Refresh' button"
echo "5. You should see bots appear in the Booter list:"
echo "   - SittingDuck"
echo "   - SpinBot"
echo "   - ChampionBot"
echo "   - MyFirstTank"
echo "   - etc."
echo ""
echo "Press Enter when you've added the directories..."
read

# Step 5: Select Bots in GUI
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 5: SELECT Bots in GUI"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "NOW DO THIS IN THE GUI:"
echo ""
echo "1. Look at the 'Robocode Tank Royale GUI' window"
echo "2. You should see a bot list/selection area"
echo "3. The bots discovered by the Booter appear here"
echo "4. Select 2-4 bots for a battle:"
echo "   - Click on SittingDuck"
echo "   - Click on SpinBot"
echo "   - Click on ChampionBot"
echo "   (You can select multiple bots)"
echo ""
echo "Press Enter when you've selected bots..."
read

# Step 6: Start Battle
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 6: START THE BATTLE!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "NOW DO THIS:"
echo ""
echo "1. In the GUI, find the 'Start Battle' button"
echo "2. Click it!"
echo "3. Watch your bots fight! 🎮"
echo ""
echo "What happens:"
echo "  • Booter launches the selected Python bot files"
echo "  • Bots connect to server (port 7654)"
echo "  • Server runs the battle"
echo "  • GUI shows the visual battle"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🎉 That's it! You should now see bots battling visually!"
echo ""
echo "═══════════════════════════════════════════════════════════"

cat << 'EOF'

TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If bots don't appear in GUI:
  ✓ Make sure Booter is running
  ✓ Check Booter has bot directories configured
  ✓ Click 'Rescan' in Booter
  ✓ Restart GUI and Booter if needed

If battle won't start:
  ✓ Need at least 2 bots selected
  ✓ Make sure Server is running
  ✓ Check bot .json files are valid

Each bot needs TWO files:
  ✓ botname.py   (Python code)
  ✓ botname.json (Bot metadata)

Bot directory structure:
  Samples/
    sitting_duck.py    ✓
    sitting_duck.json  ✓
  
  Tutorials/Week1_MyFirstTank/
    my_first_tank.py   ✓
    my_first_tank.json ✓

═══════════════════════════════════════════════════════════════
EOF
