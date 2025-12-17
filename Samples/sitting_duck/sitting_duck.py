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

from robocode_tank_royale.bot_api import Bot, BotInfo, Color

class SittingDuck(Bot):
    """The simplest tank - doesn't move, just shoots"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set distinctive color - RED!
        self.body_color = Color.from_rgb(244, 67, 54)  # Red
        self.turret_color = Color.from_rgb(233, 30, 99)  # Pink
        self.radar_color = Color.from_rgb(156, 39, 176)  # Purple
        

    async def run(self):
        """
        Main loop - runs every game tick

        This tank does almost nothing!
        Just spins its radar to look for enemies.
        """
        while self.is_running():
         
            # Spin radar to scan for enemies

            # That's it! No movement, minimal strategy
            await self.go()

    async def on_scanned_bot(self, event):
        """
        When we see an enemy - shoot!

        Even though we don't move, we'll shoot back!
        """
        # Just shoot with medium power
        await self.fire(2)

    async def on_hit_by_bullet(self, event):
        """
        When hit by a bullet - just complain!

        We don't even try to dodge.
        """
        print("Ouch! I got hit!")


# Why this tank is weak:
# ❌ Doesn't move (easy target)
# ❌ No dodging
# ❌ No aiming (shoots wherever radar happens to be)
# ❌ No strategy
# ✓ But it's simple to understand!

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "sitting_duck.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = SittingDuck(bot_info=bot_info)
    asyncio.run(bot.start())
