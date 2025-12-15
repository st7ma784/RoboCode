"""
My First Tank!
This tank spins around and shoots.

Week 1 Tutorial - Starter Tank
"""

from robocode_tank_royale.bot_api import BaseBot, BotInfo

class MyFirstTank(BaseBot):
    """Your very first tank - simple and beginner-friendly!"""

    async def run(self):
        """This is the tank's brain - it runs over and over!"""
        while True:
            # Spin our tank
            self.turn_right(10)

            # Move forward a little
            self.forward(20)

            # Shoot!
            self.fire(1)
            
            await self.go()

    def on_scanned_bot(self, event):
        """Called when we see an enemy tank!"""
        print(f"I see an enemy at {event.distance} units away!")
        # Shoot at them!
        self.fire(3)

    def on_hit_by_bullet(self, event):
        """Called when we get hit by a bullet!"""
        print("Ouch! I got hit!")
        # Turn around to face attacker
        self.turn_right(90)


if __name__ == "__main__":
    bot = MyFirstTank()
    bot.start()
