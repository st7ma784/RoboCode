# Week 6: Code Like a Pro - Classes and Clean Code! 🏗️

Your tank code is getting powerful, but it's also getting messy! This week you'll learn how professional programmers organize their code to make it:
- Easier to read
- Easier to change
- Reusable in different tanks
- Less buggy!

You'll learn:
1. What classes really are and why they're useful
2. How to organize code into logical pieces
3. Inheritance - reusing code you already wrote
4. Polymorphism - different strategies, same interface
5. Building a professional tank architecture

## Part 1: The Problem - Messy Code! 🍝

Let's look at a typical Week 5 tank. It works, but it's hard to understand:

```python
import math

class MyTank:
    def __init__(self):
        self.name = "MessyTank"
        self.target_x = 0
        self.target_y = 0
        self.last_direction = 1
        self.move_counter = 0
        
    def run(self):
        # Movement code mixed with strategy
        if self.move_counter < 50:
            self.ahead(20)
        else:
            self.turn_right(30)
            self.ahead(10)
        self.move_counter += 1
        if self.move_counter > 100:
            self.move_counter = 0
            
        # Radar code
        self.turn_radar_right(45)
        
    def on_scanned_robot(self, scanned_robot):
        # Distance calculation
        x_diff = scanned_robot.x - self.x
        y_diff = scanned_robot.y - self.y
        distance = math.sqrt(x_diff**2 + y_diff**2)
        
        # Prediction calculation
        bullet_speed = 20 - 3 * 2
        time = distance / bullet_speed
        heading_rad = math.radians(scanned_robot.heading)
        future_x = scanned_robot.x + scanned_robot.velocity * time * math.sin(heading_rad)
        future_y = scanned_robot.y + scanned_robot.velocity * time * math.cos(heading_rad)
        
        # Angle calculation
        angle = math.degrees(math.atan2(future_x - self.x, future_y - self.y))
        
        # Shooting
        self.turn_gun_to(angle)
        if distance < 200:
            self.fire(3)
        elif distance < 400:
            self.fire(2)
        else:
            self.fire(1)
```

### Problems with This Code:
- ❌ Everything is mixed together
- ❌ Hard to test individual parts
- ❌ Can't reuse the targeting code in another tank
- ❌ Difficult to try different movement strategies
- ❌ If you want to change one thing, you might break another

## Part 2: Classes - Organizing Your Code 📦

### What is a Class Really?

Think of a class like a **blueprint** or a **recipe**:
- A blueprint shows how to build a house
- A class shows how to build an object

Or think of it like a **cookie cutter**:
- The cookie cutter is the class
- Each cookie you make is an object (instance)
- All cookies have the same shape, but can have different decorations

### Your First Helper Class - TargetingSystem

Let's take all the targeting math and put it in its own class:

```python
import math

class TargetingSystem:
    """
    Handles all the math for aiming at enemies
    """
    
    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """Calculate distance between two points"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle to aim from one point to another"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.degrees(math.atan2(x_diff, y_diff))
    
    def predict_position(self, current_x, current_y, velocity, heading, time):
        """Predict where a moving target will be"""
        heading_rad = math.radians(heading)
        future_x = current_x + velocity * time * math.sin(heading_rad)
        future_y = current_y + velocity * time * math.cos(heading_rad)
        return future_x, future_y
    
    def calculate_bullet_speed(self, power):
        """Calculate how fast a bullet travels"""
        return 20 - 3 * power
```

### Why is This Better?

Now you can use it like this:

```python
class CleanTank:
    def __init__(self):
        self.name = "CleanTank"
        # Create a targeting system helper
        self.targeting = TargetingSystem()
    
    def on_scanned_robot(self, scanned_robot):
        # Much easier to read!
        distance = self.targeting.calculate_distance(
            self.x, self.y, 
            scanned_robot.x, scanned_robot.y
        )
        
        # Get bullet speed
        bullet_speed = self.targeting.calculate_bullet_speed(power=2)
        
        # Predict where enemy will be
        time_to_hit = distance / bullet_speed
        future_x, future_y = self.targeting.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )
        
        # Calculate angle to future position
        angle = self.targeting.calculate_angle(
            self.x, self.y,
            future_x, future_y
        )
        
        # Aim and fire!
        self.turn_gun_to(angle)
        self.fire(2)
```

### Benefits:
- ✅ Easy to read - each line says what it does
- ✅ Reusable - use TargetingSystem in ANY tank
- ✅ Testable - test targeting math separately
- ✅ Changeable - improve targeting without touching other code

## Part 3: More Helper Classes - Movement Strategies 🎯

Let's create different movement strategies as separate classes!

### MovementStrategy Base Class

```python
class MovementStrategy:
    """
    Base class for movement strategies
    All movement strategies will have a 'move' method
    """
    
    def move(self, tank):
        """
        This method will be implemented by specific strategies
        tank: the tank object that needs to move
        """
        raise NotImplementedError("Subclass must implement move()")
```

### CircularMovement Strategy

```python
class CircularMovement(MovementStrategy):
    """Move in a circle"""
    
    def __init__(self, radius=100):
        self.radius = radius
        self.angle = 0
    
    def move(self, tank):
        """Move the tank in a circular pattern"""
        tank.ahead(20)
        tank.turn_right(10)
        self.angle += 10
```

### WallAvoidanceMovement Strategy

```python
class WallAvoidanceMovement(MovementStrategy):
    """Move but stay away from walls"""
    
    def __init__(self, margin=50):
        self.margin = margin  # How close to walls we allow
    
    def move(self, tank):
        """Move forward but turn away from walls"""
        # Check if too close to walls
        if tank.x < self.margin:
            tank.turn_right(90)
        elif tank.x > tank.battlefield_width - self.margin:
            tank.turn_left(90)
        elif tank.y < self.margin:
            tank.turn_right(90)
        elif tank.y > tank.battlefield_height - self.margin:
            tank.turn_left(90)
        
        # Move forward
        tank.ahead(30)
```

### RandomDodgeMovement Strategy

```python
import random

class RandomDodgeMovement(MovementStrategy):
    """Move unpredictably to dodge bullets"""
    
    def __init__(self):
        self.move_counter = 0
        self.direction = 1
    
    def move(self, tank):
        """Move in unpredictable patterns"""
        self.move_counter += 1
        
        if self.move_counter > 20:
            # Change direction randomly
            self.direction = random.choice([-1, 1])
            turn_amount = random.randint(30, 90)
            
            if self.direction > 0:
                tank.turn_right(turn_amount)
            else:
                tank.turn_left(turn_amount)
            
            self.move_counter = 0
        
        tank.ahead(20)
```

### Using Movement Strategies

Now your tank can easily switch strategies!

```python
class ModularTank:
    def __init__(self):
        self.name = "ModularTank"
        
        # Choose your movement strategy!
        # self.movement = CircularMovement()
        # self.movement = WallAvoidanceMovement()
        self.movement = RandomDodgeMovement()
        
        # And your targeting system
        self.targeting = TargetingSystem()
    
    def run(self):
        # Just call the movement strategy!
        self.movement.move(self)
        
        # Spin radar to find enemies
        self.turn_radar_right(45)
```

## Part 4: Inheritance - Reusing Code 🧬

### What is Inheritance?

Inheritance is like family traits:
- You inherit your parent's eye color
- A class can inherit methods from a parent class

### Creating a Base Tank Class

```python
import math

class BaseTank:
    """
    Base tank with common functionality
    All your tanks can inherit from this!
    """
    
    def __init__(self):
        self.targeting = TargetingSystem()
    
    def aim_at_target(self, target_x, target_y):
        """Aim gun at a specific position"""
        angle = self.targeting.calculate_angle(
            self.x, self.y,
            target_x, target_y
        )
        self.turn_gun_to(angle)
    
    def aim_at_predicted_position(self, scanned_robot, bullet_power=2):
        """Aim at where enemy will be"""
        distance = self.targeting.calculate_distance(
            self.x, self.y,
            scanned_robot.x, scanned_robot.y
        )
        
        bullet_speed = self.targeting.calculate_bullet_speed(bullet_power)
        time_to_hit = distance / bullet_speed
        
        future_x, future_y = self.targeting.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )
        
        self.aim_at_target(future_x, future_y)
        return distance
    
    def choose_bullet_power(self, distance):
        """Choose appropriate bullet power based on distance"""
        if distance < 200:
            return 3
        elif distance < 400:
            return 2
        else:
            return 1
```

### Creating Tanks That Inherit From BaseTank

```python
class SniperTank(BaseTank):
    """
    A tank that inherits common functionality
    and adds its own special behavior
    """
    
    def __init__(self):
        super().__init__()  # Call parent's __init__
        self.name = "SniperTank"
        self.movement = WallAvoidanceMovement()
    
    def run(self):
        """Our custom run method"""
        self.movement.move(self)
        self.turn_radar_right(45)
    
    def on_scanned_robot(self, scanned_robot):
        """Use inherited aiming methods!"""
        # This uses methods from BaseTank!
        distance = self.aim_at_predicted_position(scanned_robot)
        power = self.choose_bullet_power(distance)
        self.fire(power)
```

```python
class BrawlerTank(BaseTank):
    """
    A different tank with the same parent
    but different behavior
    """
    
    def __init__(self):
        super().__init__()  # Call parent's __init__
        self.name = "BrawlerTank"
        self.movement = RandomDodgeMovement()
    
    def run(self):
        """More aggressive movement"""
        self.movement.move(self)
        self.turn_radar_right(60)  # Faster radar
    
    def on_scanned_robot(self, scanned_robot):
        """Aggressive close-combat style"""
        distance = self.aim_at_predicted_position(scanned_robot)
        
        # Always use high power!
        self.fire(3)
        
        # Chase the enemy!
        angle_to_enemy = self.targeting.calculate_angle(
            self.x, self.y,
            scanned_robot.x, scanned_robot.y
        )
        self.turn_to(angle_to_enemy)
```

## Part 5: Polymorphism - Same Interface, Different Behavior 🎭

### What is Polymorphism?

Polymorphism means "many forms". It's when different classes can be used the same way, but do different things.

Think of it like different musical instruments:
- All can "play()" a note
- But a piano plays differently than a guitar
- You can tell any instrument to "play()" without knowing which type it is

### Creating Different Targeting Systems

```python
class SimpleTargeting:
    """Basic targeting - aim at current position"""
    
    def get_target_position(self, tank, scanned_robot):
        """Return where to aim"""
        return scanned_robot.x, scanned_robot.y

class PredictiveTargeting:
    """Advanced targeting - predict movement"""
    
    def __init__(self):
        self.targeting_math = TargetingSystem()
    
    def get_target_position(self, tank, scanned_robot):
        """Return predicted future position"""
        distance = self.targeting_math.calculate_distance(
            tank.x, tank.y,
            scanned_robot.x, scanned_robot.y
        )
        
        bullet_speed = self.targeting_math.calculate_bullet_speed(2)
        time_to_hit = distance / bullet_speed
        
        future_x, future_y = self.targeting_math.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )
        
        return future_x, future_y

class LeadTargeting:
    """Even more advanced - lead the target extra"""
    
    def __init__(self):
        self.targeting_math = TargetingSystem()
    
    def get_target_position(self, tank, scanned_robot):
        """Return position with extra lead"""
        # Similar to PredictiveTargeting but add 20% more lead
        distance = self.targeting_math.calculate_distance(
            tank.x, tank.y,
            scanned_robot.x, scanned_robot.y
        )
        
        bullet_speed = self.targeting_math.calculate_bullet_speed(2)
        time_to_hit = distance / bullet_speed * 1.2  # 20% more lead!
        
        future_x, future_y = self.targeting_math.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )
        
        return future_x, future_y
```

### Using Polymorphism in Your Tank

```python
class AdaptiveTank:
    """
    A tank that can switch strategies!
    """
    
    def __init__(self):
        self.name = "AdaptiveTank"
        self.targeting_math = TargetingSystem()
        
        # Choose targeting strategy
        # All three have get_target_position() - that's polymorphism!
        # self.targeting_strategy = SimpleTargeting()
        self.targeting_strategy = PredictiveTargeting()
        # self.targeting_strategy = LeadTargeting()
        
        # Choose movement strategy
        self.movement_strategy = RandomDodgeMovement()
    
    def run(self):
        self.movement_strategy.move(self)
        self.turn_radar_right(45)
    
    def on_scanned_robot(self, scanned_robot):
        # Use whichever targeting strategy we chose!
        target_x, target_y = self.targeting_strategy.get_target_position(
            self, scanned_robot
        )
        
        # Aim at the target
        angle = self.targeting_math.calculate_angle(
            self.x, self.y,
            target_x, target_y
        )
        self.turn_gun_to(angle)
        
        # Fire!
        distance = self.targeting_math.calculate_distance(
            self.x, self.y,
            scanned_robot.x, scanned_robot.y
        )
        
        if distance < 200:
            self.fire(3)
        else:
            self.fire(2)
```

## Part 6: Building a Professional Tank Architecture 🏗️

Now let's put it all together into one clean, professional tank!

Create `professional_tank.py`:

```python
"""
Professional Tank - Clean, Modular Architecture
By: [Your Name]
"""
import math
import random


# ============= UTILITY CLASSES =============

class TargetingSystem:
    """Math utilities for targeting"""
    
    def calculate_distance(self, from_x, from_y, to_x, to_y):
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angle(self, from_x, from_y, to_x, to_y):
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.degrees(math.atan2(x_diff, y_diff))
    
    def predict_position(self, x, y, velocity, heading, time):
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y
    
    def calculate_bullet_speed(self, power):
        return 20 - 3 * power


# ============= MOVEMENT STRATEGIES =============

class MovementStrategy:
    """Base class for movement"""
    def move(self, tank):
        raise NotImplementedError()


class DodgeMovement(MovementStrategy):
    """Dodge in unpredictable patterns"""
    
    def __init__(self):
        self.counter = 0
        self.direction = 1
    
    def move(self, tank):
        self.counter += 1
        
        # Check walls
        margin = 50
        if (tank.x < margin or tank.x > tank.battlefield_width - margin or
            tank.y < margin or tank.y > tank.battlefield_height - margin):
            tank.turn_right(90)
        
        # Random direction changes
        if self.counter > 20:
            self.direction = random.choice([-1, 1])
            turn = random.randint(30, 90)
            if self.direction > 0:
                tank.turn_right(turn)
            else:
                tank.turn_left(turn)
            self.counter = 0
        
        tank.ahead(20)


# ============= TARGETING STRATEGIES =============

class TargetingStrategy:
    """Base class for targeting"""
    def get_target_position(self, tank, scanned_robot):
        raise NotImplementedError()


class PredictiveTargeting(TargetingStrategy):
    """Predict where enemy will be"""
    
    def __init__(self):
        self.math = TargetingSystem()
    
    def get_target_position(self, tank, scanned_robot):
        distance = self.math.calculate_distance(
            tank.x, tank.y,
            scanned_robot.x, scanned_robot.y
        )
        
        bullet_speed = self.math.calculate_bullet_speed(2)
        time_to_hit = distance / bullet_speed
        
        return self.math.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )


# ============= BASE TANK =============

class BaseTank:
    """Base class with common tank functionality"""
    
    def __init__(self):
        self.targeting_math = TargetingSystem()
    
    def aim_at(self, target_x, target_y):
        """Aim gun at specific coordinates"""
        angle = self.targeting_math.calculate_angle(
            self.x, self.y,
            target_x, target_y
        )
        self.turn_gun_to(angle)
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        return self.targeting_math.calculate_distance(
            self.x, self.y, x, y
        )


# ============= FINAL TANK =============

class ProfessionalTank(BaseTank):
    """
    A professional, modular tank design
    Easy to modify, test, and improve!
    """
    
    def __init__(self):
        super().__init__()
        self.name = "ProfessionalTank"
        
        # Plug in our strategies
        self.movement = DodgeMovement()
        self.targeting = PredictiveTargeting()
    
    def run(self):
        """Main loop"""
        # Use our movement strategy
        self.movement.move(self)
        
        # Scan for enemies
        self.turn_radar_right(45)
    
    def on_scanned_robot(self, scanned_robot):
        """When we spot an enemy"""
        # Get target position from strategy
        target_x, target_y = self.targeting.get_target_position(
            self, scanned_robot
        )
        
        # Aim at target
        self.aim_at(target_x, target_y)
        
        # Choose power based on distance
        distance = self.distance_to(scanned_robot.x, scanned_robot.y)
        if distance < 200:
            power = 3
        elif distance < 400:
            power = 2
        else:
            power = 1
        
        # Fire!
        self.fire(power)
    
    def on_hit_by_bullet(self, event):
        """React when hit"""
        # Turn perpendicular to dodge
        self.turn_right(90)
        self.ahead(100)
```

## Part 7: Benefits of This Architecture 🌟

### Easy to Modify

Want to change movement? Just swap one line:
```python
# self.movement = DodgeMovement()
self.movement = CircularMovement()
```

### Easy to Test

Test each component separately:
```python
# Test targeting math
targeting = TargetingSystem()
distance = targeting.calculate_distance(0, 0, 300, 400)
print(f"Distance: {distance}")  # Should be 500

# Test prediction
future_x, future_y = targeting.predict_position(100, 100, 5, 0, 10)
print(f"Future position: ({future_x}, {future_y})")
```

### Easy to Extend

Add new strategies without changing existing code:
```python
class SpiralMovement(MovementStrategy):
    """New movement strategy!"""
    
    def __init__(self):
        self.radius = 50
        self.angle = 0
    
    def move(self, tank):
        tank.ahead(20)
        tank.turn_right(15)
        self.radius += 0.5
        self.angle += 15
```

### Reusable

Use the same classes in multiple tanks:
```python
class QuickTank(BaseTank):
    def __init__(self):
        super().__init__()
        self.name = "QuickTank"
        self.movement = DodgeMovement()  # Reuse!
        self.targeting = PredictiveTargeting()  # Reuse!

class SnipeTank(BaseTank):
    def __init__(self):
        super().__init__()
        self.name = "SnipeTank"
        self.movement = CircularMovement()  # Reuse!
        self.targeting = LeadTargeting()  # Reuse!
```

## Part 8: Testing Your Professional Tank 🧪

Let's see if clean code performs better!

### Battle Against Multiple Opponents

```bash
python battle_runner.py Tutorials/Week6_AdvancedPython/professional_tank.py Samples/walls_bot.py
```

### Compare With Earlier Tanks

```bash
# Week 1 vs Professional
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Tutorials/Week6_AdvancedPython/professional_tank.py

# Week 5 vs Professional
python battle_runner.py Tutorials/Week5_AdvancedTargeting/sniper_bot.py Tutorials/Week6_AdvancedPython/professional_tank.py
```

### Test All Samples

```bash
python battle_runner.py Tutorials/Week6_AdvancedPython/professional_tank.py --all-samples
```

## Part 9: Challenges and Experiments 🚀

### Easy Challenges:
1. **Create a New Movement Strategy** - Make a `ZigZagMovement` class
2. **Add Debug Output** - Print which strategy is being used
3. **Test Different Combinations** - Try all movement + targeting combinations

### Medium Challenges:
1. **Adaptive Targeting** - Switch targeting based on enemy distance
2. **Smart Power System** - Create a `PowerStrategy` class
3. **Radar Strategy** - Make radar focusing a separate class

### Hard Challenges:
1. **Machine Learning Tank** - Track which strategies work best and adapt
2. **Multi-Target System** - Handle multiple enemies with different strategies
3. **Energy Management** - Create an `EnergyStrategy` that manages when to shoot

### Expert Challenge:
**Create a Strategy Factory** - Automatically choose the best strategy based on the opponent!

```python
class StrategyFactory:
    """Choose strategies based on opponent behavior"""
    
    def choose_movement(self, opponent_data):
        """Pick best movement for this opponent"""
        if opponent_data.accuracy > 0.5:
            return RandomDodgeMovement()  # They're good, dodge a lot!
        else:
            return CircularMovement()  # They're not good, simple is fine
    
    def choose_targeting(self, opponent_data):
        """Pick best targeting for this opponent"""
        if opponent_data.velocity > 5:
            return LeadTargeting()  # They're fast, lead more
        else:
            return PredictiveTargeting()  # Normal prediction
```

## Part 10: Key Concepts Review 📚

### Classes
- **Definition**: A blueprint for creating objects
- **Purpose**: Organize related data and functions together
- **Example**: `TargetingSystem` groups all targeting math

### Inheritance
- **Definition**: A class can inherit from another class
- **Purpose**: Reuse code without copying it
- **Example**: `SniperTank` and `BrawlerTank` both inherit from `BaseTank`
- **Keyword**: `super()` calls the parent class

### Polymorphism
- **Definition**: Different classes with the same interface
- **Purpose**: Use different implementations the same way
- **Example**: All movement strategies have `move()`, all targeting strategies have `get_target_position()`

### Encapsulation
- **Definition**: Keeping related things together
- **Purpose**: Each class has one clear responsibility
- **Example**: `TargetingSystem` only does math, `MovementStrategy` only does movement

### Composition
- **Definition**: Building complex objects from simpler ones
- **Purpose**: Mix and match components
- **Example**: Tank is composed of a movement strategy + targeting strategy

## Part 11: Professional Coding Practices 💼

### Good Class Names
```python
# Good - clear and descriptive
class PredictiveTargeting:
class RandomDodgeMovement:
class TargetingSystem:

# Bad - unclear
class PT:
class Thing:
class Helper:
```

### Good Method Names
```python
# Good - says what it does
def calculate_distance(self, x1, y1, x2, y2):
def predict_position(self, x, y, velocity, heading, time):

# Bad - unclear
def calc(self, a, b, c, d):
def do_thing(self, stuff):
```

### Comments and Documentation
```python
class TargetingSystem:
    """
    Handles mathematical calculations for targeting enemies
    
    This class provides utilities for:
    - Distance calculations
    - Angle calculations  
    - Position prediction
    - Bullet speed calculations
    """
    
    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """
        Calculate Euclidean distance between two points
        
        Args:
            from_x: Starting X coordinate
            from_y: Starting Y coordinate
            to_x: Ending X coordinate
            to_y: Ending Y coordinate
            
        Returns:
            Float: Distance in pixels
        """
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)
```

### Single Responsibility Principle
Each class should do ONE thing well:
- ✅ `TargetingSystem` - only math
- ✅ `MovementStrategy` - only movement
- ✅ `ProfessionalTank` - coordinates everything
- ❌ A class that does targeting AND movement AND radar

## Part 12: Submit Your Professional Tank! 🏆

Ready to show off your clean code?

1. Test your tank thoroughly
2. Make sure it beats at least 3 sample tanks
3. Copy to `Submissions/YourName/professional_tank.py`
4. Create a Pull Request with title: `[Submission] YourName's Professional Tank`

In your PR description, explain your architecture:
```
## Professional Tank Submission

**Tank Name:** ProfessionalTank
**Week:** Week 6 - Advanced Python

**Architecture:**
- Movement: RandomDodgeMovement with wall avoidance
- Targeting: PredictiveTargeting with distance-based power
- Design: Modular, easy to extend

**Special Features:**
- Clean separation of concerns
- Reusable components
- Easy to test and modify

This tank uses object-oriented principles to create maintainable code!
```

## Homework

Before moving forward:
1. ✅ Refactor one of your earlier tanks using classes
2. ✅ Create at least 2 different movement strategies
3. ✅ Create at least 2 different targeting strategies
4. ✅ Test different strategy combinations
5. ✅ Document your code with comments
6. ✅ Submit your professional tank

**Bonus**: Create a strategy that adapts during the battle!

## What's Next?

You now know how to write clean, professional code! These skills work for ANY programming project, not just tanks:
- Web applications
- Games
- Data analysis
- Machine learning
- Mobile apps

The principles you learned (classes, inheritance, polymorphism) are used by professional programmers every day!

## Quick Reference

### Class Template
```python
class MyClass:
    """What this class does"""
    
    def __init__(self, parameter):
        """Constructor - runs when object is created"""
        self.attribute = parameter
    
    def method(self):
        """A method that does something"""
        return self.attribute
```

### Inheritance Template
```python
class Parent:
    def __init__(self):
        self.shared_data = "I'm shared!"
    
    def shared_method(self):
        print("Parent method")

class Child(Parent):
    def __init__(self):
        super().__init__()  # Call parent constructor
        self.child_data = "I'm specific to child"
    
    def child_method(self):
        print("Child method")
        self.shared_method()  # Can use parent methods!
```

### Strategy Pattern Template
```python
class Strategy:
    def execute(self):
        raise NotImplementedError()

class ConcreteStrategyA(Strategy):
    def execute(self):
        print("Strategy A")

class ConcreteStrategyB(Strategy):
    def execute(self):
        print("Strategy B")

class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def do_something(self):
        self.strategy.execute()

# Usage
context = Context(ConcreteStrategyA())
context.do_something()  # Prints "Strategy A"

context.strategy = ConcreteStrategyB()
context.do_something()  # Prints "Strategy B"
```

## Help!

**"What's the difference between a class and an object?"**
- A class is the blueprint (recipe)
- An object is the actual thing you create (the cookie)
- `TargetingSystem` is a class
- `self.targeting = TargetingSystem()` creates an object

**"When should I use inheritance?"**
- When classes share common functionality
- When you want to reuse code
- Example: Multiple tank types with shared aiming code

**"When should I use composition instead?"**
- When you want to mix and match behaviors
- When behaviors aren't related by "is-a" relationship
- Example: A tank HAS a movement strategy (not IS a movement strategy)

**"My classes are getting complicated!"**
- Break them into smaller classes
- Each class should do ONE thing
- If you can't describe a class in one sentence, it's too big

**"How do I know if my code is 'clean'?"**
- Can you understand it a week later?
- Can someone else understand it?
- Can you change one part without breaking others?
- Is each class/method easy to test?

---

Congratulations! You're now coding like a professional! 🎉

Your code is clean, organized, and ready to grow. These skills will serve you well in all your future programming adventures!
