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

from robocode_tank_royale.bot_api import Bot, BotInfo

class SittingDuck(Bot):
    """The simplest tank - doesn't move, just shoots"""

    async def run(self):
        """
        Main loop - runs every game tick

        This tank does almost nothing!
        Just spins its radar to look for enemies.
        """
        while True:
            # Spin radar to scan for enemies
            self.turn_radar_right(45)

            # That's it! No movement, minimal strategy
            await self.go()

    def on_scanned_bot(self, event):
        """
        When we see an enemy - shoot!

        Even though we don't move, we'll shoot back!
        """
        # Just shoot with medium power
        self.fire(2)

    def on_hit_by_bullet(self, event):
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
