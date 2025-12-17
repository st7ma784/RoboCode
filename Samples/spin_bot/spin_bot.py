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
        

    async def run(self):
        """
        Main loop - spin in place!

        Strategy: Spin continuously, letting on_scanned_bot handle firing
        when we're pointed at an enemy.
        """
        tick = 0
        while self.is_running():
            tick += 1
           
            # Spin the tank body AND gun together continuously
            self.turn_rate = 20
            self.gun_turn_rate = 20  # Gun spins with body

            # DON'T fire here - let on_scanned_bot handle firing when aimed!

            await self.go()

    async def on_scanned_bot(self, event):
        """
        When we see an enemy - ONLY fire if gun is pointed at them!

        Since we're spinning, we only shoot when we happen to be aimed correctly.
        """
        # Calculate angle to enemy
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        angle_to_enemy = math.degrees(math.atan2(dx, dy))

        # Calculate how far off our gun is from target
        gun_error = angle_to_enemy - self.get_gun_direction()
        # Normalize to -180 to 180
        while gun_error > 180:
            gun_error -= 360
        while gun_error < -180:
            gun_error += 360

        # ONLY fire if gun is pointing close to enemy (within 10 degrees)
        if abs(gun_error) < 10:
            # Calculate distance
            distance = math.sqrt(dx*dx + dy*dy)

            # Choose power based on distance
            if distance < 200:
                await self.fire(3)
            else:
                await self.fire(1)


    async def on_hit_by_bullet(self, event):
        """
        When hit - spin faster!

        Not a great strategy, but better than nothing.
        """

        # Spin to change position slightly
        self.turn_rate = 90


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
