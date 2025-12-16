# 🎮 Tank Royale Step-by-Step Guide

## The Complete Picture

Tank Royale has **4 components** that work together:

```
┌─────────────────────┐
│  1. SERVER          │  Manages battles, coordinates everything
│  Port 7654          │  (Usually auto-starts or already running)
└──────────┬──────────┘
           │
    ┌──────┴──────┬─────────────┐
    │             │             │
┌───▼────────┐ ┌──▼─────────┐ ┌▼──────────┐
│ 2. GUI     │ │ 3. BOOTER  │ │ 4. BOTS   │
│ (Visual)   │ │ (Python!)  │ │ (.py+.json)│
└────────────┘ └────────────┘ └───────────┘
```

## Step-by-Step Process

### STEP 1: Start the Server
```bash
# Usually already running
# If not: /opt/robocode-tank-royale-server/bin/Robocode\ Tank\ Royale\ Server &
```
**What it does:** Runs battles, manages game logic, port 7654

### STEP 2: Start the GUI
```bash
./start_gui.sh
```
**What it does:** Visual window where you watch battles

### STEP 3: Start the Booter ⭐ (CRITICAL FOR PYTHON!)
```bash
./start_booter.sh
```
**What it does:** 
- Scans directories for Python bots
- Reads `.json` files to get bot info
- Makes bots available to GUI
- Launches bots when battle starts

### STEP 4: Configure Booter

In the **Booter window**:
1. Open Settings/Preferences
2. Add bot directories:
   ```
   /home/user/Documents/RoboCode/Samples
   /home/user/Documents/RoboCode/Tutorials/Week1_MyFirstTank
   /home/user/Documents/RoboCode/Tutorials/Week5_AdvancedTargeting
   ```
3. Click **"Rescan"** or **"Refresh"**

**What happens:**
- Booter scans these directories
- Finds bot pairs: `bot.py` + `bot.json`
- Registers them with the server
- Makes them selectable in GUI

### STEP 5: Select Bots in GUI

In the **GUI window**:
1. Look for the bot selection panel/list
2. You should now see:
   - ✓ SittingDuck
   - ✓ SpinBot
   - ✓ ChampionBot
   - ✓ MyFirstTank
   - ✓ etc.
3. Click to select 2-4 bots

### STEP 6: Start Battle!

1. Click **"Start Battle"** button in GUI
2. **Booter launches** the Python bot processes
3. Bots **connect to server** (port 7654)
4. Server **runs the battle**
5. GUI **shows visual battle** 🎮

## Why Python Bots Need the Booter

### Java Bots (Traditional Robocode):
```
Bot.jar → Server → GUI
   ↓
Direct connection ✓
```

### Python Bots (Tank Royale):
```
Bot.py + Bot.json → Booter → Server → GUI
                      ↓
              Discovery & Launch ✓
```

Python bots can't connect directly! They need:
1. **Discovery:** Booter finds them in directories
2. **Metadata:** Booter reads `.json` for bot info
3. **Registration:** Booter tells server about them
4. **Launch:** Booter starts Python process when battle begins

## File Structure Requirements

Each bot needs **BOTH** files in the **SAME DIRECTORY**:

```
✅ CORRECT:
Samples/
  ├── sitting_duck.py     ← Python code
  └── sitting_duck.json   ← Bot metadata

Tutorials/Week1_MyFirstTank/
  ├── my_first_tank.py    ← Python code
  └── my_first_tank.json  ← Bot metadata

❌ WRONG:
Samples/
  ├── all_bots.py         ← Multiple bots in one file
  └── config.json         ← Wrong naming
```

## JSON File Format

The `.json` file tells the Booter about your bot:

```json
{
  "name": "MyBot",
  "version": "1.0.0",
  "authors": ["Your Name"],
  "description": "What the bot does",
  "countryCodes": ["US"],
  "gameTypes": ["melee", "1v1"],
  "platform": "Python",
  "programmingLang": "Python 3.10+"
}
```

## Quick Reference

| Component | Purpose | Command |
|-----------|---------|---------|
| Server | Battle engine | Usually auto-starts |
| GUI | Visual interface | `./start_gui.sh` |
| Booter | Python bot discovery | `./start_booter.sh` |
| Bots | Your tank code | Managed by Booter |

## Common Issues

### "I don't see my bots in the GUI"
✓ Check: Is Booter running?
✓ Check: Did you add directories in Booter settings?
✓ Check: Did you click "Rescan" in Booter?
✓ Check: Does each bot have BOTH `.py` and `.json` files?

### "Battle won't start"
✓ Need at least 2 bots selected
✓ Server must be running
✓ Bot `.json` files must be valid

### "Bot appears but won't launch"
✓ Check Python code has no syntax errors
✓ Check bot inherits from `BaseBot`
✓ Check `__init__` accepts `bot_info` parameter
✓ Check entry point uses `asyncio.run(bot.start())`

## Flow Diagram

```
You → Start Booter → Configure directories → Rescan
                                                ↓
                                        Booter finds bots
                                                ↓
You → Start GUI → See bot list ← Booter provides list
                      ↓
              Select bots (2-4)
                      ↓
              Click "Start Battle"
                      ↓
          Booter launches Python processes
                      ↓
          Bots connect to Server (7654)
                      ↓
              Server runs battle
                      ↓
          GUI shows visual battle 🎮
```

## Complete Workflow

1. **Setup (once):**
   ```bash
   ./start_booter.sh
   # Configure directories in Booter
   ```

2. **Each session:**
   ```bash
   ./start_gui.sh           # Open visual interface
   # Select bots in GUI
   # Click "Start Battle"
   ```

3. **Bots appear and battle automatically!** 🎉

## Testing Your Setup

Run this to verify everything:
```bash
./complete_setup_demo.sh
```

This walks you through each step interactively.
