# Tank Utilities - Reusable Code for Your Tanks! 🛠️

## What is This?

`tank_utils.py` is a **shared toolbox** of helpful functions that many tanks need. Instead of copying the same code into every tank, we can just import these functions!

## Why Use Shared Code?

**Without tank_utils (The Old Way):**
```
Week2_bot.py: 150 lines (50 lines are math functions)
Week3_bot.py: 180 lines (50 lines are THE SAME math functions copied!)
Week4_bot.py: 200 lines (50 lines COPIED AGAIN!)
```
❌ Lots of duplicate code!
❌ If we fix a bug, we have to fix it in 10 places!
❌ Hard to maintain!

**With tank_utils (The Smart Way):**
```
tank_utils.py: 300 lines (all the shared functions in ONE place!)
Week2_bot.py: 100 lines (imports from tank_utils)
Week3_bot.py: 130 lines (imports from tank_utils)
Week4_bot.py: 150 lines (imports from tank_utils)
```
✅ No duplicate code!
✅ Fix a bug once, all tanks benefit!
✅ Easy to maintain!

## How to Use It

### Basic Import

```python
# At the top of your tank file:
from tank_utils import TankMath, TankTargeting, TankMovement

class YourTank(BaseBot):
    def on_scanned_bot(self, event):
        # Use the utility functions!
        distance = TankMath.calculate_distance(
            self.get_x(), self.get_y(),
            event.x, event.y
        )
        print(f"Enemy is {distance} pixels away!")
```

### Quick Aim Function

For simple tanks, use the one-liner:

```python
from tank_utils import quick_aim

class SimpleTank(BaseBot):
    def on_scanned_bot(self, event):
        # Automatically calculates prediction and aiming!
        turn_angle = quick_aim(self, event, fire_power=2)
        self.turn_gun_right(turn_angle)
        self.fire(2)
```

## Available Functions

### 📐 TankMath - Mathematical Helpers

#### `calculate_distance(from_x, from_y, to_x, to_y)`
Calculate distance between two points.

```python
distance = TankMath.calculate_distance(0, 0, 3, 4)
# Returns: 5.0 (the 3-4-5 triangle!)
```

#### `calculate_angle(from_x, from_y, to_x, to_y)`
Calculate angle from one point to another.

```python
angle = TankMath.calculate_angle(0, 0, 100, 0)
# Returns: 90.0 (pointing east)
```

#### `predict_position(x, y, velocity, heading, time)`
Predict where a moving target will be.

```python
future_x, future_y = TankMath.predict_position(
    100, 100,  # Current position
    5,         # Speed
    0,         # Heading (north)
    10         # Time (ticks)
)
# Returns: (100, 150) - moved 50 pixels north
```

#### `normalize_angle(angle)`
Convert any angle to -180 to 180 range.

```python
angle = TankMath.normalize_angle(450)
# Returns: 90.0
```

#### `bullet_speed(power)`
Calculate bullet speed based on fire power.

```python
speed = TankMath.bullet_speed(2)
# Returns: 14.0 pixels per tick
```

### 🎯 TankTargeting - Aiming Helpers

#### `aim_at_target(bot, target_x, target_y)`
Calculate gun turn angle to aim at a point.

```python
turn_angle = TankTargeting.aim_at_target(self, enemy_x, enemy_y)
self.turn_gun_right(turn_angle)
```

#### `lead_shot(bot, enemy_x, enemy_y, enemy_velocity, enemy_heading, fire_power)`
Calculate predictive shot (aims where enemy will be).

```python
aim_angle, future_x, future_y = TankTargeting.lead_shot(
    self,
    event.x, event.y,
    event.speed, event.direction,
    fire_power=2
)
self.turn_gun_right(aim_angle)
self.fire(2)
```

### 🚗 TankMovement - Navigation Helpers

#### `is_near_wall(bot, margin=50)`
Check if too close to any wall.

```python
if TankMovement.is_near_wall(self, margin=50):
    print("Too close to a wall!")
    # Turn away!
```

#### `find_nearest_wall(bot)`
Find which wall is closest.

```python
nearest = TankMovement.find_nearest_wall(self)
# Returns: "left", "right", "top", or "bottom"
```

#### `is_valid_target(bot, target_x, target_y, margin=20)`
Check if a target is inside arena bounds.

```python
future_x, future_y = TankMath.predict_position(...)

if TankMovement.is_valid_target(self, future_x, future_y):
    # Safe to shoot at predicted position
    self.fire(2)
else:
    # Enemy will hit wall, shoot at current position instead
    self.fire(1)
```

## Example: Before and After

### Before (Week 2 - Duplicate Code)

```python
class PredictorBot(BaseBot):
    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """Calculate distance - copied from tutorial"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle - copied from tutorial"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))
    
    def predict_position(self, x, y, velocity, heading, time):
        """Predict position - copied from tutorial"""
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y
    
    # ... 50+ more lines of helpers ...
    
    def on_scanned_bot(self, event):
        distance = self.calculate_distance(
            self.get_x(), self.get_y(), event.x, event.y
        )
        # ... use the functions ...
```

### After (Using tank_utils)

```python
from tank_utils import TankMath, TankTargeting

class PredictorBot(BaseBot):
    # No need to define helper functions!
    
    def on_scanned_bot(self, event):
        distance = TankMath.calculate_distance(
            self.get_x(), self.get_y(), event.x, event.y
        )
        # ... same logic, less code! ...
```

**Result:** Your tank file is **50+ lines shorter** and easier to read!

## When to Use tank_utils

✅ **Use tank_utils when:**
- You need distance, angle, or prediction calculations
- You're implementing targeting or aiming
- You need wall avoidance logic
- You want cleaner, shorter code

❌ **Don't use tank_utils when:**
- You're learning the basics (Week 1-2) - it's good to understand the math first!
- You need custom calculations that are specific to your unique strategy
- You're implementing something completely new that isn't in the utils yet

## Contributing New Utilities

Found a function you keep copying between tanks? Add it to `tank_utils.py`!

1. Write your function with clear documentation
2. Add examples in the docstring
3. Test it works
4. Submit a pull request!

Everyone benefits from shared, well-tested code! 🤝

## Questions?

- **"Will this work in battles?"** Yes! Just make sure `tank_utils.py` is in your RoboCode folder.
- **"Can I modify tank_utils?"** Yes! But remember, changes affect ALL tanks using it.
- **"What if tank_utils has a bug?"** Fix it once, all tanks benefit! That's the power of shared code.

---

**Happy coding! Now your tanks can focus on strategy instead of reinventing math! 🚀**
