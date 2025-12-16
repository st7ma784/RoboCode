# 🎮 START GUI BATTLE NOW - Copy/Paste Commands

## ⚡ 5-Minute Quick Start

### Terminal 1: Start Server (if not already running)

Download from: https://github.com/robocode-dev/tank-royale/releases

Or use Docker:
```bash
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
```

### Terminal 2: Open Browser

Go to: **http://localhost:8080**

### Terminal 3: Launch Tank 1

```bash
cd ~/Documents/RoboCode
python Submissions/ClaudeCode/final_boss_tank_gui.py
```

**You'll see in browser:** "FinalBossTankGUI" appears! ✅

### Terminal 4: Launch Tank 2 (Quick Demo Opponent)

```bash
cd ~/Documents/RoboCode
python3 -c "
import asyncio
import os
from robocode_tank_royale.bot_api import BaseBot

class QuickBot(BaseBot):
    async def run(self):
        while True:
            self.forward = 100
            self.turn_body = 30
            self.turn_radar_right(45)
            await self.go()

    def on_scanned_bot(self, event):
        self.fire(2)

if __name__ == '__main__':
    os.environ['BOT_NAME'] = 'QuickBot'
    os.environ['BOT_VERSION'] = '1.0'
    os.environ['BOT_AUTHORS'] = 'Demo'
    bot = QuickBot()
    asyncio.run(bot.start())
"
```

**You'll see in browser:** "QuickBot" appears! ✅

### Browser: Start Battle

1. Check boxes next to both tanks
2. Click **"Start Battle"**
3. **WATCH THEM FIGHT!** 💥

---

## 🎯 The Key Understanding

**Tanks appear in GUI by RUNNING them as processes!**

```
Run tank.py → Bot connects to server → Appears in browser
```

**NOT:**
```
Have tank.py file → Magically appears (NO! Must run it!)
```

---

## 📋 All Commands in One Place

```bash
# Terminal 1: Server (if needed)
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server

# Terminal 2: Your tank
cd ~/Documents/RoboCode
python Submissions/ClaudeCode/final_boss_tank_gui.py

# Terminal 3: Opponent tank (inline)
python3 -c "
import asyncio, os
from robocode_tank_royale.bot_api import BaseBot
class Bot(BaseBot):
    async def run(self):
        while True:
            self.forward = 100; self.turn_body = 30; await self.go()
    def on_scanned_bot(self, e): self.fire(2)
os.environ.update({'BOT_NAME':'QuickBot','BOT_VERSION':'1.0','BOT_AUTHORS':'Demo'})
asyncio.run(Bot().start())
"

# Browser: http://localhost:8080
# Select tanks → Click "Start Battle"
```

---

## 🔧 Troubleshooting

**"No tanks appear in browser"**
- Server running? Check terminal for "Server running on port 7654"
- Tanks running? Check terminals are still open and no errors
- Refresh browser

**"Connection refused"**
- Start server first!
- Check `http://localhost:8080` loads

**"Module not found"**
```bash
python -m pip install -r requirements.txt
```

---

## 🎮 That's It!

You now know how to add tanks to the GUI:
1. ✅ Run tank as Python process
2. ✅ It connects to server
3. ✅ Appears in browser
4. ✅ Select and battle!

**Try the demo script for guided walkthrough:**
```bash
./demo_gui_battle.sh
```
