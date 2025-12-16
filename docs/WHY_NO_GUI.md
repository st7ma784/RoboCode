# Why Your Tanks Don't Work in the GUI

## Quick Answer

**Your tanks use a simplified Python structure that's incompatible with the official RoboCode Tank Royale GUI.**

This is **intentional** - the simplified system is better for learning!

## The Two Systems

### Your System (Custom - For Learning)

**Tank Structure:**
```python
class MyTank:
    def run(self):
        self.ahead(50)
        self.fire(2)
    
    def on_scanned_robot(self, event):
        self.fire(3)
```

**Benefits:**
- ✅ Simple Python classes
- ✅ Easy to understand
- ✅ Kid-friendly error messages
- ✅ Fast testing with `battle_runner.py`
- ✅ No complex dependencies

**Testing:**
```bash
python battle_runner.py your_tank.py Samples/sitting_duck.py
```

---

### Official GUI System (Robocode Tank Royale)

**Tank Structure:**
```python
from robocode_tank_royale.bot_api import BaseBot

class MyTank(BaseBot):
    def run(self):
        while self.is_running():
            self.forward(50)
            self.fire(2)
    
    def on_scanned_bot(self, event):
        self.fire(3)

# Must call start()
if __name__ == "__main__":
    bot = MyTank()
    bot.start()
```

**Requirements:**
- Must inherit from `BaseBot`
- Different method names (`forward` vs `ahead`, `on_scanned_bot` vs `on_scanned_robot`)
- Needs `robocode-tank-royale` package installed
- Must connect to GUI server
- More complex setup

## Why Your Tanks Don't Have `.start()`

The `.start()` method is part of the official RoboCode Tank Royale API. It:
1. Connects to the GUI server (localhost:7654)
2. Registers the bot
3. Waits for battle commands
4. Runs your `run()` method in a loop

**Your simplified tanks don't need this** because `battle_runner.py` handles all the battle simulation internally!

## What Should You Do?

### For Learning (Recommended): Stick With What You Have

```bash
# Your current system works great!
python battle_runner.py your_tank.py --all-samples
```

**Advantages:**
- Focus on Python and strategy
- No GUI complexity
- Faster development cycle
- Better error messages for beginners

### For Visual Battles (Optional): Convert Your Tanks

If you want to see animated battles, you need to:

1. **Install the official package:**
   ```bash
   pip install robocode-tank-royale
   ```

2. **Rewrite your tank** to use the official API:
   - Inherit from `BaseBot`
   - Change method names
   - Add connection logic
   - Handle the game loop differently

3. **Download and run the GUI server:**
   - Get it from: https://github.com/robocode-dev/tank-royale/releases
   - Run the server
   - Open browser to http://localhost:8080

4. **Run your converted tank:**
   ```bash
   python your_official_tank.py
   ```

## Comparison Example

### Your Current Tank (Sitting Duck):
```python
class SittingDuck:
    def run(self):
        self.turn_radar_right(45)
    
    def on_scanned_robot(self, scanned):
        self.fire(2)
```

### Official API Version:
```python
from robocode_tank_royale.bot_api import BaseBot

class SittingDuck(BaseBot):
    def run(self):
        while self.is_running():
            self.turn_radar_right(45)
            self.go()  # Execute pending commands
    
    def on_scanned_bot(self, event):
        self.fire(2)

if __name__ == "__main__":
    bot = SittingDuck()
    bot.start()  # This connects to GUI server
```

**Notice the differences:**
- Inheritance from `BaseBot`
- `while self.is_running()` loop
- `on_scanned_bot` instead of `on_scanned_robot`
- `self.go()` to execute commands
- `bot.start()` at the end

## Bottom Line

🎯 **For this tutorial series, use `battle_runner.py`** - it's simpler and better for learning!

🎮 **The GUI is optional** - visual battles are cool, but not necessary for learning Python and strategy.

🔧 **Converting to the GUI is advanced** - only do this after you're comfortable with Python and tank programming.

## Still Want the GUI?

See the official docs:
- https://robocode-dev.github.io/tank-royale/
- https://github.com/robocode-dev/tank-royale

Or create an issue and we can help you convert a tank!
