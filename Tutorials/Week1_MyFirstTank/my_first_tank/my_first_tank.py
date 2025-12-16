"""
My First Tank!
This tank spins around and shoots.

Week 1 Tutorial - Starter Tank
"""

from robocode_tank_royale.bot_api import Bot, BotInfo

class MyFirstTank(Bot):
    """Your very first tank - simple and beginner-friendly!"""

    async def run(self):
        """This is the tank's brain - it runs over and over!"""
        while self.is_running():
            # Spin our tank
            self.turn_rate = 10

            # Move forward a little
            self.target_speed = 20

            # Shoot!
            await self.fire(1)
            
            await self.go()

    async def on_scanned_bot(self, event):
        """Called when we see an enemy tank!"""
        # Calculate distance from coordinates
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)
        print(f"I see an enemy at {distance:.1f} units away!")
        # Shoot at them!
        await self.fire(3)

    async def on_hit_by_bullet(self, event):
        """Called when we get hit by a bullet!"""
        print("Ouch! I got hit!")
        # Turn around to face attacker
        self.turn_rate = 90

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
