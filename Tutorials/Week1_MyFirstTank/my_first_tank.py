"""
My First Tank!
This tank spins around and shoots.

Week 1 Tutorial - Starter Tank
"""

from robocode_tank_royale.bot_api import Bot, BotInfo

class MyFirstTank(Bot):
    """Your very first tank - simple and beginner-friendly!"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # IMPORTANT: These flags let gun/radar move independently from body!
        # Without these, turning your body would mess up your aim
        self.set_adjust_gun_for_body_turn(True)
        self.set_adjust_radar_for_body_turn(True)
        self.set_adjust_radar_for_gun_turn(True)

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
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "my_first_tank.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = MyFirstTank(bot_info=bot_info)
    asyncio.run(bot.start())
