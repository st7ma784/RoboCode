"""
SittingDuck - The simplest tank possible

Difficulty: ★☆☆☆☆ (Level 1)

This tank demonstrates:
- Minimal tank structure
- Basic shooting
- No movement (easy target for practicing aim)

Perfect for:
- Testing if your tank can hit stationary targets
- Comparing your shooting accuracy
- Your first opponent!
"""

class SittingDuck:
    def __init__(self):
        """Initialize the tank"""
        self.name = "SittingDuck"

    def run(self):
        """
        Main loop - runs every game tick

        This tank does almost nothing!
        Just spins its radar to look for enemies.
        """
        # Spin radar to scan for enemies
        self.turn_radar_right(45)

        # That's it! No movement, minimal strategy

    def on_scanned_robot(self, scanned_robot):
        """
        When we see an enemy - shoot!

        Even though we don't move, we'll shoot back!
        """
        # Just shoot with medium power
        self.fire(2)

    def on_hit_by_bullet(self, bullet):
        """
        When hit by a bullet - just complain!

        We don't even try to dodge.
        """
        print("Ouch! I got hit!")

    # Game engine methods
    def turn_radar_right(self, degrees):
        """Provided by game engine"""
        pass

    def fire(self, power):
        """Provided by game engine"""
        pass


# Why this tank is weak:
# ❌ Doesn't move (easy target)
# ❌ No dodging
# ❌ No aiming (shoots wherever radar happens to be)
# ❌ No strategy
# ✓ But it's simple to understand!
