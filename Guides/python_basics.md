# Python Basics for Tank Coders

A guide to the Python concepts you'll use in RoboCode, explained with tank examples!

## Table of Contents
1. [Variables](#variables)
2. [Functions](#functions)
3. [Classes](#classes)
4. [If Statements](#if-statements)
5. [Loops](#loops)
6. [Scope (Global vs Local)](#scope)
7. [Importing Modules](#importing-modules)

---

## Variables

Variables are like labeled boxes that store information.

### Basic Variables

```python
# Number variables
tank_x = 400
tank_y = 300
enemy_distance = 250.5

# Text (string) variables
tank_name = "MyTank"
status = "searching"

# Boolean (True/False) variables
is_moving = True
enemy_spotted = False
```

### Using Variables

```python
# Store tank position
my_x = 100
my_y = 200

# Calculate distance to center
center_x = 400
center_y = 300

x_diff = center_x - my_x  # 300
y_diff = center_y - my_y  # 100
```

### Variable Naming Rules

```python
# Good names (clear and descriptive)
enemy_distance = 200
bullet_power = 3
shots_fired = 0

# Bad names (unclear)
x = 200
p = 3
n = 0

# Rules:
# ✓ Use letters, numbers, underscores
# ✓ Start with letter or underscore
# ✓ Use descriptive names
# ✗ Can't start with number
# ✗ Can't use spaces
```

---

## Functions

Functions are reusable blocks of code that do specific tasks.

### Defining Functions

```python
def calculate_distance(x1, y1, x2, y2):
    """Calculate distance between two points"""
    x_diff = x2 - x1
    y_diff = y2 - y1
    distance = math.sqrt(x_diff**2 + y_diff**2)
    return distance

# Using the function
dist = calculate_distance(100, 100, 400, 300)
print(f"Distance: {dist}")  # Distance: 360.55
```

### Parameters and Return Values

```python
def choose_bullet_power(distance):
    """
    Choose power based on distance

    Parameter: distance (how far away enemy is)
    Returns: power level (1, 2, or 3)
    """
    if distance < 150:
        return 3  # Close range
    elif distance < 350:
        return 2  # Medium range
    else:
        return 1  # Long range

# Using it
power = choose_bullet_power(200)  # Returns 2
```

### Functions Without Return

```python
def print_status(energy, position):
    """Print tank status (doesn't return anything)"""
    print(f"Energy: {energy}")
    print(f"Position: {position}")

# Using it
print_status(75, "center")
```

---

## Classes

Classes are blueprints for creating objects. Your tank is a class!

### Basic Class Structure

```python
class Tank:
    def __init__(self, name):
        """Initialize the tank (runs once when created)"""
        self.name = name
        self.energy = 100
        self.x = 0
        self.y = 0

    def move_forward(self, distance):
        """Move the tank forward"""
        self.y += distance
        print(f"{self.name} moved {distance} pixels")

    def shoot(self, power):
        """Shoot a bullet"""
        self.energy -= power
        print(f"{self.name} fired! Energy: {self.energy}")

# Creating a tank
my_tank = Tank("Destroyer")
my_tank.move_forward(50)
my_tank.shoot(3)
```

### Understanding `self`

```python
class RoboTank:
    def __init__(self):
        # self.variable is accessible in ALL methods
        self.energy = 100
        self.shots_fired = 0

    def fire(self, power):
        # Use self to access the tank's own variables
        self.energy -= power
        self.shots_fired += 1
        print(f"Fired shot #{self.shots_fired}, Energy: {self.energy}")

    def get_stats(self):
        # Can access self.shots_fired from any method
        return f"Shots: {self.shots_fired}, Energy: {self.energy}"

# Using the class
tank = RoboTank()
tank.fire(2)      # Fired shot #1, Energy: 98
tank.fire(1)      # Fired shot #2, Energy: 97
print(tank.get_stats())  # Shots: 2, Energy: 97
```

### Class vs Instance Variables

```python
class BattleTank:
    # Class variable (shared by ALL tanks)
    total_tanks = 0

    def __init__(self, name):
        # Instance variables (unique to each tank)
        self.name = name
        self.energy = 100

        # Increment class variable
        BattleTank.total_tanks += 1

# Creating tanks
tank1 = BattleTank("Alpha")
tank2 = BattleTank("Beta")

print(tank1.name)  # "Alpha"
print(tank2.name)  # "Beta"
print(BattleTank.total_tanks)  # 2
```

---

## If Statements

If statements let your tank make decisions.

### Basic If

```python
distance = 150

if distance < 200:
    print("Enemy is close!")
    power = 3
```

### If-Else

```python
energy = 45

if energy > 50:
    print("Healthy - attack!")
    fire(3)
else:
    print("Low energy - retreat!")
    back(100)
```

### If-Elif-Else

```python
distance = 250

if distance < 150:
    print("Close combat")
    power = 3
elif distance < 350:
    print("Medium range")
    power = 2
else:
    print("Long range")
    power = 1

fire(power)
```

### Comparison Operators

```python
x = 100

# Comparisons
x < 200      # Less than: True
x > 50       # Greater than: True
x <= 100     # Less than or equal: True
x >= 100     # Greater than or equal: True
x == 100     # Equal to: True
x != 50      # Not equal to: True
```

### Combining Conditions

```python
distance = 150
energy = 80

# AND - both must be True
if distance < 200 and energy > 50:
    print("Close and healthy - ATTACK!")

# OR - at least one must be True
if distance < 100 or energy < 20:
    print("Emergency situation!")

# NOT - opposite
if not enemy_spotted:
    print("Keep searching...")
```

---

## Loops

Loops repeat code multiple times.

### For Loop

```python
# Count from 0 to 4
for i in range(5):
    print(f"Searching sector {i}")

# Count from 1 to 3
for power in range(1, 4):
    print(f"Testing power {power}")

# Loop through a list
directions = ["north", "east", "south", "west"]
for direction in directions:
    print(f"Scanning {direction}")
```

### While Loop

```python
# Keep moving until close to wall
distance_to_wall = 500

while distance_to_wall > 50:
    ahead(20)
    distance_to_wall -= 20
    print(f"Distance to wall: {distance_to_wall}")

print("Wall ahead! Stopping.")
```

### Break and Continue

```python
# Break - exit loop early
for i in range(100):
    turn_radar(10)
    if enemy_spotted:
        print("Found enemy!")
        break  # Stop searching

# Continue - skip to next iteration
for power in range(1, 4):
    if power == 2:
        continue  # Skip power 2
    print(f"Testing power {power}")  # Prints 1 and 3
```

---

## Scope (Global vs Local Variables)

Scope determines where a variable can be accessed.

### Local Variables

```python
def calculate_damage(power):
    # damage is LOCAL - only exists inside this function
    damage = power * 4
    return damage

damage = calculate_damage(3)  # Returns 12
# Can't use damage variable from inside the function here
```

### Instance Variables (Class Scope)

```python
class MyTank:
    def __init__(self):
        # self.energy is accessible in ALL methods of this tank
        self.energy = 100

    def fire(self, power):
        # Can access self.energy from any method
        self.energy -= power

    def get_energy(self):
        # Can access self.energy from any method
        return self.energy

tank = MyTank()
tank.fire(3)
print(tank.get_energy())  # 97
```

### Global Variables (Avoid in RoboCode)

```python
# Global variable (outside any function/class)
ARENA_WIDTH = 800

class Tank:
    def check_position(self):
        # Can access global variable
        if self.x > ARENA_WIDTH:
            print("Out of bounds!")

# Generally avoid global variables in tank code
# Use instance variables (self.variable) instead
```

### Variable Shadowing

```python
class Tank:
    def __init__(self):
        self.power = 2  # Instance variable

    def fire(self):
        power = 3  # Local variable (shadows self.power)
        print(power)  # Prints 3

        # To access instance variable when shadowed:
        print(self.power)  # Prints 2
```

---

## Importing Modules

Modules provide extra functionality.

### Math Module

```python
import math

# Square root
distance = math.sqrt(100)  # 10.0

# Trigonometry
angle_rad = math.atan2(300, 400)
angle_deg = math.degrees(angle_rad)

# Constants
print(math.pi)  # 3.14159...
```

### Random Module

```python
import random

# Random number between 0.0 and 1.0
chance = random.random()

# Random integer
power = random.randint(1, 3)  # 1, 2, or 3

# Random choice from list
move = random.choice(["forward", "back", "left", "right"])
```

### Import Styles

```python
# Import entire module
import math
x = math.sqrt(100)

# Import specific function
from math import sqrt
x = sqrt(100)

# Import with alias
import math as m
x = m.sqrt(100)

# Import multiple functions
from math import sqrt, sin, cos
```

---

## Quick Reference

### Common Patterns in RoboCode

```python
class MyTank:
    def __init__(self):
        # Initialize variables
        self.name = "MyTank"
        self.energy = 100

    def run(self):
        # Main loop
        if self.energy > 50:
            # Attack mode
            self.ahead(50)
        else:
            # Defensive mode
            self.back(30)

    def on_scanned_robot(self, enemy):
        # Calculate
        distance = enemy.distance

        # Decide
        if distance < 200:
            power = 3
        else:
            power = 1

        # Act
        self.fire(power)
```

### Data Types

```python
# Integer (whole number)
x = 42

# Float (decimal)
y = 3.14

# String (text)
name = "Tank"

# Boolean (True/False)
alive = True

# List (collection)
positions = [100, 200, 300]

# Dictionary (key-value pairs)
stats = {"shots": 10, "hits": 7}
```

### String Formatting

```python
name = "MyTank"
energy = 75
distance = 234.567

# f-strings (modern way)
print(f"{name} has {energy} energy")
print(f"Distance: {distance:.2f}")  # 2 decimal places

# .format() method
print("{} has {} energy".format(name, energy))

# % formatting (old way)
print("%s has %d energy" % (name, energy))
```

---

## Practice Exercises

### Exercise 1: Variables and Functions
Create a function that calculates bullet damage:
```python
def calculate_damage(power):
    # Your code here
    pass

# Should return: 4, 8, 12 for powers 1, 2, 3
```

### Exercise 2: Classes
Create a simple tank class with energy management:
```python
class SimpleTank:
    def __init__(self):
        # Initialize energy to 100
        pass

    def fire(self, power):
        # Reduce energy by power
        # Print remaining energy
        pass
```

### Exercise 3: If Statements
Write code to choose movement based on energy:
```python
energy = 45

# If energy > 70: attack
# If energy > 30: balanced
# If energy <= 30: retreat
```

---

## Tips for Learning

1. **Start Simple**: Begin with basic variables and functions
2. **Experiment**: Change values and see what happens
3. **Read Error Messages**: They tell you what's wrong
4. **Use Print**: Add `print()` to see what your code is doing
5. **Practice**: The more you code, the easier it gets!

## Common Mistakes

### Indentation
```python
# Wrong - no indentation
def my_function():
print("Hello")  # ERROR!

# Right - proper indentation
def my_function():
    print("Hello")  # Correct!
```

### Forgetting self
```python
class Tank:
    def __init__(self):
        energy = 100  # Wrong! Should be self.energy

    def fire(self):
        energy -= 1  # Error! 'energy' not defined
```

### Wrong Comparison
```python
# Wrong - assignment instead of comparison
if x = 100:  # ERROR! = is assignment

# Right - use == for comparison
if x == 100:  # Correct!
```

---

Now you're ready to code tanks! Use this guide as a reference whenever you need to remember how something works.

Happy coding! 🚀
