"""
SpinBot - A simple spinning tank

Difficulty: ★★☆☆☆ (Level 2)

This tank demonstrates:
- Continuous rotation (spinning)
- Coordinated movement
- Basic shooting

Good for:
- Learning basic movement patterns
- Understanding the spin strategy
- Still relatively easy to beat
"""

class SpinBot:
    def __init__(self):
        """Initialize the tank"""
        self.name = "SpinBot"

    def run(self):
        """
        Main loop - spin and shoot!

        Strategy: Spin in place while radar scans.
        The spinning makes us slightly harder to hit than SittingDuck.
        """
        # Spin the tank body
        self.turn_right(20)

        # Spin the radar faster to scan
        self.turn_radar_right(45)

        # Shoot periodically
        self.fire(1)

    def on_scanned_robot(self, scanned_robot):
        """
        When we see an enemy - shoot harder!

        We shoot with more power when we detect someone.
        """
        print(f"Enemy spotted at distance {scanned_robot.distance:.0f}!")

        # Choose power based on distance
        if scanned_robot.distance < 200:
            # Close range - use high power
            self.fire(3)
        else:
            # Far away - use low power
            self.fire(1)

    def on_hit_by_bullet(self, bullet):
        """
        When hit - spin faster!

        Not a great strategy, but better than nothing.
        """
        print("Got hit! Spinning faster!")

        # Spin to change position slightly
        self.turn_right(90)

    def on_hit_wall(self, wall):
        """
        If we somehow hit a wall (we shouldn't since we don't move)

        Just in case!
        """
        print("Hit a wall? How did that happen?")

    # Game engine methods
    def turn_right(self, degrees):
        pass

    def turn_radar_right(self, degrees):
        pass

    def fire(self, power):
        pass


# Strengths:
# ✓ Slightly harder to hit than SittingDuck
# ✓ Scans area quickly with spinning radar
# ✓ Adjusts power based on distance

# Weaknesses:
# ❌ Still doesn't move from starting position
# ❌ No real dodging strategy
# ❌ Predictable spinning pattern
# ❌ No aiming - shoots randomly
