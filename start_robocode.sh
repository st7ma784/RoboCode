#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🤖 Starting RoboCode Tank Royale Complete System${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if components are already running
SERVER_PID=$(pgrep -f "robocode-tank-royale-server")
GUI_PID=$(pgrep -f "robocode-tank-royale-gui")
BOOTER_PID=$(pgrep -f "robocode-tank-royale-booter")

if [ ! -z "$SERVER_PID" ]; then
    echo -e "${YELLOW}⚠️  Server already running (PID: $SERVER_PID)${NC}"
else
    echo -e "${GREEN}1️⃣  Starting Server...${NC}"
    nohup /opt/robocode-tank-royale-server/bin/Robocode\ Tank\ Royale\ Server > /tmp/robocode-server.log 2>&1 &
    sleep 3
    echo -e "${GREEN}   ✓ Server started${NC}"
fi

if [ ! -z "$GUI_PID" ]; then
    echo -e "${YELLOW}⚠️  GUI already running (PID: $GUI_PID)${NC}"
else
    echo -e "${GREEN}2️⃣  Starting GUI...${NC}"
    nohup /opt/robocode-tank-royale-gui/bin/Robocode\ Tank\ Royale\ GUI > /tmp/robocode-gui.log 2>&1 &
    sleep 2
    echo -e "${GREEN}   ✓ GUI window should appear${NC}"
fi

if [ ! -z "$BOOTER_PID" ]; then
    echo -e "${YELLOW}⚠️  Booter already running (PID: $BOOTER_PID)${NC}"
else
    echo -e "${GREEN}3️⃣  Starting Booter...${NC}"
    nohup /opt/robocode-tank-royale-booter/bin/Robocode\ Tank\ Royale\ Booter > /tmp/robocode-booter.log 2>&1 &
    sleep 2
    echo -e "${GREEN}   ✓ Booter window should appear${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ RoboCode Tank Royale is now running!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📋 NEXT STEPS:${NC}"
echo -e "   1. In the ${BLUE}Booter window${NC}:"
echo -e "      • Go to Settings → Bot Directories"
echo -e "      • Add these directories:"
echo -e "        - ${GREEN}$PWD/Samples${NC}"
echo -e "        - ${GREEN}$PWD/Tutorials/Week1_MyFirstTank${NC}"
echo -e "        - ${GREEN}$PWD/Submissions/ExampleSubmission${NC}"
echo -e "      • Click 'Rescan' button"
echo ""
echo -e "   2. In the ${BLUE}GUI window${NC}:"
echo -e "      • Bots should appear in the list (20 available!)"
echo -e "      • Select 2-4 bots"
echo -e "      • Click 'Start Battle'"
echo -e "      • Enjoy the battle! 🎮"
echo ""
echo -e "${YELLOW}📝 Logs available at:${NC}"
echo -e "   Server: /tmp/robocode-server.log"
echo -e "   GUI:    /tmp/robocode-gui.log"
echo -e "   Booter: /tmp/robocode-booter.log"
echo ""
echo -e "${YELLOW}🛑 To stop all components:${NC}"
echo -e "   pkill -f robocode-tank-royale"
echo ""
