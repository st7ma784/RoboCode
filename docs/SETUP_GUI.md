# 🎮 GUI Battle Setup Guide

Complete guide to watching your tanks fight with animated graphics!

## ⚠️ IMPORTANT: Correct Python/Pip Usage

### The Problem
If you see "module not found" errors even after installing packages, you likely have multiple Python versions installed.

### The Solution
**Always use `python -m pip` instead of just `pip`:**

```bash
# ❌ WRONG - might install to different Python
pip install -r requirements.txt

# ✅ CORRECT - installs to YOUR Python
python -m pip install -r requirements.txt
```

This ensures packages install to the same Python you're using to run scripts!

---

## 📋 Prerequisites

1. **Python 3.10+** installed
2. **RoboCode project** downloaded
3. **Packages installed** with correct pip:
   ```bash
   cd RoboCode
   python -m pip install -r requirements.txt
   ```

---

## 🚀 Quick Start - 3 Steps

### Step 1: Start the Tank Royale Server

**Option A: Pre-built Server (Easiest)**
1. Download from: https://github.com/robocode-dev/tank-royale/releases
2. Extract the zip file
3. Run the server:
   - **Windows:** Double-click `robocode-tank-royale-server.exe`
   - **Mac/Linux:** Run `./robocode-tank-royale-server` in terminal

**Option B: Docker (Quick)**
```bash
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
```

**You'll see:**
```
Server running on port 7654
UI available at http://localhost:8080
```

### Step 2: Open the Battle Arena

Open your browser and go to:
```
http://localhost:8080
```

You should see the **Robocode Tank Royale** arena interface! 🎮

### Step 3: Launch Your Tanks

Open **separate terminals** for each bot you want in the battle:

**Terminal 1 (Your tank):**
```bash
cd RoboCode
python run_gui_battle.py Submissions/ClaudeCode/final_boss_tank.py
```

**Terminal 2 (Opponent):**
```bash
python run_gui_battle.py Samples/champion_bot.py
```

**Terminal 3 (Another opponent):**
```bash
python run_gui_battle.py Samples/tracker_bot.py
```

### Step 4: Start the Battle!

In your browser (at `http://localhost:8080`):
1. You'll see your bots listed on the left
2. Select the bots you want to fight (check their boxes)
3. Click **"Start Battle"**
4. **WATCH THE ACTION!** 💥

---

## 🎯 Example Battle Scenarios

### Scenario 1: Your Tank vs Easy Opponents
```bash
# Terminal 1
python run_gui_battle.py Tutorials/Week1_MyFirstTank/my_first_tank.py

# Terminal 2
python run_gui_battle.py Samples/sitting_duck.py

# Terminal 3
python run_gui_battle.py Samples/spin_bot.py
```

### Scenario 2: Final Boss vs Challenger
```bash
# Terminal 1
python run_gui_battle.py Submissions/ClaudeCode/final_boss_tank.py

# Terminal 2
python run_gui_battle.py Submissions/ClaudeCode/challenger_tank.py

# Terminal 3
python run_gui_battle.py Samples/champion_bot.py
```

### Scenario 3: Tutorial Progression
```bash
# Test each week's tank!
python run_gui_battle.py Tutorials/Week1_MyFirstTank/my_first_tank.py
python run_gui_battle.py Tutorials/Week2_Trigonometry/predictor_bot.py
python run_gui_battle.py Tutorials/Week3_BoundaryChecking/boundary_bot.py
# ... and so on
```

---

## 🔧 Troubleshooting

### "Module not found: robocode_tank_royale"

**Fix:**
```bash
# Make sure you use python -m pip
python -m pip install robocode-tank-royale

# Or reinstall all requirements
python -m pip install -r requirements.txt --force-reinstall
```

**Check installation:**
```bash
python -c "from robocode_tank_royale.bot_api import BaseBot; print('Installed!')"
```

### "Connection refused" or "Can't connect to server"

**Fixes:**
1. Make sure the server is running first
2. Check you see "Server running on port 7654" message
3. Try restarting the server
4. Check firewall isn't blocking port 7654

### "No bots appear in browser"

**Fixes:**
1. Make sure bots are actually running (terminals should be active)
2. Check each terminal for error messages
3. Try refreshing the browser
4. Restart server and bots

### "Battle won't start"

**Fixes:**
1. Make sure at least 2 bots are selected
2. Check all bot terminals are still running
3. Try clicking "Refresh Bots" in the UI
4. Restart everything (server + bots)

### Multiple Python Versions

**Check which Python you're using:**
```bash
which python
python --version
```

**Check which pip:**
```bash
which pip
pip --version
```

**If they don't match, always use:**
```bash
python -m pip install [package]
```

---

## 📝 Understanding the System

### Two Ways to Test Tanks

| Method | Purpose | Setup | Visual |
|--------|---------|-------|--------|
| `battle_runner.py` | Quick validation | None | Text only |
| `run_gui_battle.py` | Watch battles | Need server | Full graphics |

### How GUI Battles Work

1. **Server** runs on localhost:7654 (game engine)
2. **UI** opens at localhost:8080 (browser interface)
3. **Bots** connect to server via Python script
4. **You** control battles from browser

### File Requirements

Each bot needs two files:
- `bot_name.py` - The Python code
- `bot_name.json` - Configuration (already created!)

The JSON tells the server:
- Bot name
- Author
- Which Python class to load
- Game types supported

---

## 🎓 Tips for Students

### During Development

**Use `battle_runner.py` for quick testing:**
```bash
python battle_runner.py your_tank.py Samples/sitting_duck.py
```
- Instant feedback
- No setup needed
- Perfect for debugging

### For Showcasing

**Use GUI battles when you want to show off:**
```bash
python run_gui_battle.py your_tank.py
```
- Visual battles
- Great for presentations
- Fun to watch!

### Workflow

1. Write code
2. Test with `battle_runner.py`
3. Fix errors
4. Repeat steps 2-3 until working
5. Show off with GUI battle! 🎉

---

## 🚀 Advanced: Running Multiple Battle Rounds

You can run tournaments by launching many bots:

```bash
# Start server
# In separate terminals, launch all sample bots:
python run_gui_battle.py Samples/sitting_duck.py
python run_gui_battle.py Samples/spin_bot.py
python run_gui_battle.py Samples/walls_bot.py
python run_gui_battle.py Samples/tracker_bot.py
python run_gui_battle.py Samples/champion_bot.py

# Add tutorial bots:
python run_gui_battle.py Tutorials/Week8_AntiGravitySwarms/anti_gravity_tank.py

# Add your submissions:
python run_gui_battle.py Submissions/ClaudeCode/final_boss_tank.py
python run_gui_battle.py Submissions/ClaudeCode/challenger_tank.py

# Now in browser, select all and battle!
```

---

## 📚 Additional Resources

- **Tank Royale Docs:** https://robocode-dev.github.io/tank-royale/
- **Python API Docs:** https://robocode-dev.github.io/tank-royale/api/python/
- **GitHub:** https://github.com/robocode-dev/tank-royale

---

## 🎮 Ready to Battle!

1. ✅ Server running
2. ✅ Browser open to localhost:8080
3. ✅ Bots launched in terminals
4. ✅ Select bots in UI
5. ✅ Click "Start Battle"
6. ✅ **ENJOY THE SHOW!** 🎉💥

Happy battling! 🚀
