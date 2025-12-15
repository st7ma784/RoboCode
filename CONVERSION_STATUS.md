# BaseBot Conversion Status

## ✅ Completed Conversions

### Samples (5/5 files) ✓
- ✅ `Samples/sitting_duck.py`
- ✅ `Samples/spin_bot.py`
- ✅ `Samples/walls_bot.py`
- ✅ `Samples/tracker_bot.py`
- ✅ `Samples/champion_bot.py`

### Tutorials (3/8 files)
- ✅ `Tutorials/Week1_MyFirstTank/my_first_tank.py`
- ✅ `Tutorials/Week2_Trigonometry/predictor_bot.py`
- ✅ `Tutorials/Week3_BoundaryChecking/boundary_bot.py`
- ⏳ `Tutorials/Week4_Strategy/trickster_bot.py` - NEEDS CONVERSION
- ⏳ `Tutorials/Week5_AdvancedTargeting/sniper_bot.py` - NEEDS CONVERSION
- ⏳ `Tutorials/Week6_AdvancedPython/professional_tank.py` - NEEDS CONVERSION
- ⏳ `Tutorials/Week7_AdvancedSkirmisher/skirmisher_tank.py` - NEEDS CONVERSION
- ⏳ `Tutorials/Week8_AntiGravitySwarms/anti_gravity_tank.py` - NEEDS CONVERSION

### Submissions (1/4 files)
- ✅ `Submissions/ClaudeCode/final_boss_tank_gui.py` (already had BaseBot)
- ⏳ `Submissions/ClaudeCode/final_boss_tank.py` - NEEDS CONVERSION
- ⏳ `Submissions/ClaudeCode/challenger_tank.py` - NEEDS CONVERSION  
- ⏳ `Submissions/ExampleSubmission/example_tank.py` - NEEDS CONVERSION

## Conversion Pattern

All conversions follow this pattern:

### 1. Add Import
```python
from robocode_tank_royale.bot_api import BaseBot, BotInfo
```

### 2. Change Class Definition
```python
# OLD:
class MyTank:
    def __init__(self):
        self.name = "MyTank"
        self.x = 0
        self.y = 0
        # ...

# NEW:
class MyTank(BaseBot):
    """Tank description"""
    # No __init__ needed - BaseBot provides all properties
```

### 3. Convert run() Method
```python
# OLD:
def run(self):
    self.ahead(50)
    self.fire(1)

# NEW:
async def run(self):
    while True:
        self.forward(50)
        self.fire(1)
        await self.go()
```

### 4. Update Method Names
- `ahead()` → `forward()`
- Event parameters: `scanned_robot` → `event`, `hit_by_bullet` → `event`, etc.

### 5. Update Property Names
- `battlefield_width` → `arena_width`
- `battlefield_height` → `arena_height`
- `heading` → `direction`

### 6. Update Event Handlers
```python
# OLD:
def on_scanned_robot(self, scanned_robot):
    x = scanned_robot.x
    y = scanned_robot.y

# NEW:
def on_scanned_bot(self, event):
    # Calculate position from bearing
    bearing_rad = math.radians(event.bearing)
    x = self.x + event.distance * math.sin(bearing_rad)
    y = self.y + event.distance * math.cos(bearing_rad)
```

### 7. Add Main Entry Point
```python
if __name__ == "__main__":
    bot = MyTank()
    bot.start()
```

### 8. Remove Stub Methods
Delete all the empty pass methods at the end (turn_right, fire, etc.) - BaseBot provides them

## Quick Conversion Script

For remaining files, use this pattern:

```python
import re

def convert_tank_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add import if not present
    if 'from robocode_tank_royale.bot_api import BaseBot' not in content:
        content = content.replace(
            'import math',
            'import math\nfrom robocode_tank_royale.bot_api import BaseBot, BotInfo'
        )
    
    # Convert class definition
    content = re.sub(
        r'class (\w+):\s+def __init__\(self\):.*?(?=\n    def )',
        r'class \1(BaseBot):\n    """Converted tank"""\n\n    def ',
        content,
        flags=re.DOTALL
    )
    
    # Convert run method
    content = content.replace('def run(self):', 'async def run(self):')
    content = re.sub(
        r'(async def run\(self\):.*?""".*?""")',
        r'\1\n        while True:',
        content,
        flags=re.DOTALL
    )
    
    # Add await self.go() before method ends
    # (complex - needs manual review)
    
    # Update method names
    content = content.replace('.ahead(', '.forward(')
    content = content.replace('def on_scanned_robot(', 'def on_scanned_bot(')
    content = content.replace('def on_hit_by_bullet(', 'def on_hit_by_bullet(')
    
    # Update property names
    content = content.replace('self.battlefield_width', 'self.arena_width')
    content = content.replace('self.battlefield_height', 'self.arena_height')
    content = content.replace('self.heading', 'self.direction')
    
    # Add main entry point
    if 'if __name__ == "__main__"' not in content or 'test_' in content:
        content += '\n\nif __name__ == "__main__":\n    bot = [ClassName]()  # FIXME: Replace with actual class name\n    bot.start()\n'
    
    with open(filepath, 'w') as f:
        f.write(content)
```

## Testing After Conversion

Once converted, test each bot:

```bash
# Test individual bot
python Tutorials/Week4_Strategy/trickster_bot.py

# Test in GUI battle
python run_gui_battle.py Tutorials/Week4_Strategy/trickster_bot.py
```

## Common Issues

1. **"Bot doesn't move"** - Missing `await self.go()` in run loop
2. **"Can't get position"** - Using `scanned_robot.x` instead of calculating from `event.bearing`
3. **"AttributeError"** - Using old property names (`battlefield_width` vs `arena_width`)
4. **"Bot won't start"** - Missing `bot.start()` in `if __name__` block

## Next Steps

To finish the conversion:
1. Convert remaining tutorial bots (Weeks 4-8)
2. Convert submission bots
3. Test each bot individually
4. Run test battles
5. Update documentation to reflect BaseBot usage
