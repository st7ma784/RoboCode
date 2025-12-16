# 🚀 Install Tank Royale Server

## You Have the .deb Files! Let's Install Them

I found these in your `~/Downloads`:
- `robocode-tank-royale-server_0.34.2_amd64.deb`
- `robocode-tank-royale-gui_0.34.2_amd64.deb`
- `robocode-tank-royale-booter_0.34.2_amd64.deb`
- `robocode-tank-royale-recorder_0.34.2_amd64.deb`

---

## 📦 Installation Steps

### Step 1: Install the Packages

```bash
cd ~/Downloads

# Install server (required)
sudo dpkg -i robocode-tank-royale-server_0.34.2_amd64.deb

# Install GUI (optional but recommended)
sudo dpkg -i robocode-tank-royale-gui_0.34.2_amd64.deb

# Install booter (optional)
sudo dpkg -i robocode-tank-royale-booter_0.34.2_amd64.deb

# Fix any missing dependencies
sudo apt-get install -f
```

### Step 2: Verify Installation

```bash
# Check if installed
which robocode-tank-royale-server

# Should output something like:
# /usr/bin/robocode-tank-royale-server
```

---

## 🎮 Starting the Server

### Method 1: Command Line

```bash
robocode-tank-royale-server
```

**You should see:**
```
Starting Robocode Tank Royale Server
Server running on port 7654
UI available at http://localhost:8080
```

**Keep this terminal open!**

### Method 2: Use the Helper Script

```bash
cd ~/Documents/RoboCode
./start_server.sh
```

### Method 3: GUI Launcher (if you installed the GUI package)

```bash
robocode-tank-royale-gui
```

---

## 🌐 Test It Works

### Open Browser

Go to: **http://localhost:8080**

You should see the Tank Royale arena! 🎮

If you see the interface, **SUCCESS!** ✅

---

## 🐋 Alternative: Use Docker (No Installation!)

If you have Docker, this is even easier:

```bash
# One command to start server
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
```

**Pros:**
- No installation needed
- Always latest version
- Easy to stop/start

**Cons:**
- Requires Docker installed
- Slightly slower startup

---

## 🔧 Troubleshooting

### "dpkg: error processing package"

**Fix missing dependencies:**
```bash
sudo apt-get update
sudo apt-get install -f
```

### "robocode-tank-royale-server: command not found"

**Check if installed:**
```bash
dpkg -l | grep robocode
```

**If not listed, install again:**
```bash
cd ~/Downloads
sudo dpkg -i robocode-tank-royale-server_0.34.2_amd64.deb
```

### Server Starts But Browser Can't Connect

**Check if server is actually running:**
```bash
# Check process
ps aux | grep robocode

# Check ports
netstat -tln | grep -E '7654|8080'
```

**You should see:**
```
tcp6  0  0  :::7654   :::*   LISTEN
tcp6  0  0  :::8080   :::*   LISTEN
```

**Try localhost instead of 127.0.0.1:**
```
http://localhost:8080  ← Try this
http://127.0.0.1:8080  ← Or this
```

### "Address already in use"

**Something else is using port 8080 or 7654:**

```bash
# Find what's using the port
sudo lsof -i :8080
sudo lsof -i :7654

# Kill it (replace PID with actual process ID)
kill <PID>
```

---

## 📝 Quick Reference

### Start Server
```bash
robocode-tank-royale-server
```

### Stop Server
```
Ctrl+C in the terminal where it's running
```

### Check If Running
```bash
ps aux | grep robocode
netstat -tln | grep 8080
```

### Uninstall (if needed)
```bash
sudo dpkg -r robocode-tank-royale-server
sudo dpkg -r robocode-tank-royale-gui
```

---

## ✅ After Installation

Once server is running and browser shows the arena:

1. **Launch tanks:** `python tank.py`
2. **Select tanks** in browser
3. **Start battle!**

See `START_GUI_BATTLE_NOW.md` for the complete battle workflow!

---

## 🎯 Complete Workflow

```bash
# Terminal 1: Start server
robocode-tank-royale-server

# Terminal 2: Launch tank
cd ~/Documents/RoboCode
python Submissions/ClaudeCode/final_boss_tank_gui.py

# Browser: http://localhost:8080
# Select tank → Start Battle → Watch! 🎮
```

---

## 🚀 You're Ready!

After installation:
- ✅ Server installed
- ✅ Can run: `robocode-tank-royale-server`
- ✅ Browser works at localhost:8080
- ✅ Ready for battles!

**Install it now and start battling!** 🎮
