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

from robocode_tank_royale.bot_api import Bot, BotInfo, Color
import math
class SpinBot(Bot):
    """A spinning tank that shoots while rotating"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set distinctive color - ORANGE!
        self.body_color = Color.from_rgb(255, 152, 0)  # Orange
        self.turret_color = Color.from_rgb(255, 87, 34)  # Deep Orange
        self.radar_color = Color.from_rgb(255, 193, 7)  # Amber
        
        print("🌀 SpinBot initialized! Spinning up!")

    async def run(self):
        """
        Main loop - spin and shoot!

        Strategy: Spin in place while radar scans.
        The spinning makes us slightly harder to hit than SittingDuck.
        """
        print("🌀 SpinBot.run() started!")
        tick = 0
        while self.is_running():
            tick += 1
            if tick % 100 == 0:
                print(f"🌀 SpinBot tick {tick}, energy: {self.get_energy():.1f}, direction: {self.get_direction():.0f}°")
            
            # Spin the tank body
            self.turn_rate = 20


            # Shoot periodically
            await self.fire(1)
            
            await self.go()

    async def on_scanned_bot(self, event):
        """
        When we see an enemy - shoot harder!

        We shoot with more power when we detect someone.
        """
        print(f"Enemy spotted at distance {event}!")
        distance_x=(self.get_x()-event.x)**2
        distance_y=(self.get_y()-event.y)**2

        distance=math.sqrt(distance_x+distance_y)
        # Choose power based on distance
        if distance < 200:
            # Close range - use high power
            await self.fire(3)
        else:
            # Far away - use low power
            await self.fire(1)

    async def on_hit_by_bullet(self, event):
        """
        When hit - spin faster!

        Not a great strategy, but better than nothing.
        """
        print("Got hit! Spinning faster!")

        # Spin to change position slightly
        self.turn_rate = 90

    async def on_hit_wall(self, event):
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
