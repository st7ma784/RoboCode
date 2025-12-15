"""
WallsBot - Drives around the perimeter

Difficulty: ★★★☆☆ (Level 3)

This tank demonstrates:
- Movement along boundaries
- Wall detection and avoidance
- Perimeter patrol strategy
- Basic aiming

Good for:
- Learning wall avoidance
- Understanding perimeter movement
- Practicing against moving targets
"""

import math
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class WallsBot(BaseBot):
    """Patrols the perimeter of the arena"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        # How close to walls we want to stay
        self.wall_distance = 50

    async def run(self):
        """
        Main loop - drive along the walls!

        Strategy: Stay near the perimeter of the arena.
        This gives us walls at our back (fewer angles to defend).
        """
        while True:
            # Keep radar spinning
            self.turn_radar_right(45)

            # Check if we're too far from walls
            if self.too_far_from_walls():
                # Move toward nearest wall
                self.move_to_wall()
            else:
                # Drive along the wall
                self.follow_wall()
            
            await self.go()

    def too_far_from_walls(self):
        """Check if we're too far from any wall"""
        min_distance = min(
            self.x,  # Distance to left wall
            self.arena_width - self.x,  # Distance to right wall
            self.y,  # Distance to top wall
            self.arena_height - self.y  # Distance to bottom wall
        )
        return min_distance > self.wall_distance + 30

    def move_to_wall(self):
        """Move toward the nearest wall"""
        # Find nearest wall
        distances = {
            'left': self.x,
            'right': self.arena_width - self.x,
            'top': self.y,
            'bottom': self.arena_height - self.y
        }

        nearest = min(distances, key=distances.get)

        # Turn toward that wall
        if nearest == 'left':
            self.turn_to(270)  # West
        elif nearest == 'right':
            self.turn_to(90)   # East
        elif nearest == 'top':
            self.turn_to(0)    # North
        else:
            self.turn_to(180)  # South

        self.forward(30)

    def follow_wall(self):
        """Drive along the perimeter"""
        # Move forward along current heading
        self.forward(50)

        # Check if we're getting too close to a wall ahead
        if self.wall_ahead():
            # Turn to follow wall around corner
            self.turn_right(90)

    def wall_ahead(self):
        """Check if there's a wall directly ahead"""
        # Simple check based on heading and position
        margin = 60
        heading = self.direction

        if heading < 45 or heading > 315:
            # Facing up
            return self.y < margin
        elif 45 <= heading < 135:
            # Facing right
            return self.x > (self.arena_width - margin)
        elif 135 <= heading < 225:
            # Facing down
            return self.y > (self.arena_height - margin)
        else:
            # Facing left
            return self.x < margin

    def on_scanned_bot(self, event):
        """
        When we see an enemy - aim and shoot!

        This uses basic aiming toward enemy's current position.
        """
        # Aim gun at enemy (event contains the bearing)
        self.turn_gun_to(self.direction + event.bearing)

        # Shoot based on distance
        if event.distance < 200:
            self.fire(3)
        elif event.distance < 400:
            self.fire(2)
        else:
            self.fire(1)

    def on_hit_by_bullet(self, event):
        """React to being hit"""
        print("Hit! Continuing perimeter patrol...")
        # Keep moving along wall
        self.forward(100)

    def on_hit_wall(self, event):
        """If we hit a wall, turn and continue"""
        print("Bumped into wall!")
        self.back(20)
        self.turn_right(90)

    def turn_to(self, angle):
        """Turn to absolute angle"""
        turn_amount = angle - self.direction
        # Normalize to -180 to 180
        while turn_amount > 180:
            turn_amount -= 360
        while turn_amount < -180:
            turn_amount += 360
        self.turn_right(turn_amount)


# Strengths:
# ✓ Actually moves around the arena
# ✓ Uses walls as protection
# ✓ Has basic aiming
# ✓ Adjusts fire power based on distance
# ✓ Handles wall collisions

# Weaknesses:
# ❌ Predictable movement pattern (follows walls)
# ❌ No prediction of enemy movement
# ❌ Doesn't dodge when hit
# ❌ Can be cornered

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "walls_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = WallsBot(bot_info=bot_info)
    asyncio.run(bot.start())
