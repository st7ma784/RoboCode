# 🎮 How to Add Tanks to the GUI

## ⚠️ CRITICAL CONCEPT

**Tanks don't "appear" in the GUI automatically!**

You must **RUN each tank as a separate process** to connect it to the server.

---

## 📺 Visual Process

```
┌─────────────────────────────────────────┐
│  1. Tank Royale Server Running          │
│     Port 7654 (WebSocket)               │
│     Port 8080 (Browser UI)              │
└─────────────────────────────────────────┘
                  ↓ ↓ ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Terminal 1  │ │  Terminal 2  │ │  Terminal 3  │
│              │ │              │ │              │
│  Run Tank 1  │ │  Run Tank 2  │ │  Run Tank 3  │
│  ↓           │ │  ↓           │ │  ↓           │
│  Connects    │ │  Connects    │ │  Connects    │
└──────────────┘ └──────────────┘ └──────────────┘
                  ↓ ↓ ↓
┌─────────────────────────────────────────┐
│  Browser: http://localhost:8080         │
│                                         │
│  ☑ Tank 1                               │
│  ☑ Tank 2                               │
│  ☑ Tank 3                               │
│                                         │
│  [Start Battle] button                  │
└─────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step Example

### Prerequisites

**1. Tank Royale Server must be running:**
```bash
# You should see this message:
Server running on port 7654
UI available at http://localhost:8080
```

**2. Browser open to:**
```
http://localhost:8080
```

---

### Step 1: Open Terminal 1 - Launch First Tank

```bash
cd ~/Documents/RoboCode
python Submissions/ClaudeCode/final_boss_tank_gui.py
```

**What you'll see:**
```
Connecting to ws://localhost:7654...
Connected!
Waiting for game to start...
```

**In browser:** You'll see "FinalBossTankGUI" appear in the bot list! ✅

**Keep this terminal open!** The bot must keep running to stay connected.

---

### Step 2: Open Terminal 2 - Launch Second Tank

```bash
cd ~/Documents/RoboCode

# Create a quick demo tank
cat > /tmp/simple_tank.py << 'EOF'
import asyncio
import os
from robocode_tank_royale.bot_api import BaseBot

class SimpleTank(BaseBot):
    async def run(self):
        while True:
            self.forward(100)
            self.turn_right(30)
            await self.go()

    def on_scanned_bot(self, event):
        self.fire(2)

if __name__ == "__main__":
    # Set bot info via environment variables
    os.environ['BOT_NAME'] = 'SimpleTank'
    os.environ['BOT_VERSION'] = '1.0'
    os.environ['BOT_AUTHORS'] = 'Demo'
    bot = SimpleTank()
    asyncio.run(bot.start())
EOF

# Run it
python /tmp/simple_tank.py
```

**In browser:** "SimpleTank" now appears! ✅

---

### Step 3: Select Tanks in Browser

In your browser at `http://localhost:8080`:

1. You'll see a list like:
   ```
   Available Bots:
   ☐ FinalBossTankGUI
   ☐ SimpleTank
   ```

2. **Check the boxes** next to the tanks you want in the battle

3. Click the **"Start Battle"** button

4. **WATCH THE BATTLE!** 🎮💥

---

## 🎯 Common Mistakes

### ❌ Mistake 1: Expecting tanks to auto-appear

**Wrong thinking:**
> "I have tank files, why don't they show up in the GUI?"

**Reality:**
> Tank files must be RUN as Python processes to connect to the server.

### ❌ Mistake 2: Closing terminals

**Wrong:**
```bash
python tank.py
# Close terminal ← WRONG! Tank disconnects!
```

**Right:**
```bash
python tank.py
# Keep terminal open ← Tank stays connected!
```

### ❌ Mistake 3: Trying to run non-GUI tanks

**Wrong:**
```bash
python final_boss_tank.py  # ← This is a validation tank!
```

**Right:**
```bash
python final_boss_tank_gui.py  # ← This is a GUI tank!
```

---

## 🔧 Quick Reference Commands

### Launch GUI Tanks

**Your custom tanks:**
```bash
# Terminal 1
python Submissions/ClaudeCode/final_boss_tank_gui.py

# Terminal 2
# (Create challenger_tank_gui.py first!)
python Submissions/ClaudeCode/challenger_tank_gui.py
```

**Quick demo opponent:**
```bash
# Create simple tank on the fly
cat > /tmp/demo.py << 'EOF'
import asyncio, os
from robocode_tank_royale.bot_api import BaseBot

class Demo(BaseBot):
    async def run(self):
        while True:
            self.forward(100)
            self.turn_radar_right(45)
            await self.go()
    def on_scanned_bot(self, e): self.fire(2)

if __name__ == "__main__":
    os.environ.update({'BOT_NAME': 'Demo', 'BOT_VERSION': '1.0', 'BOT_AUTHORS': 'You'})
    asyncio.run(Demo().start())
EOF

python /tmp/demo.py
```

---

## 🎓 Understanding the System

### How Bots Connect

1. **Bot starts:** `python tank.py`
2. **Bot reads config:** From JSON or environment variables
3. **Bot connects:** Opens WebSocket to `ws://localhost:7654`
4. **Server registers bot:** Adds to available bots list
5. **Browser shows bot:** You see it in the UI
6. **You start battle:** Bots fight!

### Why Keep Terminals Open?

Each bot is a **separate Python process**:
- Close terminal = kill process = bot disconnects
- Keep terminal open = bot stays in battle

### Multiple Battles

Want to run another battle?
1. **Keep the same bots running** (don't close terminals!)
2. **Just click "Start Battle" again** in browser
3. Bots will join the new battle automatically

---

## 📝 Checklist: Adding Your Tank to GUI

- [ ] Tank inherits from `BaseBot`
- [ ] Tank has `async def run(self):` with `await self.go()`
- [ ] Tank has JSON config file or env vars set
- [ ] Server is running (check port 7654)
- [ ] Browser open to `localhost:8080`
- [ ] Run: `python your_tank.py` in terminal
- [ ] See bot appear in browser list
- [ ] Select bot and click "Start Battle"
- [ ] Watch it fight! 🎮

---

## 🚀 Quick Demo Script

I created a demo script for you:

```bash
cd ~/Documents/RoboCode
./demo_gui_battle.sh
```

This will:
1. Guide you through starting tanks
2. Show them appearing in browser
3. Help you run your first GUI battle!

---

## 💡 Pro Tips

1. **Use tmux or screen** to manage multiple tank terminals easily

2. **Create a launch script:**
   ```bash
   #!/bin/bash
   python tank1.py &
   python tank2.py &
   python tank3.py &
   echo "All tanks launched!"
   ```

3. **Kill all tanks at once:**
   ```bash
   pkill -f "python.*tank.*\.py"
   ```

4. **Check what tanks are running:**
   ```bash
   ps aux | grep "python.*tank"
   ```

---

## 🎮 You're Ready!

Now you know:
- ✅ Tanks must be RUN to appear
- ✅ Each tank = separate terminal
- ✅ Keep terminals open
- ✅ Select tanks in browser
- ✅ Start battle and watch!

**Go try it!** Run `./demo_gui_battle.sh` for a guided demo! 🚀
