#!/bin/bash
# Launch a bot and keep it running for the GUI

BOT_FILE="${1:-Samples/sitting_duck.py}"

echo "════════════════════════════════════════════════════════"
echo "  🤖 Launching Bot for GUI"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Bot file: $BOT_FILE"
echo ""
echo "The bot will connect to the server and appear in the GUI."
echo "Open your browser to: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the bot"
echo "════════════════════════════════════════════════════════"
echo ""

python "$BOT_FILE"
