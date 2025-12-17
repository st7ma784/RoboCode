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
from robocode_tank_royale.bot_api import Bot, BotInfo, Color

class WallsBot(Bot):
    """Patrols the perimeter of the arena"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set independence flags - gun and radar move independently
        self.set_adjust_gun_for_body_turn(True)
        self.set_adjust_radar_for_body_turn(True)
        self.set_adjust_radar_for_gun_turn(True)
        
        # Set distinctive color - BLUE!
        self.body_color = Color.from_rgb(33, 150, 243)  # Blue
        self.turret_color = Color.from_rgb(3, 169, 244)  # Light Blue
        self.radar_color = Color.from_rgb(0, 188, 212)  # Cyan
        
        # How close to walls we want to stay
        self.wall_distance = 50
        

    def calc_gun_turn(self, target_angle):
        """Calculate gun turn needed to face target angle"""
        diff = target_angle - self.get_gun_direction()
        # Normalize to -180 to 180
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        return diff

    async def run(self):
        """
        Main loop - drive along the walls!

        Strategy: Stay near the perimeter of the arena.
        This gives us walls at our back (fewer angles to defend).
        """
        while self.is_running():
          
            # Keep radar spinning
            self.radar_turn_rate = 45

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
            self.get_x(),  # Distance to left wall
            self.get_arena_width() - self.get_x(),  # Distance to right wall
            self.get_y(),  # Distance to top wall
            self.get_arena_height() - self.get_y()  # Distance to bottom wall
        )
        return min_distance > self.wall_distance + 30

    def move_to_wall(self):
        """Move toward the nearest wall"""
        # Find nearest wall
        distances = {
            'left': self.get_x(),
            'right': self.get_arena_width() - self.get_x(),
            'top': self.get_y(),
            'bottom': self.get_arena_height() - self.get_y()
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

        self.target_speed = 30

    def follow_wall(self):
        """Drive along the perimeter"""
        # Move forward along current heading
        self.target_speed = 50

        # Check if we're getting too close to a wall ahead
        if self.wall_ahead():
            # Turn to follow wall around corner
            self.turn_rate = 90

    def wall_ahead(self):
        """Check if there's a wall directly ahead"""
        # Simple check based on heading and position
        margin = 60
        heading = self.get_direction()

        if heading < 45 or heading > 315:
            # Facing up
            return self.get_y() < margin
        elif 45 <= heading < 135:
            # Facing right
            return self.get_x() > (self.get_arena_width() - margin)
        elif 135 <= heading < 225:
            # Facing down
            return self.get_y() > (self.get_arena_height() - margin)
        else:
            # Facing left
            return self.get_x() < margin

    async def on_scanned_bot(self, event):
        """
        When we see an enemy - aim and shoot!

        This uses basic aiming toward enemy's current position.
        """
        # Calculate distance from x,y coordinates
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)
        
        # Calculate bearing (angle to enemy)
        bearing = math.degrees(math.atan2(dx, dy))
        
        # Aim gun at enemy
        self.gun_turn_rate = self.calc_gun_turn(self.get_direction() + bearing)

        # Shoot based on distance
        if distance < 200:
            await self.fire(3)
        elif distance < 400:
            await self.fire(2)
        else:
            await self.fire(1)

    async def on_hit_by_bullet(self, event):
        """React to being hit"""
        # Keep moving along wall
        self.target_speed = 100

    async def on_hit_wall(self, event):
        """If we hit a wall, turn and continue"""
        self.target_speed = -(20)
        self.turn_rate = 90

    def turn_to(self, angle):
        """Turn to absolute angle"""
        turn_amount = angle - self.get_direction()
        # Normalize to -180 to 180
        while turn_amount > 180:
            turn_amount -= 360
        while turn_amount < -180:
            turn_amount += 360
        self.turn_rate = turn_amount


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
