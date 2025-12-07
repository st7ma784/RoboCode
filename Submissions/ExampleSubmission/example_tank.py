"""
Example Tank Submission

This is an example of how to submit your tank.
Replace this with your own tank code!
"""

import math
import random

class ExampleTank:
    """
    Example tank showing proper submission format

    This tank combines skills from all 5 weeks as an example.
    """

    def __init__(self):
        self.name = "ExampleTank"
        self.x = 0
        self.y = 0
        self.heading = 0
        self.energy = 100
        self.battlefield_width = 800
        self.battlefield_height = 600

    def run(self):
        """Main loop"""
        # Boundary checking (Week 3)
        if self.is_too_close_to_wall(50):
            self.avoid_walls()
        else:
            # Simple circular movement
            self.ahead(40)
            self.turn_right(15)

        # Scan for enemies
        self.turn_radar_right(45)

    def on_scanned_robot(self, scanned_robot):
        """When enemy detected"""
        distance = scanned_robot.distance

        # Simple targeting (Week 2)
        angle = self.calculate_angle(
            self.x, self.y,
            scanned_robot.x, scanned_robot.y
        )

        self.turn_gun_to(angle)

        # Power based on distance (Week 5)
        if distance < 200:
            self.fire(3)
        elif distance < 400:
            self.fire(2)
        else:
            self.fire(1)

    def on_hit_by_bullet(self, bullet):
        """React to being hit (Week 4)"""
        # Random dodge
        if random.random() < 0.5:
            self.turn_right(90)
        else:
            self.turn_left(90)
        self.ahead(80)

    def is_too_close_to_wall(self, margin):
        """Boundary check (Week 3)"""
        return (self.x < margin or
                self.x > self.battlefield_width - margin or
                self.y < margin or
                self.y > self.battlefield_height - margin)

    def avoid_walls(self):
        """Wall avoidance (Week 3)"""
        center_x = self.battlefield_width / 2
        center_y = self.battlefield_height / 2
        angle = self.calculate_angle(self.x, self.y, center_x, center_y)
        self.turn_to(angle)
        self.ahead(60)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Angle calculation (Week 2)"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    # Game engine methods (provided by framework)
    def ahead(self, distance):
        pass

    def turn_right(self, degrees):
        pass

    def turn_left(self, degrees):
        pass

    def turn_to(self, degrees):
        pass

    def turn_radar_right(self, degrees):
        pass

    def turn_gun_to(self, angle):
        pass

    def fire(self, power):
        pass
