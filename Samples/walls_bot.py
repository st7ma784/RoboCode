"""
WallsBot - Drives around the perimeter

Difficulty: ★★★☆☆ (Level 3)

This tank demonstrates:
- Movement along boundaries
- Wall detection and avoidance
- Perimeter patrol strategy
- Basic aiming

Good for:
- Learning wall avoidance
- Understanding perimeter movement
- Practicing against moving targets
"""

import math

class WallsBot:
    def __init__(self):
        """Initialize the tank"""
        self.name = "WallsBot"
        self.x = 0
        self.y = 0
        self.heading = 0
        self.battlefield_width = 800
        self.battlefield_height = 600

        # How close to walls we want to stay
        self.wall_distance = 50

    def run(self):
        """
        Main loop - drive along the walls!

        Strategy: Stay near the perimeter of the arena.
        This gives us walls at our back (fewer angles to defend).
        """
        # Keep radar spinning
        self.turn_radar_right(45)

        # Check if we're too far from walls
        if self.too_far_from_walls():
            # Move toward nearest wall
            self.move_to_wall()
        else:
            # Drive along the wall
            self.follow_wall()

    def too_far_from_walls(self):
        """Check if we're too far from any wall"""
        min_distance = min(
            self.x,  # Distance to left wall
            self.battlefield_width - self.x,  # Distance to right wall
            self.y,  # Distance to top wall
            self.battlefield_height - self.y  # Distance to bottom wall
        )
        return min_distance > self.wall_distance + 30

    def move_to_wall(self):
        """Move toward the nearest wall"""
        # Find nearest wall
        distances = {
            'left': self.x,
            'right': self.battlefield_width - self.x,
            'top': self.y,
            'bottom': self.battlefield_height - self.y
        }

        nearest = min(distances, key=distances.get)

        # Turn toward that wall
        if nearest == 'left':
            self.turn_to(270)  # West
        elif nearest == 'right':
            self.turn_to(90)   # East
        elif nearest == 'top':
            self.turn_to(0)    # North
        else:
            self.turn_to(180)  # South

        self.ahead(30)

    def follow_wall(self):
        """Drive along the perimeter"""
        # Move forward along current heading
        self.ahead(50)

        # Check if we're getting too close to a wall ahead
        if self.wall_ahead():
            # Turn to follow wall around corner
            self.turn_right(90)

    def wall_ahead(self):
        """Check if there's a wall directly ahead"""
        # Simple check based on heading and position
        margin = 60

        if self.heading < 45 or self.heading > 315:
            # Facing up
            return self.y < margin
        elif 45 <= self.heading < 135:
            # Facing right
            return self.x > (self.battlefield_width - margin)
        elif 135 <= self.heading < 225:
            # Facing down
            return self.y > (self.battlefield_height - margin)
        else:
            # Facing left
            return self.x < margin

    def on_scanned_robot(self, scanned_robot):
        """
        When we see an enemy - aim and shoot!

        This uses basic aiming toward enemy's current position.
        """
        # Calculate angle to enemy
        angle = self.calculate_angle(
            self.x, self.y,
            scanned_robot.x, scanned_robot.y
        )

        # Aim gun at enemy
        self.turn_gun_to(angle)

        # Shoot based on distance
        if scanned_robot.distance < 200:
            self.fire(3)
        elif scanned_robot.distance < 400:
            self.fire(2)
        else:
            self.fire(1)

    def on_hit_by_bullet(self, bullet):
        """React to being hit"""
        print("Hit! Continuing perimeter patrol...")
        # Keep moving along wall
        self.ahead(100)

    def on_hit_wall(self, wall):
        """If we hit a wall, turn and continue"""
        print("Bumped into wall!")
        self.back(20)
        self.turn_right(90)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle from one point to another"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    # Game engine methods
    def turn_to(self, degrees):
        pass

    def turn_right(self, degrees):
        pass

    def ahead(self, distance):
        pass

    def back(self, distance):
        pass

    def turn_radar_right(self, degrees):
        pass

    def turn_gun_to(self, angle):
        pass

    def fire(self, power):
        pass


# Strengths:
# ✓ Actually moves around the arena
# ✓ Uses walls as protection
# ✓ Has basic aiming
# ✓ Adjusts fire power based on distance
# ✓ Handles wall collisions

# Weaknesses:
# ❌ Predictable movement pattern (follows walls)
# ❌ No prediction of enemy movement
# ❌ Doesn't dodge when hit
# ❌ Can be cornered
