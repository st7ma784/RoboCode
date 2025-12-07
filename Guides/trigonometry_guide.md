# Trigonometry for Tank Commanders 📐

Learn the math that makes your tank a sharpshooter! This guide explains trigonometry using tank battles as examples.

## Table of Contents
1. [What is Trigonometry?](#what-is-trigonometry)
2. [Angles and Directions](#angles-and-directions)
3. [The Right Triangle](#the-right-triangle)
4. [Distance Calculation](#distance-calculation)
5. [Finding Angles](#finding-angles)
6. [Sine, Cosine, and Movement](#sine-cosine-and-movement)
7. [Prediction and Velocity](#prediction-and-velocity)
8. [Practice Problems](#practice-problems)

---

## What is Trigonometry?

Trigonometry is the study of triangles and angles. In RoboCode, it helps you:
- Calculate distances to enemies
- Find angles to aim at targets
- Predict where moving tanks will be
- Calculate movement directions

**Don't worry!** Python does the hard math for you. You just need to understand WHEN to use which formula.

---

## Angles and Directions

### Degrees vs Radians

There are two ways to measure angles:
- **Degrees**: 0° to 360° (what RoboCode uses)
- **Radians**: 0 to 2π (what Python's math uses)

```python
import math

# Convert between them
degrees = 90
radians = math.radians(degrees)  # 1.5708...

radians = math.pi / 2  # 1.5708...
degrees = math.degrees(radians)  # 90.0
```

### RoboCode Coordinate System

```
        0° (North)
           ↑
           |
270° ←── tank ──→ 90° (East)
 (West)    |
           ↓
        180° (South)
```

**Key Points:**
- 0° points up (north)
- Angles increase clockwise
- X increases to the right (0 to 800)
- Y increases downward (0 to 600)

### Example: Heading Values

```python
# Tank facing different directions
heading = 0    # Pointing up
heading = 90   # Pointing right
heading = 180  # Pointing down
heading = 270  # Pointing left
heading = 45   # Pointing up-right (northeast)
```

---

## The Right Triangle

Most tank calculations use right triangles (triangles with a 90° angle).

### Tank Triangle Example

```
    Enemy (400, 100)
       /|
      / |
     /  | y_diff = 100
    /   |
   /    |
  /_____|
MyTank
(200, 200)

  x_diff = 200
```

This forms a right triangle where:
- **x_diff** = horizontal distance
- **y_diff** = vertical distance
- **hypotenuse** = direct distance

---

## Distance Calculation

### Pythagorean Theorem

To find the distance between two points:

**Formula:** distance = √(x_diff² + y_diff²)

```python
import math

# My tank position
my_x = 200
my_y = 200

# Enemy position
enemy_x = 400
enemy_y = 100

# Calculate differences
x_diff = enemy_x - my_x  # 200
y_diff = enemy_y - my_y  # -100 (enemy is above us)

# Calculate distance
distance = math.sqrt(x_diff**2 + y_diff**2)
# = math.sqrt(200**2 + 100**2)
# = math.sqrt(40000 + 10000)
# = math.sqrt(50000)
# = 223.6 pixels

print(f"Enemy is {distance:.1f} pixels away")
```

### Distance Function

```python
def calculate_distance(x1, y1, x2, y2):
    """Calculate distance between two points"""
    x_diff = x2 - x1
    y_diff = y2 - y1
    return math.sqrt(x_diff**2 + y_diff**2)

# Using it
dist = calculate_distance(100, 100, 400, 300)
print(f"Distance: {dist:.1f}")  # Distance: 360.6
```

---

## Finding Angles

### atan2 - Your Best Friend

To find what angle to turn to face a target:

**Formula:** angle = atan2(x_diff, y_diff)

```python
import math

# My position
my_x = 200
my_y = 300

# Enemy position
enemy_x = 500
enemy_y = 100

# Calculate differences
x_diff = enemy_x - my_x  # 300 (enemy is to the right)
y_diff = enemy_y - my_y  # -200 (enemy is above)

# Calculate angle in radians
angle_rad = math.atan2(x_diff, y_diff)

# Convert to degrees for RoboCode
angle_deg = math.degrees(angle_rad)

print(f"Turn to {angle_deg:.1f} degrees to face enemy")
```

### Why atan2 Instead of atan?

`atan2` handles all four quadrants correctly:

```python
# atan2 knows the difference between these:
math.atan2(1, 1)    # 45° (northeast)
math.atan2(1, -1)   # 135° (southeast)
math.atan2(-1, -1)  # -135° or 225° (southwest)
math.atan2(-1, 1)   # -45° or 315° (northwest)

# Always use atan2 for tank angles!
```

### Angle Calculation Function

```python
def calculate_angle(from_x, from_y, to_x, to_y):
    """Calculate angle from one point to another"""
    x_diff = to_x - from_x
    y_diff = to_y - from_y
    return math.degrees(math.atan2(x_diff, y_diff))

# Using it
angle = calculate_angle(200, 200, 500, 400)
print(f"Aim at {angle:.1f} degrees")
```

---

## Sine, Cosine, and Movement

### Understanding Sine and Cosine

Sine and cosine help convert angles into X and Y movement:

```python
import math

heading = 45  # 45 degrees (northeast)
distance = 100  # Move 100 pixels

# Convert to radians
heading_rad = math.radians(heading)

# Calculate X and Y movement
x_movement = distance * math.sin(heading_rad)  # ≈ 70.7
y_movement = distance * math.cos(heading_rad)  # ≈ 70.7

# New position
new_x = old_x + x_movement
new_y = old_y + y_movement
```

### The Unit Circle

```
        Y (cos)
           |
      90°  | 0°
           |
    -------+------- X (sin)
   180°    |    270°
           |
```

**Key Relationships:**
- `sin(0°) = 0`, `cos(0°) = 1` → straight up
- `sin(90°) = 1`, `cos(90°) = 0` → straight right
- `sin(180°) = 0`, `cos(180°) = -1` → straight down
- `sin(270°) = -1`, `cos(270°) = 0` → straight left

### Movement in Any Direction

```python
def move_in_direction(start_x, start_y, heading, distance):
    """
    Calculate new position after moving

    heading: direction in degrees
    distance: how far to move
    """
    heading_rad = math.radians(heading)

    # Calculate movement
    dx = distance * math.sin(heading_rad)
    dy = distance * math.cos(heading_rad)

    # New position
    new_x = start_x + dx
    new_y = start_y + dy

    return new_x, new_y

# Example
x, y = move_in_direction(400, 300, 90, 100)
print(f"New position: ({x:.1f}, {y:.1f})")
# Result: (500.0, 300.0) - moved 100 pixels to the right
```

---

## Prediction and Velocity

### Predicting Enemy Position

If an enemy is moving, predict where they'll be:

```python
def predict_position(x, y, velocity, heading, time):
    """
    Predict where a moving tank will be

    x, y: current position
    velocity: speed (pixels per tick)
    heading: direction (degrees)
    time: how many ticks in the future
    """
    # Convert heading to radians
    heading_rad = math.radians(heading)

    # Calculate total movement
    total_distance = velocity * time

    # Calculate displacement
    dx = total_distance * math.sin(heading_rad)
    dy = total_distance * math.cos(heading_rad)

    # Future position
    future_x = x + dx
    future_y = y + dy

    return future_x, future_y
```

### Lead the Target

Calculate where to aim to hit a moving enemy:

```python
def aim_at_moving_target(my_x, my_y, enemy_x, enemy_y,
                         enemy_velocity, enemy_heading, bullet_power):
    """Aim at where enemy will be when bullet arrives"""

    # Step 1: Calculate current distance
    distance = calculate_distance(my_x, my_y, enemy_x, enemy_y)

    # Step 2: Calculate bullet speed
    bullet_speed = 20 - (3 * bullet_power)

    # Step 3: Estimate time for bullet to reach enemy
    time_to_hit = distance / bullet_speed

    # Step 4: Predict where enemy will be
    future_x, future_y = predict_position(
        enemy_x, enemy_y,
        enemy_velocity, enemy_heading,
        time_to_hit
    )

    # Step 5: Calculate angle to future position
    aim_angle = calculate_angle(my_x, my_y, future_x, future_y)

    return aim_angle

# Using it
angle = aim_at_moving_target(
    my_x=200, my_y=200,
    enemy_x=400, enemy_y=400,
    enemy_velocity=5, enemy_heading=90,
    bullet_power=2
)
print(f"Aim at {angle:.1f}° to hit moving target")
```

### Bullet Speed Formula

```python
def get_bullet_speed(power):
    """Calculate bullet speed based on power"""
    return 20 - (3 * power)

# Examples
get_bullet_speed(1)  # 17 pixels/tick (fast)
get_bullet_speed(2)  # 14 pixels/tick (medium)
get_bullet_speed(3)  # 11 pixels/tick (slow)
```

---

## Practice Problems

### Problem 1: Distance Calculation

**Question:** Your tank is at (100, 150). Enemy is at (300, 450). How far away is the enemy?

<details>
<summary>Click to see solution</summary>

```python
import math

my_x, my_y = 100, 150
enemy_x, enemy_y = 300, 450

x_diff = enemy_x - my_x  # 200
y_diff = enemy_y - my_y  # 300

distance = math.sqrt(x_diff**2 + y_diff**2)
# = math.sqrt(200**2 + 300**2)
# = math.sqrt(40000 + 90000)
# = math.sqrt(130000)
# = 360.6 pixels
```

Answer: **360.6 pixels**
</details>

### Problem 2: Angle Calculation

**Question:** You're at (200, 200). Enemy is at (500, 200). What angle should you turn to?

<details>
<summary>Click to see solution</summary>

```python
import math

my_x, my_y = 200, 200
enemy_x, enemy_y = 500, 200

x_diff = enemy_x - my_x  # 300
y_diff = enemy_y - my_y  # 0

angle = math.degrees(math.atan2(x_diff, y_diff))
# = math.degrees(math.atan2(300, 0))
# = 90.0 degrees
```

Answer: **90° (facing right/east)**
</details>

### Problem 3: Prediction

**Question:** Enemy is at (400, 300), moving at velocity 5, heading 0° (up). Where will they be in 10 ticks?

<details>
<summary>Click to see solution</summary>

```python
import math

x, y = 400, 300
velocity = 5
heading = 0
time = 10

heading_rad = math.radians(heading)

dx = velocity * time * math.sin(heading_rad)  # 5 * 10 * sin(0) = 0
dy = velocity * time * math.cos(heading_rad)  # 5 * 10 * cos(0) = 50

future_x = x + dx  # 400 + 0 = 400
future_y = y + dy  # 300 + 50 = 350
```

Answer: **(400, 350)** - 50 pixels down (Y increases downward)
</details>

### Problem 4: Movement

**Question:** You're at (200, 200). If you move 100 pixels at heading 45°, where will you be?

<details>
<summary>Click to see solution</summary>

```python
import math

x, y = 200, 200
heading = 45
distance = 100

heading_rad = math.radians(heading)

dx = distance * math.sin(heading_rad)  # 100 * sin(45°) ≈ 70.7
dy = distance * math.cos(heading_rad)  # 100 * cos(45°) ≈ 70.7

new_x = x + dx  # 200 + 70.7 = 270.7
new_y = y + dy  # 200 + 70.7 = 270.7
```

Answer: **(270.7, 270.7)** - moved right and down at 45° angle
</details>

---

## Quick Reference

### Common Functions

```python
import math

# Distance
distance = math.sqrt(x_diff**2 + y_diff**2)

# Angle (in radians)
angle_rad = math.atan2(x_diff, y_diff)

# Convert radians to degrees
angle_deg = math.degrees(angle_rad)

# Convert degrees to radians
angle_rad = math.radians(angle_deg)

# Sine and cosine (input must be radians!)
x_component = math.sin(angle_rad)
y_component = math.cos(angle_rad)

# Constants
pi = math.pi  # 3.14159...
```

### Common Patterns

```python
# Pattern 1: Calculate distance
distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

# Pattern 2: Calculate angle
angle = math.degrees(math.atan2(x2-x1, y2-y1))

# Pattern 3: Move in direction
dx = distance * math.sin(math.radians(heading))
dy = distance * math.cos(math.radians(heading))
new_x = old_x + dx
new_y = old_y + dy

# Pattern 4: Predict position
future_x = x + velocity * time * math.sin(math.radians(heading))
future_y = y + velocity * time * math.cos(math.radians(heading))
```

---

## Tips and Tricks

### 1. Always Convert to Radians for Math Functions

```python
# Wrong
math.sin(90)  # Expects radians, not degrees!

# Right
math.sin(math.radians(90))  # Convert first
```

### 2. RoboCode Y is Inverted

In normal math, Y increases upward. In RoboCode, Y increases downward!

```python
# Moving "up" actually decreases Y
# Moving "down" actually increases Y
```

### 3. Use atan2, Not atan

```python
# Wrong - doesn't handle all directions
angle = math.atan(y/x)

# Right - handles all four quadrants
angle = math.atan2(x, y)
```

### 4. Order Matters in atan2

```python
# For RoboCode: atan2(x_diff, y_diff)
# Note: X comes first!
angle = math.atan2(enemy_x - my_x, enemy_y - my_y)
```

---

## Visual Examples

### Example 1: Aiming East

```
      Enemy
       (500, 300)

My Tank ------→ 90°
(200, 300)

x_diff = 300
y_diff = 0
angle = atan2(300, 0) = 90°
```

### Example 2: Aiming Northeast

```
         Enemy
        (400, 100)
          ↗ 45°
         /
        /
   My Tank
  (200, 200)

x_diff = 200
y_diff = -100
angle = atan2(200, -100) ≈ 63.4°
```

### Example 3: Prediction

```
Enemy now        Enemy in 5 ticks
   (300, 200) →  (350, 200)

   velocity = 10 pixels/tick
   heading = 90° (moving right)
   time = 5 ticks

   dx = 10 * 5 * sin(90°) = 50
   dy = 10 * 5 * cos(90°) = 0
   future_x = 300 + 50 = 350
```

---

## Summary

**The Three Main Formulas:**

1. **Distance:** `sqrt(x_diff² + y_diff²)`
2. **Angle:** `atan2(x_diff, y_diff)`
3. **Movement:** `x += distance * sin(angle)`, `y += distance * cos(angle)`

Master these three, and you'll be a trigonometry tank commander!

Remember: Don't memorize formulas - understand WHEN to use them. Practice with your tanks and the math will become natural!

---

Ready to apply this knowledge? Head back to the tutorials and make your tank a mathematical sharpshooter! 🎯
