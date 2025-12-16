# 🎮 How to See Your Bots in the GUI

## The Issue
You need **BOTH** the server AND the GUI running:
- ✅ Server is running (port 7654) - for bot connections
- ❌ GUI needs to be started separately - for visualization

## Solution: Start the GUI

### Option 1: Launch GUI Application
```bash
cd /home/user/Documents/RoboCode
./start_gui.sh
```

This will start the Tank Royale GUI desktop application.

### Option 2: Manual GUI Launch
```bash
/opt/robocode-tank-royale-gui/bin/Robocode\ Tank\ Royale\ GUI &
```

## Then Launch Your Bots

Once the GUI is open:

```bash
# In terminal 1 - Launch first bot
cd /home/user/Documents/RoboCode
./launch_bot_for_gui.sh Samples/sitting_duck.py

# In terminal 2 - Launch second bot (optional)
cd /home/user/Documents/RoboCode
./launch_bot_for_gui.sh Samples/champion_bot.py
```

## What You Should See

1. **GUI Window Opens** - You'll see the Tank Royale visual interface
2. **Bots Appear** - In the GUI's bot list, you'll see:
   - SittingDuck
   - ChampionBot
   - Any other bots you launch
3. **Start Battle** - Click the "Start Battle" button in the GUI
4. **Watch the Fight!** - See your bots battle visually

## Troubleshooting

### GUI doesn't start
- Check if DISPLAY is set: `echo $DISPLAY`
- May need X11 forwarding or VNC if on remote server
- Alternative: Use the web-based GUI (if available)

### Bots don't appear
- Make sure GUI is fully loaded before launching bots
- Check bot output shows: "Connected to: ws://localhost:7654"
- Keep bot terminal windows open (don't close them)

### Quick Test
```bash
# 1. Start GUI
./start_gui.sh

# 2. Wait for GUI to open (5-10 seconds)

# 3. Launch a bot
python Samples/sitting_duck.py

# 4. You should see "SittingDuck" appear in the GUI
```

## Architecture

```
┌─────────────────────┐
│  Tank Royale GUI    │ ← You need to START this!
│  (Desktop App)      │
└──────────┬──────────┘
           │
           │ WebSocket
           │
┌──────────▼──────────┐
│  Tank Royale Server │ ← Already running ✅
│  (Port 7654)        │
└──────────┬──────────┘
           │
           │ WebSocket
           │
    ┌──────┴──────┬──────────┬─────────┐
    │             │          │         │
┌───▼───┐   ┌────▼───┐  ┌───▼───┐ ┌──▼──┐
│ Bot 1 │   │ Bot 2  │  │ Bot 3 │ │ ... │
└───────┘   └────────┘  └───────┘ └─────┘
```

Both the server AND the GUI must be running!
