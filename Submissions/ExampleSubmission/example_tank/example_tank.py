"""
Example Tank Submission

This is an example of how to submit your tank.
Replace this with your own tank code!
"""

from robocode_tank_royale.bot_api import Bot, BotInfo
import math
import random

class ExampleTank(Bot):
    """
    Example tank showing proper submission format

    This tank combines skills from all 5 weeks as an example.
    """

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        self.name = "ExampleTank"


    def calc_gun_turn(self, target_angle):
        """Calculate gun turn needed to face target angle"""
        diff = target_angle - self.get_gun_direction()
        # Normalize to -180 to 180
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        return diff

    def turn_to(self, target_angle):
        """Helper to turn to absolute angle"""
        current = self.get_direction() % 360
        target = target_angle % 360
        diff = (target - current + 180) % 360 - 180
        if diff < 0:
            self.turn_rate = -(abs(diff))
        else:
            self.turn_rate = diff

    async def run(self):
        """Main loop"""
        while self.is_running():
            # Boundary checking (Week 3)
            if self.is_too_close_to_wall(50):
                self.avoid_walls()
            else:
                # Simple circular movement
                self.target_speed = 40
                self.turn_rate = 15

            # Scan for enemies
            self.radar_turn_rate = 45
            
            await self.go()

    async def on_scanned_bot(self, event):
        """When enemy detected"""
        distance = event.distance

        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.get_x() + distance * math.sin(bearing_rad)
        enemy_y = self.get_y() + distance * math.cos(bearing_rad)

        # Simple targeting (Week 2)
        angle = self.calculate_angle(
            self.get_x(), self.get_y(),
            enemy_x, enemy_y
        )

        self.gun_turn_rate = self.calc_gun_turn(angle)

        # Power based on distance (Week 5)
        if distance < 200:
            await self.fire(3)
        elif distance < 400:
            await self.fire(2)
        else:
            await self.fire(1)

    async def on_hit_by_bullet(self, event):
        """React to being hit (Week 4)"""
        # Random dodge
        if random.random() < 0.5:
            self.turn_rate = 90
        else:
            self.turn_rate = -(90)
        self.target_speed = 80

    def is_too_close_to_wall(self, margin):
        """Boundary check (Week 3)"""
        return (self.get_x() < margin or
                self.get_x() > self.get_arena_width() - margin or
                self.get_y() < margin or
                self.get_y() > self.get_arena_height() - margin)

    def avoid_walls(self):
        """Wall avoidance (Week 3)"""
        center_x = self.get_arena_width() / 2
        center_y = self.get_arena_height() / 2
        angle = self.calculate_angle(self.get_x(), self.get_y(), center_x, center_y)
        self.turn_to(angle)
        self.target_speed = 60

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Angle calculation (Week 2)"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))


# Main entry point

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "example_tank.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = ExampleTank(bot_info=bot_info)
    asyncio.run(bot.start())
