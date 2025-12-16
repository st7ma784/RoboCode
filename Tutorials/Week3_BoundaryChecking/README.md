# Week 3: Stay Inside the Lines! ✅

> **Note:** This tutorial uses the BaseBot API which uses **property assignments** instead of method calls.
> - Movement: `self.forward = 100` (not `self.forward(100)`)
> - Turning: `self.turn_body = 45` (not `self.turn_right(45)`)
> - All event handlers must be `async` and use `await` for actions like `await self.fire()`

This week you'll learn how to keep your tank safe by:
1. Detecting walls before you hit them
2. Checking if your aim is valid
3. Using if-statements to make smart decisions
4. Staying inside the battle arena

## Part 1: Understanding the Arena (10 minutes)

### The Battle Arena

The battle arena is like a big rectangle:
```
(0,0) ──────────────── (800,0)
  │                        │
  │                        │
  │    Battle Arena        │
  │                        │
  │                        │
(0,600) ─────────────── (800,600)
```

- Top-left corner: (0, 0)
- X goes from 0 to 800 (left to right)
- Y goes from 0 to 600 (top to bottom)
- Your tank is about 36 pixels wide and 36 pixels tall

### The Danger Zone

If your tank's center gets too close to the edge, you'll hit the wall!

```python
# Safe zone (staying 50 pixels from edges)
safe_min_x = 50
safe_max_x = 800 - 50  # 750
safe_min_y = 50
safe_max_y = 600 - 50  # 550
```

## Part 2: If-Statements - Making Decisions (15 minutes)

### What's an If-Statement?

An if-statement lets your tank make decisions based on conditions:

```python
if condition:
    # Do this if condition is True
else:
    # Do this if condition is False
```

### Simple Example

```python
distance_to_wall = 30

if distance_to_wall < 50:
    print("Too close! Turn away!")
    self.turn_body = 90
else:
    print("Safe to keep going")
    self.ahead(20)
```

### Comparison Operators

These help you check conditions:

```python
x < 100     # Is x less than 100?
x > 100     # Is x greater than 100?
x <= 100    # Is x less than or equal to 100?
x >= 100    # Is x greater than or equal to 100?
x == 100    # Is x equal to 100?
x != 100    # Is x NOT equal to 100?
```

### Combining Conditions

Use `and` and `or`:

```python
# Both must be true
if x > 50 and x < 750:
    print("X is safe!")

# At least one must be true
if y < 50 or y > 550:
    print("Y is in danger zone!")

# Not (opposite)
if not (x < 50):
    print("X is not too small")
```

## Part 3: Checking Your Position (20 minutes)

### Am I Too Close to a Wall?

```python
def is_too_close_to_wall(self, margin=50):
    """
    Check if we're too close to any wall

    margin: how many pixels from edge is "too close"
    Returns: True if too close, False if safe
    """
    # Get arena size
    arena_width = self.get_arena_width()   # Usually 800
    arena_height = self.get_arena_height()  # Usually 600

    # Check each edge
    too_close_left = self.get_x() < margin
    too_close_right = self.get_x() > (arena_width - margin)
    too_close_top = self.get_y() < margin
    too_close_bottom = self.get_y() > (arena_height - margin)

    # Return True if ANY edge is too close
    return too_close_left or too_close_right or too_close_top or too_close_bottom
```

### Which Wall Am I Close To?

```python
def find_nearest_wall(self):
    """
    Figure out which wall is closest

    Returns: "top", "bottom", "left", or "right"
    """
    # Calculate distance to each wall
    dist_to_left = self.get_x()
    dist_to_right = self.get_arena_width() - self.get_x()
    dist_to_top = self.get_y()
    dist_to_bottom = self.get_arena_height() - self.get_y()

    # Find the minimum
    distances = {
        "left": dist_to_left,
        "right": dist_to_right,
        "top": dist_to_top,
        "bottom": dist_to_bottom
    }

    # Return the wall with smallest distance
    return min(distances, key=distances.get)
```

### Turn Away from Walls

```python
def avoid_walls(self):
    """Turn away from the nearest wall"""
    if self.is_too_close_to_wall():
        nearest = self.find_nearest_wall()

        if nearest == "left":
            # Turn to face right
            self.turn_to(90)
        elif nearest == "right":
            # Turn to face left
            self.turn_to(270)
        elif nearest == "top":
            # Turn to face down
            self.turn_to(180)
        elif nearest == "bottom":
            # Turn to face up
            self.turn_to(0)

        # Move away from wall
        self.ahead(100)
```

## Part 4: Checking Your Aim (20 minutes)

### Is My Target Inside the Arena?

Before shooting, make sure you're aiming at a valid point:

```python
def is_valid_target(self, x, y):
    """
    Check if a point is inside the arena

    x, y: coordinates to check
    Returns: True if inside arena, False if outside
    """
    # Add a small margin for safety
    margin = 20

    x_ok = margin < x < (self.get_arena_width() - margin)
    y_ok = margin < y < (self.get_arena_height() - margin)

    return x_ok and y_ok
```

### Smart Prediction with Boundary Checking

Remember Week 2's prediction? Let's add safety checks:

```python
def predict_and_validate(self, event):
    """Predict enemy position and check if it's valid"""
    # Get enemy info from event
    enemy_x = event.x
    enemy_y = event.y

    # Calculate distance
    dx = enemy_x - self.get_x()
    dy = enemy_y - self.get_y()
    distance = math.sqrt(dx**2 + dy**2)

    # Calculate prediction (from Week 2)
    bullet_speed = 20 - 3 * 2  # power 2
    time_to_hit = distance / bullet_speed

    future_x, future_y = self.predict_position(
        enemy_x,
        enemy_y,
        event.speed,
        event.direction,
        time_to_hit
    )

    # Check if predicted position is valid
    if self.is_valid_target(future_x, future_y):
        print(f"Valid target at ({future_x}, {future_y})")
        return future_x, future_y
    else:
        print("Predicted position is outside arena!")
        # Shoot at current position instead
        return enemy_x, enemy_y
```

## Part 5: Your Safe Tank - "BoundaryBot"

Create `boundary_bot.py`:

```python
"""
BoundaryBot - A smart tank that never hits walls!
"""
import math

class BoundaryBot:
    def __init__(self):
        self.name = "BoundaryBot"
        self.x = 0
        self.y = 0
        self.heading = 0
        self.battlefield_width = 800
        self.battlefield_height = 600

    def run(self):
        """Main loop with boundary checking"""
        # Check for walls before moving
        if self.is_too_close_to_wall(50):
            print("Wall detected! Avoiding...")
            self.avoid_walls()
        else:
            # Safe to move
            self.ahead(50)
            self.turn_body = 10

        # Keep radar spinning
        self.turn_radar_right(45)

    def is_too_close_to_wall(self, margin=50):
        """Check if we're dangerously close to any wall"""
        too_close_left = self.x < margin
        too_close_right = self.x > (self.battlefield_width - margin)
        too_close_top = self.y < margin
        too_close_bottom = self.y > (self.battlefield_height - margin)

        return too_close_left or too_close_right or too_close_top or too_close_bottom

    def find_nearest_wall(self):
        """Determine which wall is closest"""
        distances = {
            "left": self.x,
            "right": self.battlefield_width - self.x,
            "top": self.y,
            "bottom": self.battlefield_height - self.y
        }
        return min(distances, key=distances.get)

    def avoid_walls(self):
        """Turn away from the nearest wall"""
        nearest = self.find_nearest_wall()

        # Turn to face away from wall
        if nearest == "left":
            self.turn_to(90)   # Face right
        elif nearest == "right":
            self.turn_to(270)  # Face left
        elif nearest == "top":
            self.turn_to(180)  # Face down
        elif nearest == "bottom":
            self.turn_to(0)    # Face up

        # Move away
        self.ahead(100)

    def is_valid_target(self, x, y):
        """Check if coordinates are inside the arena"""
        margin = 20
        x_ok = margin < x < (self.battlefield_width - margin)
        y_ok = margin < y < (self.battlefield_height - margin)
        return x_ok and y_ok

    def on_scanned_robot(self, scanned_robot):
        """Shoot at enemies with validation"""
        # Simple aim at current position
        target_x = scanned_robot.x
        target_y = scanned_robot.y

        # Validate target
        if self.is_valid_target(target_x, target_y):
            angle = self.calculate_angle(self.x, self.y, target_x, target_y)
            self.turn_gun_to(angle)
            self.fire(2)
            print(f"Firing at valid target!")
        else:
            print("Enemy is outside valid range - not shooting")

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle to target (from Week 2)"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    def on_hit_wall(self, hit_wall):
        """Emergency response if we hit a wall"""
        print("ERROR: Hit a wall! This shouldn't happen!")
        self.forward = -100
        self.turn_body = 135

    # Game engine methods
    def ahead(self, distance):
        pass

    # Helper method for turn_body property
def turn_right(self, degrees):
    self.turn_body = degrees
        pass

    def turn_to(self, degrees):
        pass

    def turn_radar_right(self, degrees):
        pass

    def turn_gun_to(self, angle):
        pass

    def fire(self, power):
        pass

    # Helper method for forward property
def back(self, distance):
    self.forward = -distance
        pass
```

## Part 6: Challenges and Experiments

### Easy Challenges:
1. **Wall Counter**: Count how many times you get close to a wall
2. **Safe Zone Display**: Print which wall you're closest to
3. **Corner Detector**: Detect when you're in a corner (close to 2 walls)

### Medium Challenges:
1. **Smart Margin**: Use bigger margin when moving fast, smaller when slow
2. **Wall Hugger**: Stay exactly 100 pixels from walls as you move
3. **Predictive Avoidance**: Check if your NEXT move will hit a wall

### Hard Challenges:
1. **Perfect Circles**: Move in circles while avoiding walls
2. **Safe Prediction**: Combine Week 2's prediction with boundary checking
3. **Corner Escape**: Special behavior when stuck in a corner

## Part 7: Testing Your Code

### Test Your Boundary Checks

```python
# Create a test function
def test_boundary_checking():
    """Test our boundary logic"""
    bot = BoundaryBot()

    # Test case 1: Safe position
    bot.x = 400
    bot.y = 300
    assert not bot.is_too_close_to_wall(), "Should be safe in center!"

    # Test case 2: Near left wall
    bot.x = 30
    bot.y = 300
    assert bot.is_too_close_to_wall(), "Should detect left wall!"
    assert bot.find_nearest_wall() == "left", "Should identify left wall!"

    # Test case 3: Near corner
    bot.x = 30
    bot.y = 30
    assert bot.is_too_close_to_wall(), "Should detect corner danger!"

    print("All tests passed!")

# Run tests
test_boundary_checking()
```

## Homework

Before next week:
1. Create your BoundaryBot
2. Test it in different arena sizes
3. Add at least one challenge feature
4. Make sure it NEVER hits a wall during battle

## What's Next?

Next week: **Strategy** - Making your tank move unpredictably and react to being attacked!

## Quick Reference

### Comparison Operators
```python
<   # Less than
>   # Greater than
<=  # Less than or equal
>=  # Greater than or equal
==  # Equal to
!=  # Not equal to
```

### Logical Operators
```python
and  # Both conditions must be True
or   # At least one condition must be True
not  # Opposite of condition
```

### Boundary Check Pattern
```python
if self.x < margin or self.x > (max_x - margin):
    # Too close to left or right wall!

if self.y < margin or self.y > (max_y - margin):
    # Too close to top or bottom wall!
```

## Help!

**"My tank still hits walls!"**
- Check your margin - maybe it needs to be bigger (try 75 instead of 50)
- Make sure you're checking walls BEFORE moving
- Print your x and y positions to debug

**"My conditions don't work!"**
- Remember: `=` assigns, `==` compares
- Use `and` for "both must be true"
- Use `or` for "at least one must be true"

**"How do I test my checks?"**
- Set your tank's position manually in a test
- Print the results of your checks
- Try extreme positions (0, 0) and (800, 600)

---

Excellent work! Your tank is now smart enough to stay safe! 🛡️
