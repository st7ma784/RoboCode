# Week 2: Math Magic - Predicting Where Tanks Will Be! 📐

This week you'll learn the secret math that makes your tank a sharpshooter! You'll learn:
1. What angles are and how to use them
2. How to calculate distances
3. How to predict where a moving tank will be
4. How to aim perfectly!

## Part 1: Understanding Angles (15 minutes)

### What's an Angle?

An angle is just a measurement of how much you need to turn. Think of it like a clock:
- Pointing straight up (12 o'clock) = 0 degrees
- Pointing right (3 o'clock) = 90 degrees
- Pointing down (6 o'clock) = 180 degrees
- Pointing left (9 o'clock) = 270 degrees

### In RoboCode:
```
        0°
        ↑
        |
270° ← tank → 90°
        |
        ↓
       180°
```

When your tank faces 0°, it's pointing to the top of the screen!

## Part 2: Calculating Distance (20 minutes)

### The Distance Formula

To find how far away an enemy tank is, we use the Pythagorean theorem (fancy name for something simple!):

```
distance = √(x_difference² + y_difference²)
```

Don't worry! Python makes this easy:

```python
import math

# My tank's position
my_x = 100
my_y = 200

# Enemy tank's position
enemy_x = 400
enemy_y = 500

# Calculate the differences
x_diff = enemy_x - my_x  # 300
y_diff = enemy_y - my_y  # 300

# Calculate distance
distance = math.sqrt(x_diff**2 + y_diff**2)
print(f"Enemy is {distance} pixels away!")  # About 424 pixels
```

### Try It Yourself!

What's the distance if:
- You're at (0, 0)
- Enemy is at (300, 400)

<details>
<summary>Click to see answer</summary>

```python
distance = math.sqrt(300**2 + 400**2)
# = math.sqrt(90000 + 160000)
# = math.sqrt(250000)
# = 500 pixels!
```
</details>

## Part 3: Finding the Angle to an Enemy (20 minutes)

### Using atan2 (Arctangent)

To aim at an enemy, you need to know what angle to turn to. Python's `math.atan2()` does this!

```python
import math

# My position
my_x = 200
my_y = 200

# Enemy position
enemy_x = 500
enemy_y = 400

# Calculate the angle
x_diff = enemy_x - my_x  # 300
y_diff = enemy_y - my_y  # 200

# atan2 gives us the angle in radians
angle_radians = math.atan2(x_diff, y_diff)

# Convert to degrees (because RoboCode uses degrees!)
angle_degrees = math.degrees(angle_radians)

print(f"Enemy is at {angle_degrees} degrees!")
```

### Important Note!

RoboCode uses a special coordinate system:
- X increases to the right
- Y increases downward (opposite of normal math!)
- 0 degrees points up

So our angle calculation becomes:
```python
angle = math.degrees(math.atan2(enemy_x - my_x, enemy_y - my_y))
```

## Part 4: Predicting Movement (25 minutes)

### The Big Idea

If an enemy is moving, you need to aim where they're GOING, not where they ARE!

### Simple Prediction

```python
import math

def predict_position(current_x, current_y, velocity, heading, time):
    """
    Predict where a tank will be in the future

    current_x, current_y: where the tank is now
    velocity: how fast it's moving
    heading: what direction it's moving (in degrees)
    time: how many game ticks in the future
    """
    # Convert heading to radians
    heading_rad = math.radians(heading)

    # Calculate future position
    future_x = current_x + velocity * time * math.sin(heading_rad)
    future_y = current_y + velocity * time * math.cos(heading_rad)

    return future_x, future_y
```

### Using It in Your Tank

```python
def on_scanned_robot(self, scanned_robot):
    """When we spot an enemy"""
    # Get enemy info
    enemy_distance = scanned_robot.distance
    enemy_heading = scanned_robot.heading
    enemy_velocity = scanned_robot.velocity

    # How long will bullet take to reach them?
    bullet_speed = 20  # pixels per tick (for power 1)
    time_to_hit = enemy_distance / bullet_speed

    # Where will they be?
    future_x, future_y = predict_position(
        scanned_robot.x,
        scanned_robot.y,
        enemy_velocity,
        enemy_heading,
        time_to_hit
    )

    # Aim at future position!
    angle_to_future = calculate_angle(self.x, self.y, future_x, future_y)
    self.turn_gun_to(angle_to_future)
    self.fire(1)
```

## Part 5: Your Smart Tank - "PredictorBot"

Create a new file called `predictor_bot.py`:

```python
"""
PredictorBot - A tank that predicts enemy movement!
"""
import math

class PredictorBot:
    def __init__(self):
        self.name = "PredictorBot"

    def run(self):
        """Main loop"""
        # Spin radar to look for enemies
        self.turn_radar_right(45)

        # Move in a circle to dodge bullets
        self.ahead(50)
        self.turn_right(15)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle from one point to another"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """Calculate distance between two points"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)

    def predict_position(self, x, y, velocity, heading, time):
        """Predict future position of a moving tank"""
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y

    def on_scanned_robot(self, scanned_robot):
        """When we see an enemy - predict and shoot!"""
        # Bullet speed based on power
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power  # Formula for bullet speed

        # Time for bullet to reach current position
        time_to_hit = scanned_robot.distance / bullet_speed

        # Predict where enemy will be
        future_x, future_y = self.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )

        # Calculate angle to future position
        angle = self.calculate_angle(self.x, self.y, future_x, future_y)

        # Aim and fire!
        self.turn_gun_to(angle)
        self.fire(bullet_power)

        print(f"Predicted enemy at ({future_x}, {future_y})")

    def on_hit_by_bullet(self, hit_by_bullet):
        """React when hit"""
        # Turn perpendicular to the bullet to dodge better
        self.turn_right(90)
        self.ahead(100)
```

## Part 6: Test Your Prediction Skills! 🎯

Time to see if your math works!

### Battle Against WallsBot (Recommended!)

**WallsBot** is the PERFECT opponent for testing your prediction skills because:
- It moves in predictable patterns (along the walls)
- It's fast enough to require prediction
- It shoots back, so you'll know if you're dodging well!

```bash
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py Samples/walls_bot.py
```

If your prediction math is working, you should hit WallsBot much more often than a tank without prediction!

### Compare Your Results

Try fighting with and without prediction:

**With prediction (your new bot):**
```bash
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py Samples/walls_bot.py
```

**Without prediction (Week 1 bot):**
```bash
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/walls_bot.py
```

You should see a BIG difference in accuracy! 📈

### Test Against Other Opponents

**Easy (should win easily now):**
```bash
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py Samples/sitting_duck.py
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py Samples/spin_bot.py
```

**Medium (good test):**
```bash
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py Samples/walls_bot.py
```

**Hard (real challenge):**
```bash
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py Samples/tracker_bot.py
```

### Battle ALL sample tanks:
```bash
python battle_runner.py Tutorials/Week2_Trigonometry/predictor_bot.py --all-samples
```

## Part 7: Experiments and Challenges

### Easy Challenges:
1. **Distance Detector**: Print the distance to every enemy you scan
2. **Angle Calculator**: Print the angle to aim at each enemy
3. **Close Combat**: Only shoot enemies that are less than 200 pixels away

### Medium Challenges:
1. **Smart Power**: Use more power (3) for close enemies, less (1) for far enemies
2. **Better Prediction**: Account for the enemy changing direction
3. **Radar Focus**: Once you find an enemy, keep radar focused on them

### Hard Challenges:
1. **Lead the Target**: Calculate exactly how much to lead a moving target
2. **Dodge Predictor**: Predict where enemy bullets will be and dodge them
3. **Circular Prediction**: Predict enemies moving in circles

## Part 8: Understanding the Math

### Why Does This Work?

Imagine you're throwing a ball to a friend who's running:
- You don't throw where they ARE
- You throw where they WILL BE
- Same with tank bullets!

### The Right Triangle

When calculating distance, you're using the Pythagorean theorem:
```
      Enemy
        /|
       / |
      /  | y_diff
     /   |
    /____|
   Tank  x_diff

distance = √(x_diff² + y_diff²)
```

### The Angle

`atan2` finds the angle of that triangle:
```python
angle = atan2(x_diff, y_diff)
```

This tells you "turn this many degrees to point at the enemy!"

## Part 9: Submit Your Improved Tank! 🏆

Ready to show off your math skills?

1. Copy your `predictor_bot.py` to `Submissions/YourName/`
2. Test it against walls_bot to make sure it works well
3. Create a Pull Request with the title: `[Submission] YourName's Predictor Bot`
4. Watch your tank compete with better accuracy!

Your Week 2 tank should score much higher than your Week 1 tank because of prediction!

## Homework

Before next week:
1. ✅ Create your PredictorBot with the math functions
2. ✅ Test it against WallsBot - try to get at least 50% accuracy!
3. ✅ Compare performance: Week 1 tank vs Week 2 tank
4. ✅ Add at least one challenge feature
5. ✅ Submit your improved tank via Pull Request

**Bonus**: Can you beat TrackerBot? That's a real accomplishment!

## What's Next?

Next week: **Boundary Checking** - Making sure your tank doesn't crash into walls and aims at valid targets!

## Quick Reference

### Math Functions You Learned

```python
import math

# Distance
math.sqrt(x**2 + y**2)

# Angle in radians
math.atan2(x_diff, y_diff)

# Convert radians to degrees
math.degrees(radians)

# Convert degrees to radians
math.radians(degrees)

# Trigonometry for movement
math.sin(angle)  # For X movement
math.cos(angle)  # For Y movement
```

### Bullet Speed Formula
```python
bullet_speed = 20 - 3 * bullet_power
# Power 1: speed 17
# Power 2: speed 14
# Power 3: speed 11
```

## Help!

**"My math gives weird numbers!"**
- Make sure you're converting between radians and degrees
- RoboCode uses degrees, Python's math uses radians
- Use `math.degrees()` and `math.radians()` to convert

**"My tank shoots the wrong direction!"**
- Check your x_diff and y_diff calculations
- Make sure you're subtracting in the right order: `enemy - my_position`
- Remember: Y increases downward in RoboCode!

**"Prediction doesn't work!"**
- Start simple - try predicting for just 1 time unit
- Print out the values to see what's happening
- Test against a tank moving in a straight line first

---

Great job learning trigonometry! Your tank is getting smarter! 🎯
