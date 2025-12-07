# Week 4: Be Unpredictable! 🎲

This week you'll learn advanced strategies to make your tank harder to hit:
1. Moving in unpredictable patterns
2. Reacting to enemy fire
3. Using random numbers strategically
4. Changing tactics based on the situation

## Part 1: Why Be Unpredictable? (10 minutes)

### The Problem with Patterns

If you always move the same way, enemies can predict where you'll be!

**Bad Examples:**
```python
# Always move in circles - PREDICTABLE!
def run(self):
    self.ahead(50)
    self.turn_right(10)

# Always dodge the same way - PREDICTABLE!
def on_hit_by_bullet(self, bullet):
    self.turn_right(90)  # Enemy knows you'll do this!
```

**Why This is Bad:**
- Smart enemies will aim where you're going
- You become an easy target
- You'll get hit more often

### The Solution: Randomness!

Add some randomness to keep enemies guessing:
```python
import random

def run(self):
    # Sometimes turn left, sometimes right!
    if random.random() < 0.5:
        self.turn_right(random.randint(5, 30))
    else:
        self.turn_left(random.randint(5, 30))

    self.ahead(random.randint(20, 80))
```

## Part 2: Using Random Numbers (15 minutes)

### Python's Random Module

```python
import random

# Random float between 0.0 and 1.0
chance = random.random()
print(chance)  # Might print: 0.742891

# Random integer between min and max (inclusive)
distance = random.randint(20, 100)
print(distance)  # Might print: 67

# Random choice from a list
direction = random.choice(["left", "right", "forward", "back"])
print(direction)  # Might print: "right"
```

### Strategic Randomness

Don't just use random numbers everywhere - use them smartly!

```python
def should_dodge():
    """30% chance to dodge"""
    return random.random() < 0.3

def choose_movement():
    """Pick a random movement strategy"""
    strategies = [
        "circle",
        "zigzag",
        "straight",
        "spiral"
    ]
    return random.choice(strategies)
```

## Part 3: Movement Patterns (25 minutes)

### Pattern 1: Zigzag

```python
def zigzag_movement(self):
    """Move in a zigzag pattern"""
    # Move forward
    self.ahead(100)

    # Randomly turn left or right
    if random.random() < 0.5:
        self.turn_right(30)
    else:
        self.turn_left(30)
```

### Pattern 2: Spiral

```python
def spiral_movement(self):
    """Move in an expanding spiral"""
    # Gradually increase turn radius
    distance = 20 + (self.time % 100)  # time is game tick counter
    self.ahead(distance)
    self.turn_right(20)
```

### Pattern 3: Random Walk

```python
def random_walk(self):
    """Move randomly but smoothly"""
    # Random forward distance
    distance = random.randint(30, 100)
    self.ahead(distance)

    # Random turn (small angles for smooth movement)
    angle = random.randint(-30, 30)
    if angle < 0:
        self.turn_left(abs(angle))
    else:
        self.turn_right(angle)
```

### Pattern 4: Stop and Go

```python
def stop_and_go(self):
    """Unpredictable stops make you hard to hit"""
    # 20% chance to stop
    if random.random() < 0.2:
        # Stop and spin
        self.turn_right(random.randint(45, 180))
    else:
        # Keep moving
        self.ahead(50)
        self.turn_right(10)
```

## Part 4: Reacting to Events (20 minutes)

### When You Get Hit

React differently each time!

```python
def on_hit_by_bullet(self, bullet):
    """React to being hit - keep them guessing!"""
    reaction = random.randint(1, 4)

    if reaction == 1:
        # Quick dodge forward
        self.ahead(100)
    elif reaction == 2:
        # Sharp turn and retreat
        self.turn_right(135)
        self.back(80)
    elif reaction == 3:
        # Spin and advance
        self.turn_left(90)
        self.ahead(120)
    else:
        # Stop and shoot back!
        angle_to_enemy = bullet.bearing  # Direction bullet came from
        self.turn_gun_to(angle_to_enemy)
        self.fire(3)  # Full power!

    print(f"Hit! Using reaction #{reaction}")
```

### When You Scan an Enemy

Different tactics based on distance:

```python
def on_scanned_robot(self, scanned_robot):
    """Choose tactics based on situation"""
    distance = scanned_robot.distance

    if distance < 100:
        # Close combat - aggressive!
        print("Close combat mode!")
        self.fire(3)  # Max power
        self.ahead(20)  # Move toward enemy
    elif distance < 300:
        # Medium range - tactical
        print("Medium range mode!")
        self.fire(2)  # Medium power
        # Strafe (move perpendicular)
        self.turn_right(90)
        self.ahead(50)
        self.turn_left(90)
    else:
        # Long range - cautious
        print("Sniper mode!")
        self.fire(1)  # Low power (faster bullet)
        # Keep distance
        self.back(30)
```

### When You Hit a Wall

Turn it into an advantage!

```python
def on_hit_wall(self, wall):
    """Use wall collision as a tactical reset"""
    # Back up
    self.back(50)

    # Random turn to confuse enemies
    angle = random.choice([45, 90, 135, 180])
    if random.random() < 0.5:
        self.turn_right(angle)
    else:
        self.turn_left(angle)

    # Quick burst forward
    self.ahead(100)
```

## Part 5: Your Strategic Tank - "TricksterBot"

Create `trickster_bot.py`:

```python
"""
TricksterBot - A tank that's impossible to predict!
"""
import random
import math

class TricksterBot:
    def __init__(self):
        self.name = "TricksterBot"
        self.x = 0
        self.y = 0
        self.time = 0  # Game tick counter

        # Strategy state
        self.current_pattern = "random_walk"
        self.pattern_change_countdown = 0

    def run(self):
        """Main loop with changing strategies"""
        self.time += 1

        # Change pattern every 50 ticks
        if self.pattern_change_countdown <= 0:
            self.current_pattern = random.choice([
                "zigzag",
                "spiral",
                "random_walk",
                "stop_and_go"
            ])
            self.pattern_change_countdown = 50
            print(f"Switching to {self.current_pattern} pattern!")

        # Execute current pattern
        if self.current_pattern == "zigzag":
            self.zigzag_movement()
        elif self.current_pattern == "spiral":
            self.spiral_movement()
        elif self.current_pattern == "random_walk":
            self.random_walk()
        elif self.current_pattern == "stop_and_go":
            self.stop_and_go()

        self.pattern_change_countdown -= 1

        # Keep radar spinning
        self.turn_radar_right(45)

    def zigzag_movement(self):
        """Zigzag pattern"""
        self.ahead(80)
        if random.random() < 0.5:
            self.turn_right(30)
        else:
            self.turn_left(30)

    def spiral_movement(self):
        """Spiral outward"""
        distance = 20 + (self.time % 80)
        self.ahead(distance)
        self.turn_right(25)

    def random_walk(self):
        """Random but smooth movement"""
        distance = random.randint(40, 100)
        self.ahead(distance)

        angle = random.randint(-25, 25)
        if angle < 0:
            self.turn_left(abs(angle))
        else:
            self.turn_right(angle)

    def stop_and_go(self):
        """Unpredictable stops"""
        if random.random() < 0.25:
            # Sudden stop and turn
            self.turn_right(random.randint(60, 180))
        else:
            self.ahead(60)
            self.turn_right(12)

    def on_scanned_robot(self, scanned_robot):
        """Adaptive tactics based on distance"""
        distance = scanned_robot.distance

        # Calculate aim
        angle = self.calculate_angle(
            self.x, self.y,
            scanned_robot.x, scanned_robot.y
        )

        if distance < 150:
            # Close combat - aggressive!
            print("⚔️ ATTACK MODE!")
            self.turn_gun_to(angle)
            self.fire(3)
            # Charge!
            self.ahead(30)

        elif distance < 350:
            # Medium range - tactical
            print("🎯 TACTICAL MODE")
            self.turn_gun_to(angle)
            self.fire(2)
            # Strafe
            if random.random() < 0.5:
                self.turn_right(90)
            else:
                self.turn_left(90)
            self.ahead(40)

        else:
            # Long range - sniper
            print("🔭 SNIPER MODE")
            self.turn_gun_to(angle)
            self.fire(1)
            # Maintain distance
            if random.random() < 0.3:
                self.back(40)

    def on_hit_by_bullet(self, bullet):
        """Unpredictable reactions"""
        print("💥 HIT! Reacting...")

        # Random reaction
        reaction = random.randint(1, 5)

        if reaction == 1:
            # Quick dodge
            self.ahead(100)
        elif reaction == 2:
            # Sharp turn and retreat
            self.turn_right(135)
            self.back(80)
        elif reaction == 3:
            # Aggressive counter
            self.turn_left(90)
            self.ahead(120)
        elif reaction == 4:
            # Spin move
            self.turn_right(random.randint(120, 240))
            self.ahead(60)
        else:
            # Stop and shoot back
            # (bearing tells us where bullet came from)
            self.turn_gun_to(bullet.bearing)
            self.fire(3)

        # Force pattern change
        self.pattern_change_countdown = 0

    def on_hit_wall(self, wall):
        """Tactical wall bounce"""
        print("🧱 Wall! Bouncing...")
        self.back(60)

        # Random escape angle
        angle = random.choice([60, 90, 120, 150])
        if random.random() < 0.5:
            self.turn_right(angle)
        else:
            self.turn_left(angle)

        self.ahead(80)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle to target"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    # Game engine methods
    def ahead(self, distance):
        pass

    def back(self, distance):
        pass

    def turn_right(self, degrees):
        pass

    def turn_left(self, degrees):
        pass

    def turn_radar_right(self, degrees):
        pass

    def turn_gun_to(self, angle):
        pass

    def fire(self, power):
        pass
```

## Part 6: Challenges and Experiments

### Easy Challenges:
1. **Pattern Logger**: Print which pattern you're using and count how many times each is used
2. **Dodge Counter**: Count successful dodges (getting hit less after implementing random reactions)
3. **Aggression Meter**: Track when you're in close/medium/long range mode

### Medium Challenges:
1. **Adaptive Patterns**: If you keep getting hit, switch patterns more often
2. **Energy Management**: Be more aggressive when you have lots of energy, defensive when low
3. **Multi-Enemy Tactics**: Behave differently when multiple enemies are nearby

### Hard Challenges:
1. **Pattern Memory**: Don't repeat the same pattern twice in a row
2. **Predictive Dodging**: Try to dodge based on when you THINK enemy will fire
3. **Custom Patterns**: Invent your own movement pattern!

## Homework

Before next week:
1. Create your TricksterBot
2. Test it against your previous tanks - does unpredictability help?
3. Invent at least one new movement pattern
4. Track which patterns work best

## What's Next?

Next week: **Advanced Targeting** - Choosing the right power, simulating shots, and maximizing hit probability!

## Quick Reference

### Random Functions

```python
import random

random.random()              # 0.0 to 1.0
random.randint(1, 10)        # 1 to 10 (inclusive)
random.choice([1, 2, 3])     # Pick one from list
random.uniform(1.5, 3.5)     # Float between values
```

### Pattern Ideas

- **Zigzag**: Alternate left/right turns
- **Spiral**: Gradually increase movement radius
- **Random Walk**: Small random adjustments
- **Stop-and-Go**: Unpredictable pauses
- **Figure-8**: Cross your own path
- **Square Dance**: Move in squares with random sides
- **Chaos Mode**: Completely random every tick!

## Help!

**"My tank is TOO random and hits walls!"**
- Add boundary checking from Week 3!
- Use smaller random ranges for angles
- Check walls before executing random movements

**"I can't hit anyone with random movement!"**
- Save your position when you scan an enemy
- Stop briefly to aim and fire
- Use separate movement and targeting logic

**"Which pattern is best?"**
- It depends on your opponent!
- Test different patterns
- Mix them up - the best strategy is variety!

---

Awesome! Your tank is now a tactical genius! 🧠
