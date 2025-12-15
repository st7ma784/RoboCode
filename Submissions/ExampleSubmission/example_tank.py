"""
Example Tank Submission

This is an example of how to submit your tank.
Replace this with your own tank code!
"""

from robocode_tank_royale.bot_api import BaseBot, BotInfo
import math
import random

class ExampleTank(BaseBot):
    """
    Example tank showing proper submission format

    This tank combines skills from all 5 weeks as an example.
    """

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        self.name = "ExampleTank"

    def turn_to(self, target_angle):
        """Helper to turn to absolute angle"""
        current = self.direction % 360
        target = target_angle % 360
        diff = (target - current + 180) % 360 - 180
        if diff < 0:
            self.turn_left(abs(diff))
        else:
            self.turn_right(diff)

    async def run(self):
        """Main loop"""
        while True:
            # Boundary checking (Week 3)
            if self.is_too_close_to_wall(50):
                self.avoid_walls()
            else:
                # Simple circular movement
                self.forward(40)
                self.turn_right(15)

            # Scan for enemies
            self.turn_radar_right(45)
            
            await self.go()

    def on_scanned_bot(self, event):
        """When enemy detected"""
        distance = event.distance

        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.x + distance * math.sin(bearing_rad)
        enemy_y = self.y + distance * math.cos(bearing_rad)

        # Simple targeting (Week 2)
        angle = self.calculate_angle(
            self.x, self.y,
            enemy_x, enemy_y
        )

        self.turn_gun_to(angle)

        # Power based on distance (Week 5)
        if distance < 200:
            self.fire(3)
        elif distance < 400:
            self.fire(2)
        else:
            self.fire(1)

    def on_hit_by_bullet(self, event):
        """React to being hit (Week 4)"""
        # Random dodge
        if random.random() < 0.5:
            self.turn_right(90)
        else:
            self.turn_left(90)
        self.forward(80)

    def is_too_close_to_wall(self, margin):
        """Boundary check (Week 3)"""
        return (self.x < margin or
                self.x > self.arena_width - margin or
                self.y < margin or
                self.y > self.arena_height - margin)

    def avoid_walls(self):
        """Wall avoidance (Week 3)"""
        center_x = self.arena_width / 2
        center_y = self.arena_height / 2
        angle = self.calculate_angle(self.x, self.y, center_x, center_y)
        self.turn_to(angle)
        self.forward(60)

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
