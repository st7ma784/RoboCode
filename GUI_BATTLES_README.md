# 🎮 GUI Battles - Complete Guide

## 🎯 Understanding the Two Types of Tanks

This project has **TWO types of tank files**:

### 1. Validation Tanks (For Development)
- **Files:** `final_boss_tank.py`, `challenger_tank.py`, tutorial tanks, sample tanks
- **Usage:** `python battle_runner.py tank1.py tank2.py`
- **Purpose:** Quick code validation during development
- **Visual:** Text output only
- **Speed:** Instant
- **Setup:** None needed

### 2. GUI Tanks (For Visual Battles)
- **Files:** `*_gui.py` (e.g., `final_boss_tank_gui.py`)
- **Usage:** `python tank_gui.py` (while server running)
- **Purpose:** Watch animated battles with graphics
- **Visual:** Full graphics, explosions, radar!
- **Speed:** Requires ~30sec setup
- **Setup:** Need Tank Royale server running

---

## ⚠️ THE KEY ISSUE YOU HIT

You tried to run validation tanks (`final_boss_tank.py`) with the GUI - **they're not compatible!**

**Error you saw:**
```
AttributeError: 'FinalBossTank' object has no attribute 'start'
```

**Why:**
- Validation tanks are standalone classes
- GUI tanks must inherit from `BaseBot`
- Different APIs, different purposes

---

## ✅ SOLUTION: Use GUI Tanks

### Option 1: Use Existing GUI Tank (Quickest!)

```bash
# Make sure you installed packages correctly
python -m pip install -r requirements.txt

# Run the GUI tank (server must be running first!)
python Submissions/ClaudeCode/final_boss_tank_gui.py
```

### Option 2: Create Your Own GUI Tank

**Template:**
```python
import asyncio
from pathlib import Path
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class MyAwesomeTank(BaseBot):
    """Your tank description"""

    async def run(self):
        """Main loop - runs every turn"""
        while True:
            # Your strategy here
            self.forward(100)
            self.turn_radar_right(45)
            self.turn_gun_right(30)

            # IMPORTANT: Must call go() each turn!
            await self.go()

    def on_scanned_bot(self, event):
        """Called when radar finds an enemy"""
        self.fire(2)  # Shoot!

    def on_hit_by_bullet(self, event):
        """Called when you get hit"""
        self.turn_right(90)  # Dodge!

if __name__ == "__main__":
    # Load config from JSON
    script_dir = Path(__file__).parent
    json_file = script_dir / "MyAwesomeTank.json"

    bot_info = BotInfo.from_file(str(json_file)) if json_file.exists() else None

    # Start the bot
    bot = MyAwesomeTank(bot_info=bot_info)
    asyncio.run(bot.start())
```

**Also create `MyAwesomeTank.json`:**
```json
{
  "name": "MyAwesomeTank",
  "version": "1.0.0",
  "authors": ["Your Name"],
  "description": "My awesome tank!",
  "countryCodes": ["US"],
  "gameTypes": ["melee", "1v1"],
  "platform": "Python",
  "programmingLang": "Python 3.10+"
}
```

---

## 🚀 Step-by-Step: Your First GUI Battle

### Step 1: Install Everything Correctly

**IMPORTANT - Use this exact command:**
```bash
cd ~/Documents/RoboCode
python -m pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "from robocode_tank_royale.bot_api import BaseBot; print('✓ Installed!')"
```

### Step 2: Start Tank Royale Server

**Download from:** https://github.com/robocode-dev/tank-royale/releases

**Run it:**
- Windows: Double-click `robocode-tank-royale-server.exe`
- Mac/Linux: `./robocode-tank-royale-server`
- Docker: `docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server`

**You should see:**
```
Server running on port 7654
UI available at http://localhost:8080
```

### Step 3: Open Browser

Go to: **http://localhost:8080**

You'll see the Tank Royale arena interface!

### Step 4: Launch Your Tank

**In a terminal:**
```bash
cd ~/Documents/RoboCode
python Submissions/ClaudeCode/final_boss_tank_gui.py
```

**You should see:**
```
Connecting to ws://localhost:7654
Connected!
Waiting for game to start...
```

### Step 5: Launch Opponents (Optional)

**In separate terminals**, launch more bots:

```bash
# Create a simple opponent
python -c "
import asyncio
from robocode_tank_royale.bot_api import BaseBot

class SimpleBot(BaseBot):
    async def run(self):
        while True:
            self.forward(100)
            self.turn_right(30)
            await self.go()

if __name__ == '__main__':
    bot = SimpleBot()
    asyncio.run(bot.start())
" &
```

### Step 6: Start Battle in Browser

1. You'll see your bot(s) listed in the browser
2. Select the bots you want to fight
3. Click **"Start Battle"**
4. **WATCH THE ACTION!** 💥

---

## 📊 Quick Reference

### Commands Cheat Sheet

```bash
# Install (ALWAYS use python -m pip!)
python -m pip install -r requirements.txt

# Verify installation
python -c "from robocode_tank_royale.bot_api import BaseBot; print('OK!')"

# Run validation tank (quick testing)
python battle_runner.py tank1.py tank2.py

# Run GUI tank (visual battles - server must be running!)
python tank_gui.py
```

### File Naming Convention

```
my_tank.py          # Validation version
my_tank_gui.py      # GUI version
my_tank_gui.json    # GUI config (required!)
```

---

## 🔧 Troubleshooting

### "Module not found: robocode_tank_royale"

**Fix:**
```bash
# Use python -m pip (not just pip!)
python -m pip install robocode-tank-royale
```

### "No attribute 'start'"

**Problem:** You're trying to run a validation tank in GUI mode.

**Fix:** Use a `*_gui.py` tank or create one!

### "Connection refused"

**Problem:** Tank Royale server not running.

**Fix:**
1. Start the server first
2. Make sure you see "Server running on port 7654"
3. Check browser works at `http://localhost:8080`

### "Bot doesn't appear in browser"

**Fixes:**
1. Make sure bot script is still running (check terminal)
2. Check for errors in bot terminal
3. Refresh browser page
4. Restart server

---

## 🎓 Learning Path

1. **Start with validation tanks** (`battle_runner.py`)
   - Quick feedback
   - Easy debugging
   - Perfect for learning

2. **Graduate to GUI tanks** when ready
   - Watch your creations fight!
   - Show off to friends
   - Submit to competitions

3. **Master both approaches**
   - Develop with validation tanks
   - Showcase with GUI battles

---

## 📚 More Resources

- **SETUP_GUI.md** - Detailed GUI setup
- **QUICK_GUI_START.md** - Fast GUI start guide
- **Week1 README** - Tutorial with GUI instructions
- **Tank Royale Docs:** https://robocode-dev.github.io/tank-royale/

---

## 🎮 Ready to Battle!

You now understand:
- ✅ Difference between validation and GUI tanks
- ✅ How to install packages correctly (`python -m pip`)
- ✅ How to create GUI tanks
- ✅ How to run visual battles

**Go create something awesome!** 🚀
