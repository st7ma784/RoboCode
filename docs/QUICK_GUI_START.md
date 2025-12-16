# 🎮 GUI Quick Start - Watch Battles NOW!

## The Problem You Hit

The tanks in this repo (`final_boss_tank.py`, `challenger_tank.py`, etc.) are **validation-only** tanks - they work with `battle_runner.py` but not the GUI.

For GUI battles, you need tanks that inherit from `BaseBot`.

## ✅ Solution: Use GUI-Compatible Tanks

I've created GUI versions for you!

---

## 🚀 3-Step Quick Start

### Step 1: Start Tank Royale Server

If you haven't already:
- Download from: https://github.com/robocode-dev/tank-royale/releases
- Run the server (double-click executable or `./robocode-tank-royale-server`)

**You should see:** "Server running on port 7654"

### Step 2: Open Browser

Go to: **http://localhost:8080**

### Step 3: Run GUI Tanks

Open separate terminals and run:

**Terminal 1:**
```bash
cd ~/Documents/RoboCode
python Submissions/ClaudeCode/final_boss_tank_gui.py
```

**Terminal 2:**
```bash
python Samples/sitting_duck_gui.py  # Coming soon!
```

Or create your own GUI tank (see below)!

---

## 🎯 Creating Your Own GUI Tank

Simple template:

```python
import asyncio
from robocode_tank_royale.bot_api import BaseBot

class MyTank(BaseBot):
    async def run(self):
        """Main loop"""
        while True:
            self.forward = 100
            self.turn_radar_right(30)
            await self.go()  # IMPORTANT: Must call go()!

    def on_scanned_bot(self, event):
        """Fire when you see an enemy"""
        self.fire(2)

if __name__ == "__main__":
    bot = MyTank()
    asyncio.run(bot.start())
```

Save as `my_tank.py` and run:
```bash
python my_tank.py
```

---

## 📋 Key Differences: Validation vs GUI Tanks

| Feature | Validation Tanks | GUI Tanks |
|---------|------------------|-----------|
| **Parent Class** | None (standalone) | `BaseBot` |
| **Methods** | `self.forward = X`, `self.turn_body = X` | `forward()`, `self.turn_body = X` |
| **Run Loop** | `def run(self):` | `async def run(self):` |
| **Turn Execution** | Automatic | `await self.go()` |
| **Usage** | `battle_runner.py` | Visual GUI battles |
| **JSON Config** | Optional | Required (auto-loaded) |

---

## 🔄 Converting Validation Tank to GUI Tank

**Before (Validation):**
```python
class MyTank:
    def run(self):
        self.ahead(50)
        self.turn_body = 30
```

**After (GUI):**
```python
import asyncio
from robocode_tank_royale.bot_api import BaseBot

class MyTankGUI(BaseBot):
    async def run(self):
        while True:
            self.forward = 50
            self.turn_body = 30
            await self.go()

if __name__ == "__main__":
    bot = MyTankGUI()
    asyncio.run(bot.start())
```

---

## 📝 Available GUI Tanks

Currently available:
- ✅ `final_boss_tank_gui.py` - FinalBoss for GUI

**Coming soon** - I can create GUI versions of:
- `challenger_tank.py`
- All sample tanks
- All tutorial tanks

Just ask!

---

## 🎮 Ready to Battle!

1. Server running ✅
2. Browser at localhost:8080 ✅
3. Run: `python final_boss_tank_gui.py` ✅
4. Select bot in browser ✅
5. Click "Start Battle" ✅
6. **WATCH!** 🎉

---

## 🆘 Still Having Issues?

Check `SETUP_GUI.md` for detailed troubleshooting!
