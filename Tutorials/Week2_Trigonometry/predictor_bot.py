"""
PredictorBot - A tank that predicts enemy movement!

Week 2 Tutorial - Learning Trigonometry
This tank uses math to predict where enemies will be and shoots at their future position.
"""
import math

class PredictorBot:
    def __init__(self):
        self.name = "PredictorBot"
        # We'll store our position (game engine sets these)
        self.x = 0
        self.y = 0

    def run(self):
        """Main loop - runs every game tick"""
        # Spin radar to look for enemies
        self.turn_radar_right(45)

        # Move in a circle to dodge bullets
        self.ahead(50)
        self.turn_right(15)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """
        Calculate angle from one point to another

        Returns: angle in degrees
        """
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """
        Calculate distance between two points using Pythagorean theorem

        Returns: distance in pixels
        """
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)

    def predict_position(self, x, y, velocity, heading, time):
        """
        Predict future position of a moving tank

        x, y: current position
        velocity: speed of movement
        heading: direction of movement (degrees)
        time: how many game ticks in the future

        Returns: (future_x, future_y)
        """
        # Convert heading to radians for math functions
        heading_rad = math.radians(heading)

        # Calculate future position
        # sin for X movement, cos for Y movement
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)

        return future_x, future_y

    def on_scanned_robot(self, scanned_robot):
        """When we see an enemy - predict and shoot!"""
        # Bullet speed based on power (official formula)
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power

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

        print(f"Enemy spotted at distance {scanned_robot.distance:.1f}")
        print(f"Predicted future position: ({future_x:.1f}, {future_y:.1f})")

    def on_hit_by_bullet(self, hit_by_bullet):
        """React when hit - dodge!"""
        print("Ouch! Dodging!")
        # Turn perpendicular to the bullet to dodge better
        self.turn_right(90)
        self.ahead(100)

    def on_hit_wall(self, hit_wall):
        """React when we hit a wall"""
        print("Hit a wall! Backing up...")
        # Back up and turn
        self.back(50)
        self.turn_right(90)

    # These methods are provided by the game engine
    # We're just defining them here for reference
    def turn_radar_right(self, degrees):
        pass

    def ahead(self, distance):
        pass

    def turn_right(self, degrees):
        pass

    def turn_gun_to(self, angle):
        pass

    def fire(self, power):
        pass

    def back(self, distance):
        pass
