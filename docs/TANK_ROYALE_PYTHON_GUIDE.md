# 🎯 REAL Solution: How Tank Royale Works with Python Bots

## The Architecture (What You ACTUALLY Need)

Tank Royale has **4 components** for Python bots:

```
1. Server (Port 7654)     ✅ Running
2. GUI (Desktop App)      ✅ Started  
3. Booter (Bot Discovery) ❌ MISSING - THIS IS THE ISSUE!
4. Python Bots            ✅ Ready
```

## The Missing Piece: The BOOTER

**The Booter is ESSENTIAL for Python bots!**

- Java bots can connect directly to the server
- **Python bots MUST be discovered by the Booter**
- The Booter makes bots visible to the GUI

## Complete Startup Sequence

### Step 1: Start the Server (Already Running ✅)
```bash
# Server is already running on port 7654
```

### Step 2: Start the Booter (THIS IS WHAT'S MISSING! ❌)
```bash
cd /home/user/Documents/RoboCode
./start_booter.sh
```

### Step 3: Start the GUI
```bash
./start_gui.sh
```

### Step 4: Configure Bot Directories in Booter

The Booter needs to know WHERE to find your bots. There are two approaches:

#### Option A: Use Booter UI (Recommended)
1. Open the Booter application window
2. Go to Settings/Preferences
3. Add bot directories:
   - `/home/user/Documents/RoboCode/Samples`
   - `/home/user/Documents/RoboCode/Tutorials/Week1_MyFirstTank`
   - `/home/user/Documents/RoboCode/Submissions/ClaudeCode`
4. Click "Rescan" or "Refresh"

#### Option B: Edit Booter Config File
Look for config file (usually in `~/.robocode-tank-royale/` or similar):
```json
{
  "botDirectories": [
    "/home/user/Documents/RoboCode/Samples",
    "/home/user/Documents/RoboCode/Tutorials",
    "/home/user/Documents/RoboCode/Submissions"
  ]
}
```

## Bot Directory Structure

Each bot needs to be in its own directory with BOTH files:

```
Samples/
  sitting_duck.py      ← Python code
  sitting_duck.json    ← Bot metadata

Tutorials/Week1_MyFirstTank/
  my_first_tank.py     ← Python code
  my_first_tank.json   ← Bot metadata
```

## Why Direct Python Execution Doesn't Work

When you run `python bot.py` directly:
- ✅ Bot connects to server
- ❌ GUI doesn't know about it
- ❌ Can't be selected for battles
- ❌ Not managed by Booter

The Booter:
- Scans configured directories
- Reads bot JSON metadata
- Registers bots with server
- Makes them available in GUI
- Manages bot lifecycle

## Complete Test

```bash
# 1. Start Booter
./start_booter.sh

# 2. Start GUI  
./start_gui.sh

# 3. In Booter:
#    - Add /home/user/Documents/RoboCode/Samples
#    - Click Rescan

# 4. In GUI:
#    - You should now see: SittingDuck, SpinBot, etc.
#    - Select bots and Start Battle!
```

## Architecture Diagram

```
┌─────────────────────┐
│   Tank Royale GUI   │ ← Visual interface
│   (Select bots,     │
│    Start battles)   │
└──────────┬──────────┘
           │
           │ WebSocket
           │
┌──────────▼──────────┐
│  Tank Royale Server │ ← Battle engine
│  (Port 7654)        │
└──────────▲──────────┘
           │
           │ WebSocket
           │
┌──────────┴──────────┐
│  Tank Royale Booter │ ← Bot discovery & management
│  (Scans directories)│ ← YOU NEED TO START THIS!
└──────────┬──────────┘
           │
           │ Discovers & Launches
           │
    ┌──────┴──────┬──────────┐
    │             │          │
┌───▼───┐   ┌────▼───┐  ┌───▼───┐
│Bot Dir│   │Bot Dir │  │Bot Dir│
│ .py   │   │ .py    │  │ .py   │
│ .json │   │ .json  │  │ .json │
└───────┘   └────────┘  └───────┘
```

## Summary

❌ **Wrong Approach:**
```bash
python my_bot.py  # Bot runs but GUI doesn't see it
```

✅ **Correct Approach:**
```bash
1. Start Booter (discovers bots)
2. Start GUI (select bots)
3. Booter launches bots for battles
```

The Python bots don't run standalone - they're managed by the Booter!
