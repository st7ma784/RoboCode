# BaseBot API Guide

## Overview

All bots in this repository use the **BaseBot API** from Robocode Tank Royale, which uses **property assignments** instead of method calls for control commands.

## ⚠️ Important Differences from Classic Robocode

| Classic Robocode | BaseBot API | Description |
|------------------|-------------|-------------|
| `self.turn_right(45)` | `self.turn_body = 45` | Turn body right (positive degrees) |
| `self.turn_left(45)` | `self.turn_body = -45` | Turn body left (negative degrees) |
| `self.forward(100)` | `self.forward = 100` | Move forward (positive distance) |
| `self.back(50)` | `self.forward = -50` | Move backward (negative distance) |
| `self.turn_gun_right(30)` | `self.turn_gun = 30` | Turn gun right |
| `self.turn_gun_left(30)` | `self.turn_gun = -30` | Turn gun left |
| `self.turn_radar_right(45)` | `self.turn_radar = 45` | Turn radar right |
| `self.turn_radar_left(45)` | `self.turn_radar = -45` | Turn radar left |
| `self.fire(3)` | `await self.fire(3)` | Fire bullet (must await!) |

## Key Concepts

### 1. Property-Based Control

Instead of calling methods, you **assign values to properties**:

```python
# ❌ WRONG (Classic Robocode style)
self.turn_right(90)
self.forward(100)
self.fire(2)

# ✅ CORRECT (BaseBot API)
self.turn_body = 90
self.forward = 100
await self.fire(2)
```

### 2. Positive/Negative Values

Turning and movement use positive/negative values instead of separate methods:

```python
# Turn right 45 degrees
self.turn_body = 45

# Turn left 45 degrees  
self.turn_body = -45

# Move forward 100 units
self.forward = 100

# Move backward 50 units
self.forward = -50
```

### 3. Async/Await Pattern

All bots and event handlers must use async/await:

```python
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class MyBot(BaseBot):
    async def run(self):
        """Main loop - must be async"""
        while self.is_running():
            self.turn_radar = 45
            self.forward = 50
            await self.go()  # Execute turn
    
    async def on_scanned_bot(self, event):
        """Event handler - must be async"""
        await self.fire(3)  # Actions must be awaited
```

### 4. Game Loop Control

Use `while self.is_running():` instead of `while True:`:

```python
# ❌ WRONG - Never exits
while True:
    self.turn_radar = 45
    await self.go()

# ✅ CORRECT - Exits when game ends
while self.is_running():
    self.turn_radar = 45
    await self.go()
```

### 5. The go() Method

`await self.go()` sends your commands to the server and advances one game tick:

```python
async def run(self):
    while self.is_running():
        # Set commands
        self.turn_body = 10
        self.forward = 50
        self.turn_radar = 45
        
        # Execute all commands and advance one tick
        await self.go()
```

## Common Patterns

### Basic Movement

```python
# Move forward
self.forward = 100
await self.go()

# Move backward
self.forward = -50
await self.go()

# Turn while moving
self.turn_body = 90
self.forward = 100
await self.go()
```

### Scanning and Shooting

```python
async def run(self):
    while self.is_running():
        # Sweep radar
        self.turn_radar = 45
        await self.go()

async def on_scanned_bot(self, event):
    # Aim at enemy
    gun_angle = self.calculate_gun_angle(event.x, event.y)
    self.turn_gun = gun_angle
    
    # Fire
    await self.fire(2)
```

### Helper Methods for Compatibility

If you want methods like `turn_right()` for convenience:

```python
class MyBot(BaseBot):
    def turn_right(self, degrees):
        """Helper to turn right"""
        self.turn_body = degrees
    
    def turn_left(self, degrees):
        """Helper to turn left"""
        self.turn_body = -degrees
    
    async def run(self):
        while self.is_running():
            self.turn_right(90)  # Uses helper
            await self.go()
```

## Event Handlers

All event handlers must be async and use await for actions:

```python
async def on_scanned_bot(self, event):
    """Called when radar scans an enemy"""
    await self.fire(1)

async def on_hit_by_bullet(self, event):
    """Called when hit by bullet"""
    self.turn_body = 90
    await self.go()

async def on_hit_wall(self, event):
    """Called when hitting a wall"""
    self.forward = -100  # Back up
    await self.go()
```

## Complete Example

```python
from robocode_tank_royale.bot_api import BaseBot, BotInfo
import asyncio

class MyFirstBot(BaseBot):
    """Example bot using BaseBot API"""
    
    async def run(self):
        """Main game loop"""
        while self.is_running():
            # Scan for enemies
            self.turn_radar = 45
            
            # Move in a pattern
            self.forward = 100
            self.turn_body = 10
            
            # Execute turn
            await self.go()
    
    async def on_scanned_bot(self, event):
        """Fire when we see an enemy"""
        # Calculate aim
        bearing = event.bearing
        self.turn_gun = bearing
        
        # Fire based on distance
        if event.distance < 200:
            await self.fire(3)
        else:
            await self.fire(1)
    
    async def on_hit_by_bullet(self, event):
        """Dodge when hit"""
        self.turn_body = 90
        self.forward = 100
        await self.go()

if __name__ == "__main__":
    bot_info = BotInfo.from_file("my_first_bot.json")
    bot = MyFirstBot(bot_info=bot_info)
    asyncio.run(bot.start())
```

## Troubleshooting

### Bot doesn't move

**Problem:** Using method calls instead of property assignments

```python
# ❌ WRONG
self.turn_right(90)
self.forward(100)

# ✅ CORRECT
self.turn_body = 90
self.forward = 100
```

### "await outside async function" error

**Problem:** Event handler not marked as async

```python
# ❌ WRONG
def on_scanned_bot(self, event):
    await self.fire(3)

# ✅ CORRECT
async def on_scanned_bot(self, event):
    await self.fire(3)
```

### Bot never exits/timeouts

**Problem:** Using `while True:` instead of `while self.is_running():`

```python
# ❌ WRONG
while True:
    await self.go()

# ✅ CORRECT
while self.is_running():
    await self.go()
```

### Actions don't execute

**Problem:** Forgetting to call `await self.go()`

```python
# ❌ WRONG - Commands set but never executed
self.turn_body = 90
self.forward = 100
# Missing await self.go()!

# ✅ CORRECT
self.turn_body = 90
self.forward = 100
await self.go()
```

## Resources

- [Official BaseBot API Documentation](https://robocode-dev.github.io/tank-royale/api/python/)
- [Tank Royale GitHub](https://github.com/robocode-dev/tank-royale)
- [Sample Bots](../Samples/)
- [Tutorials](../Tutorials/)

## Migration Checklist

If migrating from classic Robocode or old Bot API:

- [ ] Change all `turn_right()` to `self.turn_body = X`
- [ ] Change all `turn_left()` to `self.turn_body = -X`
- [ ] Change all `forward()` to `self.forward = X`
- [ ] Change all `back()` to `self.forward = -X`
- [ ] Make all event handlers `async`
- [ ] Add `await` before `fire()`, `rescan()`, etc.
- [ ] Change `while True:` to `while self.is_running():`
- [ ] Add `await self.go()` in main loop
- [ ] Import from `robocode_tank_royale.bot_api` not `robocode`
- [ ] Use `BaseBot` not `Bot` or `AdvancedRobot`
