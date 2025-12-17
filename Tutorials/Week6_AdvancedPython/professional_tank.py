"""
Professional Tank - Clean, Modular Architecture
Week 6: Advanced Python - Classes and Clean Code

This tank demonstrates:
- Class organization
- Inheritance
- Polymorphism
- Strategy pattern
- Clean, maintainable code
"""
from robocode_tank_royale.bot_api import Bot, BotInfo
import math
import random


# ============= UTILITY CLASSES =============

class TargetingSystem:
    """
    Math utilities for targeting enemies
    
    This class encapsulates all the mathematical calculations
    needed for aiming and shooting at targets.
    """
    
    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """Calculate distance between two points using Pythagorean theorem"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle to aim from one point to another"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.degrees(math.atan2(x_diff, y_diff))
    
    def predict_position(self, x, y, velocity, heading, time):
        """
        Predict where a moving target will be in the future
        
        Args:
            x, y: Current position
            velocity: How fast the target is moving
            heading: Direction the target is moving (degrees)
            time: How many ticks in the future to predict
            
        Returns:
            Tuple of (future_x, future_y)
        """
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y
    
    def calculate_bullet_speed(self, power):
        """Calculate how fast a bullet travels based on its power"""
        return 20 - 3 * power


# ============= MOVEMENT STRATEGIES =============

class MovementStrategy:
    """
    Base class for movement strategies
    
    All movement strategies must implement the move() method.
    This is an example of polymorphism - different strategies,
    same interface.
    """
    
    def move(self, tank):
        """
        Move the tank according to this strategy
        
        Args:
            tank: The tank object to move
        """
        raise NotImplementedError("Subclass must implement move()")


class DodgeMovement(MovementStrategy):
    """
    Movement strategy that dodges in unpredictable patterns
    and avoids walls
    """
    
    def __init__(self):
        self.counter = 0
        self.direction = 1
    
    def move(self, tank):
        """Move with random dodging and wall avoidance"""
        self.counter += 1
        
        # Wall avoidance
        margin = 50
        if tank.get_x() < margin:
            tank.turn_right(90)
        elif tank.get_x() > tank.get_arena_width() - margin:
            tank.turn_left(90)
        elif tank.get_y() < margin:
            tank.turn_right(90)
        elif tank.get_y() > tank.get_arena_height() - margin:
            tank.turn_left(90)
        
        # Random direction changes for unpredictability
        if self.counter > 20:
            self.direction = random.choice([-1, 1])
            turn = random.randint(30, 90)
            
            if self.direction > 0:
                tank.turn_right(turn)
            else:
                tank.turn_left(turn)
            
            self.counter = 0
        
        # Move forward
        tank.ahead(20)


class CircularMovement(MovementStrategy):
    """
    Movement strategy that moves in circular patterns
    Simple but effective for dodging
    """
    
    def __init__(self, radius=100):
        self.radius = radius
        self.angle = 0
    
    def move(self, tank):
        """Move in a circular pattern"""
        tank.forward(20)
        tank.turn_right(10)
        self.angle += 10


# ============= TARGETING STRATEGIES =============

class TargetingStrategy:
    """
    Base class for targeting strategies
    
    All targeting strategies must implement get_target_position().
    This allows us to easily swap targeting algorithms.
    """
    
    def get_target_position(self, tank, scanned_robot):
        """
        Calculate where to aim
        
        Args:
            tank: Our tank
            scanned_robot: The enemy we scanned
            
        Returns:
            Tuple of (target_x, target_y)
        """
        raise NotImplementedError("Subclass must implement get_target_position()")


class SimpleTargeting(TargetingStrategy):
    """
    Simple targeting - just aim at current position
    Good for stationary or slow targets
    """
    
    def get_target_position(self, tank, scanned_robot):
        """Return enemy's current position"""
        return scanned_robot.x, scanned_robot.y


class PredictiveTargeting(TargetingStrategy):
    """
    Advanced targeting - predict where enemy will be
    Much better for moving targets
    """
    
    def __init__(self, bullet_power=2):
        self.math = TargetingSystem()
        self.bullet_power = bullet_power
    
    def get_target_position(self, tank, scanned_robot):
        """Return predicted future position of enemy"""
        # Calculate current distance
        distance = self.math.calculate_distance(
            tank.x, tank.y,
            scanned_robot.x, scanned_robot.y
        )
        
        # Calculate bullet travel time
        bullet_speed = self.math.calculate_bullet_speed(self.bullet_power)
        time_to_hit = distance / bullet_speed
        
        # Predict where enemy will be
        future_x, future_y = self.math.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            scanned_robot.velocity,
            scanned_robot.heading,
            time_to_hit
        )
        
        return future_x, future_y


# ============= BASE TANK =============

class BaseTank(Bot):
    """
    Base class with common tank functionality
    
    This demonstrates inheritance - other tanks can inherit
    these useful methods without rewriting them.
    """
    
    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        self.targeting_math = TargetingSystem()
    
    def aim_at(self, target_x, target_y):
        """
        Aim gun at specific coordinates
        
        This is a helper method that any tank can use
        """
        angle = self.targeting_math.calculate_angle(
            self.get_x(), self.get_y(),
            target_x, target_y
        )
        self.turn_gun_to(angle)
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        return self.targeting_math.calculate_distance(
            self.get_x(), self.get_y(), x, y
        )
    
    def choose_bullet_power(self, distance):
        """
        Choose appropriate bullet power based on distance
        
        Close range: Power 3 (slow but devastating)
        Medium range: Power 2 (balanced)
        Long range: Power 1 (fast but weak)
        """
        if distance < 200:
            return 3
        elif distance < 400:
            return 2
        else:
            return 1


# ============= FINAL TANK =============

class ProfessionalTank(BaseTank):
    """
    A professional, modular tank design
    
    This tank demonstrates all the principles we learned:
    - Classes: Organized into logical components
    - Inheritance: Inherits from BaseTank
    - Polymorphism: Uses strategy pattern for movement/targeting
    - Encapsulation: Each class has a single responsibility
    - Composition: Built from smaller, reusable pieces
    
    Easy to modify, test, and improve!
    """
    
    def __init__(self, bot_info=None):
        # Call parent class constructor
        super().__init__(bot_info=bot_info)
        
        self.name = "ProfessionalTank"
        
        # Composition: Our tank is composed of strategies
        # Want different behavior? Just swap these out!
        self.movement = DodgeMovement()
        # self.movement = CircularMovement()
        
        self.targeting = PredictiveTargeting(bullet_power=2)
        # self.targeting = SimpleTargeting()
    
    async def run(self):
        """
        Main loop - runs every tick
        
        Notice how clean this is! The complexity is hidden
        in the strategy classes.
        """
        while True:
            # Use our movement strategy
            self.movement.move(self)
            
            # Scan for enemies
            self.turn_radar_right(45)
            
            await self.go()
    
    def on_scanned_bot(self, event):
        """
        Called when we spot an enemy
        
        This method is clean and easy to understand because
        we delegated the complex logic to other classes.
        """
        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.get_x() + event.distance * math.sin(bearing_rad)
        enemy_y = self.get_y() + event.distance * math.cos(bearing_rad)
        
        # Create scanned_robot object for strategy compatibility
        class ScannedRobot:
            def __init__(self, x, y, speed, direction, energy):
                self.x = x
                self.y = y
                self.speed = speed
                self.direction = direction
                self.energy = energy
        
        scanned_robot = ScannedRobot(enemy_x, enemy_y, event.speed, event.direction, event.energy)
        
        # Get target position from our targeting strategy
        target_x, target_y = self.targeting.get_target_position(
            self, scanned_robot
        )
        
        # Aim at the target (using inherited method!)
        self.aim_at(target_x, target_y)
        
        # Choose appropriate power (using inherited method!)
        distance = self.distance_to(enemy_x, enemy_y)
        power = self.choose_bullet_power(distance)
        
        # Fire!
        self.fire(power)
        
        # Optional: Print debug info
        print(f"Targeting enemy at distance {distance:.0f}, power {power}")
    
    def on_hit_by_bullet(self, event):
        """
        React when we get hit
        
        Simple reaction: Turn perpendicular and dodge
        """
        self.turn_right(90)
        self.forward(100)
    
    def on_hit_wall(self, event):
        """
        React when we hit a wall
        
        Back up and turn around
        """
        self.back(50)
        self.turn_right(90)


# Alternative tank using the same components!
class SniperTank(BaseTank):
    """
    A sniper variant - same base, different strategy
    
    This demonstrates how easy it is to create variations
    when you have a clean architecture.
    """
    
    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        self.name = "SniperTank"
        
        # Different strategy combination!
        self.movement = CircularMovement(radius=150)
        self.targeting = PredictiveTargeting(bullet_power=1)  # Fast bullets
    
    async def run(self):
        while True:
            self.movement.move(self)
            self.turn_radar_right(30)  # Slower, more deliberate scanning
            await self.go()
    
    def on_scanned_bot(self, event):
        # Similar logic, but always uses power 1 for speed
        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.get_x() + event.distance * math.sin(bearing_rad)
        enemy_y = self.get_y() + event.distance * math.cos(bearing_rad)
        
        # Create scanned_robot object for strategy compatibility
        class ScannedRobot:
            def __init__(self, x, y, speed, direction, energy):
                self.x = x
                self.y = y
                self.speed = speed
                self.direction = direction
                self.energy = energy
        
        scanned_robot = ScannedRobot(enemy_x, enemy_y, event.speed, event.direction, event.energy)
        
        target_x, target_y = self.targeting.get_target_position(
            self, scanned_robot
        )
        self.aim_at(target_x, target_y)
        self.fire(1)  # Always fast bullets!


# Main entry point

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "professional_tank.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = ProfessionalTank(bot_info=bot_info)
    asyncio.run(bot.start())
