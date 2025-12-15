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

from robocode_tank_royale.bot_api import BaseBot, BotInfo

class SpinBot(BaseBot):
    """A spinning tank that shoots while rotating"""

    async def run(self):
        """
        Main loop - spin and shoot!

        Strategy: Spin in place while radar scans.
        The spinning makes us slightly harder to hit than SittingDuck.
        """
        while True:
            # Spin the tank body
            self.turn_right(20)

            # Spin the radar faster to scan
            self.turn_radar_right(45)

            # Shoot periodically
            self.fire(1)
            
            await self.go()

    def on_scanned_bot(self, event):
        """
        When we see an enemy - shoot harder!

        We shoot with more power when we detect someone.
        """
        print(f"Enemy spotted at distance {event.distance:.0f}!")

        # Choose power based on distance
        if event.distance < 200:
            # Close range - use high power
            self.fire(3)
        else:
            # Far away - use low power
            self.fire(1)

    def on_hit_by_bullet(self, event):
        """
        When hit - spin faster!

        Not a great strategy, but better than nothing.
        """
        print("Got hit! Spinning faster!")

        # Spin to change position slightly
        self.turn_right(90)

    def on_hit_wall(self, event):
        """
        If we somehow hit a wall (we shouldn't since we don't move)

        Just in case!
        """
        print("Hit a wall? How did that happen?")


# Strengths:
# ✓ Slightly harder to hit than SittingDuck
# ✓ Scans area quickly with spinning radar
# ✓ Adjusts power based on distance

# Weaknesses:
# ❌ Still doesn't move from starting position
# ❌ No real dodging strategy
# ❌ Predictable spinning pattern
# ❌ No aiming - shoots randomly

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "spin_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = SpinBot(bot_info=bot_info)
    asyncio.run(bot.start())
