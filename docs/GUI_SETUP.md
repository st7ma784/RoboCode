# RoboCode Tank Royale GUI Setup Guide

## ⚠️ IMPORTANT: Two Different Systems

**This project uses a SIMPLIFIED tank system** that is different from the official RoboCode Tank Royale GUI!

### What You Have (Custom System):
- ✅ **Plain Python classes** - No complex inheritance needed
- ✅ **`battle_runner.py`** - Tests your tanks work correctly
- ✅ **Beginner-friendly** - Perfect for learning Python
- ❌ **No GUI** - Text-based output only

### What the Official GUI Needs:
- 🔧 Tanks must inherit from `BaseBot` class
- 🔧 Must use official `robocode-tank-royale` API
- 🔧 Different method signatures and structure
- ✅ **Visual battles** - Watch tanks fight with graphics

## The Problem

**Your sample tanks are NOT compatible with the official GUI!** They use a simplified structure for learning. To use the GUI, you would need to completely rewrite your tanks using the official API.

## Recommended Solution: Use What You Have!

**Your `battle_runner.py` already works perfectly for learning!** No GUI needed:

```bash
# Test your tank
python battle_runner.py YourTank/your_tank.py Samples/sitting_duck.py

# Fight all sample opponents
python battle_runner.py YourTank/your_tank.py --all-samples

# Quick validation
python battle_runner.py YourTank/your_tank.py --test
```

This is actually **better for beginners** because:
- ✅ Simpler code structure
- ✅ Faster testing
- ✅ Better error messages
- ✅ No complex setup needed

---

## Alternative: Convert to Official API (Advanced)

If you **really** want the GUI, here's what you need to do:

### Step 1: Install Python Package

```bash
# Make sure you're in the RoboCode directory
cd /home/user/Documents/RoboCode

# Install the Python bot API
pip install robocode-tank-royale>=0.20.0

# OR install everything at once
pip install -r requirements.txt
```

Verify installation:
```bash
python -c "import robocode; print('✓ Robocode installed!')"
```

### Step 2: Download & Run the GUI Server

**Option A: Pre-built Release (Easiest)**

1. Download from: https://github.com/robocode-dev/tank-royale/releases
2. Get the latest version for your OS (Linux/Windows/Mac)
3. Extract the ZIP file
4. Run the server:
   ```bash
   # Linux/Mac
   ./robocode-tank-royale-server
   
   # Windows
   robocode-tank-royale-server.exe
   ```

**Option B: Using Docker**

```bash
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
```

**Option C: Build from Source (Advanced)**

```bash
git clone https://github.com/robocode-dev/tank-royale.git
cd tank-royale
./gradlew build
./gradlew run
```

### Step 3: Access the GUI

Once the server is running:

1. Open your web browser
2. Go to: **http://localhost:8080**
3. You should see the Tank Royale interface!

### Step 4: Configure Bot Directory

The GUI needs to know where your Python tanks are located.

**In the GUI:**
1. Click **Settings** (⚙️ icon)
2. Go to **Bot Directories**
3. Add this path: `/home/user/Documents/RoboCode`
4. Click **Save**
5. Click **Rescan Bots**

### Step 5: Verify Your Tanks Appear

Check if you see these sample tanks:
- ✅ SittingDuck
- ✅ SpinBot
- ✅ WallsBot
- ✅ TrackerBot
- ✅ ChampionBot

If you see them, **you're ready to battle!** 🎉

## Understanding the JSON Files

Each Python tank needs a matching `.json` file. For example:

**File: `sitting_duck.py`** (your Python code)
**File: `sitting_duck.json`** (metadata for GUI)

### JSON File Structure

```json
{
  "name": "MyTank",
  "version": "1.0.0",
  "authors": ["Your Name"],
  "description": "My awesome tank",
  "gameTypes": ["melee", "1v1"],
  "platform": "Python",
  "programmingLang": "Python 3.10+",
  "botClass": "MyTank",
  "botModule": "my_tank"
}
```

**Key fields:**
- `botClass` - The class name in your Python file
- `botModule` - Python filename without `.py` extension

## Creating JSON for Your Own Tanks

### Quick Method: Copy & Modify

```bash
# Copy an existing JSON
cp Samples/sitting_duck.json Submissions/YourName/your_tank.json

# Edit it with your tank's details
nano Submissions/YourName/your_tank.json
```

### Example: Creating JSON for `my_cool_tank.py`

If your Python file is:
```python
class MyCoolTank:
    def run(self):
        # ... your code
```

Create `my_cool_tank.json`:
```json
{
  "name": "MyCoolTank",
  "version": "1.0.0",
  "authors": ["Your Name"],
  "description": "My first tank!",
  "gameTypes": ["melee", "1v1"],
  "platform": "Python",
  "programmingLang": "Python 3.8+",
  "botClass": "MyCoolTank",
  "botModule": "my_cool_tank"
}
```

**Rules:**
- JSON filename matches Python filename (both lowercase with underscores)
- `botClass` matches your Python class name (CamelCase)
- `botModule` is the filename without `.py`

## Running Battles in the GUI

1. **Start a Battle:**
   - Click "Battle"
   - Select 2+ tanks from the list
   - Choose arena size
   - Click "Start Battle"

2. **Watch the Action:**
   - See tanks moving and shooting in real-time
   - View scores and energy bars
   - Watch the kill feed

3. **Review Results:**
   - See final rankings
   - Check damage dealt/taken
   - Review survival time

## Troubleshooting

### "No bots found"

**Fix:**
1. Check bot directory is correct: `/home/user/Documents/RoboCode`
2. Make sure JSON files exist for all tanks
3. Click "Rescan Bots" in settings
4. Check console for errors

### "Bot failed to start"

**Fix:**
1. Make sure `robocode-tank-royale` is installed
2. Check Python syntax:
   ```bash
   python your_tank.py
   ```
3. Verify class name matches JSON `botClass`
4. Check Python version (need 3.8+)

### "Module not found" error

**Fix:**
```bash
pip install robocode-tank-royale
# or
pip install -r requirements.txt
```

### JSON syntax errors

**Common mistakes:**
- ❌ Missing comma after item
- ❌ Extra comma at end of list
- ❌ Wrong quote type (use `"` not `'`)
- ❌ Unescaped special characters

**Validate JSON:**
```bash
python -m json.tool your_tank.json
```

### Can't connect to server

**Fix:**
1. Make sure server is running (check terminal)
2. Try http://localhost:8080 in browser
3. Check if port 8080 is already in use:
   ```bash
   lsof -i :8080
   ```
4. Try different port in server settings

## Testing Without GUI

You can test tanks work without the GUI:

```bash
# Test Python syntax
python Samples/sitting_duck.py

# Run automated battles (no GUI needed)
python battle_runner.py Samples/sitting_duck.py Samples/spin_bot.py
```

## Quick Reference

### File Structure
```
YourTank/
├── your_tank.py       ← Python code
└── your_tank.json     ← Metadata for GUI
```

### Essential Commands
```bash
# Install Python API
pip install robocode-tank-royale

# Check syntax
python your_tank.py

# Validate JSON
python -m json.tool your_tank.json

# Start GUI server (if built from source)
./gradlew run
```

### Important URLs
- **GUI**: http://localhost:8080
- **Server API**: http://localhost:7654
- **Releases**: https://github.com/robocode-dev/tank-royale/releases
- **Documentation**: https://robocode-dev.github.io/tank-royale/

## Next Steps

1. ✅ Verify all sample tanks appear in GUI
2. ✅ Run a test battle with sample tanks
3. ✅ Create JSON for your custom tanks
4. ✅ Test your tanks in the GUI
5. ✅ Have fun! 🚀

---

**Still having issues?** Check the server console for error messages or open an issue on GitHub!
