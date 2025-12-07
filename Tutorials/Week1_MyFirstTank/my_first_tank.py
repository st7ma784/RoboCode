"""
My First Tank!
This tank spins around and shoots.

Week 1 Tutorial - Starter Tank
"""

class MyFirstTank:
    def __init__(self):
        """Set up our tank when it starts"""
        self.name = "MyFirstTank"

    def run(self):
        """This is the tank's brain - it runs over and over!"""
        # Spin our tank
        self.turn_right(10)

        # Move forward a little
        self.ahead(20)

        # Shoot!
        self.fire(1)

    def on_scanned_robot(self, scanned_robot):
        """Called when we see an enemy tank!"""
        print(f"I see an enemy at {scanned_robot.distance} units away!")
        # Shoot at them!
        self.fire(3)

    def on_hit_by_bullet(self, hit_by_bullet):
        """Called when we get hit by a bullet!"""
        print("Ouch! I got hit!")
        # Turn around to face attacker
        self.turn_right(90)

    # These methods will be provided by the game engine
    # We're just showing what they look like here
    def turn_right(self, degrees):
        """Turn the tank right"""
        pass

    def turn_left(self, degrees):
        """Turn the tank left"""
        pass

    def ahead(self, distance):
        """Move forward"""
        pass

    def back(self, distance):
        """Move backward"""
        pass

    def fire(self, power):
        """Shoot a bullet (power 1-3)"""
        pass
