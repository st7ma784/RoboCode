"""
Rambo - The Perimeter Sharpshooter

Strategy:
Instead of aiming the gun and then choosing power, Rambo does the opposite:
- Patrols around the arena walls
- Keeps the gun pointing inward with minimal movement
- Calculates when enemies will cross the current firing line
- Varies bullet power so the bullet arrives exactly when the enemy crosses

This innovative approach means Rambo fires with precision timing rather than
precision aiming, making it deadly at intercepting crossing targets.
"""

from robocode_tank_royale.bot_api import Bot, BotInfo, Color
import math
import sys
import os

# Add parent directory to path to import tank_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tank_utils import TankMath, TankMovement


class Rambo(Bot):
    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)

        # Rambo's signature colors (camo green)
        self.body_color = Color.from_rgb(85, 107, 47)      # Dark olive green
        self.turret_color = Color.from_rgb(107, 142, 35)   # Olive drab
        self.radar_color = Color.from_rgb(154, 205, 50)    # Yellow green

        # Movement state
        self.wall_margin = 80
        self.move_direction = 1  # 1 for forward, -1 for backward
        self.current_wall = None

        # Gun control - sweep slowly inward
        self.gun_sweep_direction = 1
        self.gun_base_angle = 0  # Points toward center

    async def run(self):
        """Main game loop"""
        while self.is_running():
            # Wall-following movement
            self.follow_walls()

            # Keep gun pointing generally inward with slight sweep
            self.aim_inward()

            # Radar sweeps constantly
            self.radar_turn_rate = 45

            await self.go()

    def follow_walls(self):
        """Move along the perimeter of the arena"""
        arena_width = self.get_arena_width()
        arena_height = self.get_arena_height()
        x = self.get_x()
        y = self.get_y()

        # Determine which wall we're near
        dist_left = x
        dist_right = arena_width - x
        dist_top = arena_height - y
        dist_bottom = y

        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        # Target speed along wall
        self.target_speed = 50 * self.move_direction

        # Determine direction to follow wall
        if min_dist == dist_left:
            # Near left wall, head up or down
            self.current_wall = "left"
            if y < self.wall_margin:
                target_heading = 0  # North
            elif y > arena_height - self.wall_margin:
                target_heading = 180  # South
            else:
                target_heading = 0 if self.move_direction > 0 else 180

        elif min_dist == dist_right:
            # Near right wall, head up or down
            self.current_wall = "right"
            if y < self.wall_margin:
                target_heading = 0  # North
            elif y > arena_height - self.wall_margin:
                target_heading = 180  # South
            else:
                target_heading = 0 if self.move_direction > 0 else 180

        elif min_dist == dist_top:
            # Near top wall, head left or right
            self.current_wall = "top"
            if x < self.wall_margin:
                target_heading = 90  # East
            elif x > arena_width - self.wall_margin:
                target_heading = 270  # West
            else:
                target_heading = 90 if self.move_direction > 0 else 270

        else:
            # Near bottom wall, head left or right
            self.current_wall = "bottom"
            if x < self.wall_margin:
                target_heading = 90  # East
            elif x > arena_width - self.wall_margin:
                target_heading = 270  # West
            else:
                target_heading = 90 if self.move_direction > 0 else 270

        # Turn toward target heading
        current_heading = self.get_direction()
        turn_needed = TankMath.normalize_angle(target_heading - current_heading)
        self.turn_rate = max(-10, min(10, turn_needed))

    def aim_inward(self):
        """Keep gun pointing toward arena center with minimal movement"""
        arena_width = self.get_arena_width()
        arena_height = self.get_arena_height()
        center_x = arena_width / 2
        center_y = arena_height / 2

        # Calculate angle to center
        angle_to_center = TankMath.calculate_angle(
            self.get_x(), self.get_y(),
            center_x, center_y
        )

        # Add small sweep (+/- 15 degrees)
        self.gun_base_angle = angle_to_center
        sweep_offset = 15 * math.sin(self.get_tick_count() * 0.05)
        target_gun_angle = angle_to_center + sweep_offset

        # Minimal gun adjustment
        current_gun = self.get_gun_direction()
        turn_needed = TankMath.normalize_angle(target_gun_angle - current_gun)
        self.gun_turn_rate = max(-5, min(5, turn_needed))  # Slow, minimal turns

    async def on_scanned_bot(self, event):
        """
        When enemy detected, calculate trajectory intersection and fire with
        appropriate power to intercept
        """
        # Get bot state
        bx, by = self.get_x(), self.get_y()
        gun_dir = self.get_gun_direction()

        # Get enemy state
        ex, ey = event.x, event.y
        enemy_speed = event.speed
        enemy_dir = event.direction

        # Calculate trajectory intersection
        power = self.calculate_intercept_power(
            bx, by, gun_dir,
            ex, ey, enemy_speed, enemy_dir
        )

        if power is not None and 0.1 <= power <= 3.0:
            # Valid power, fire!
            await self.fire(power)

    def calculate_intercept_power(self, bx, by, gun_dir, ex, ey, enemy_speed, enemy_dir):
        """
        Calculate the power needed for a bullet to intercept an enemy
        crossing our firing line.

        Returns:
            float: Power (0.1-3.0) or None if no valid intersection
        """
        # Convert angles to radians
        gun_rad = math.radians(gun_dir)
        enemy_rad = math.radians(enemy_dir)

        # Gun direction unit vector
        gun_dx = math.sin(gun_rad)
        gun_dy = math.cos(gun_rad)

        # Enemy direction unit vector (scaled by speed)
        enemy_dx = math.sin(enemy_rad)
        enemy_dy = math.cos(enemy_rad)

        # Solve for ray intersection
        # Gun ray: P = (bx, by) + t1 * (gun_dx, gun_dy)
        # Enemy ray: Q = (ex, ey) + t2 * enemy_speed * (enemy_dx, enemy_dy)

        # System of equations:
        # bx + t1*gun_dx = ex + t2*enemy_speed*enemy_dx
        # by + t1*gun_dy = ey + t2*enemy_speed*enemy_dy

        # Matrix form: [gun_dx, -enemy_speed*enemy_dx] [t1]   [ex - bx]
        #              [gun_dy, -enemy_speed*enemy_dy] [t2] = [ey - by]

        # Calculate determinant
        det = gun_dx * (-enemy_speed * enemy_dy) - (-enemy_speed * enemy_dx) * gun_dy
        det = -enemy_speed * (gun_dx * enemy_dy - gun_dy * enemy_dx)

        # Check if lines are parallel (det ≈ 0)
        if abs(det) < 0.001:
            return None

        # Solve using Cramer's rule
        dx_diff = ex - bx
        dy_diff = ey - by

        t1 = (dx_diff * (-enemy_speed * enemy_dy) - (-enemy_speed * enemy_dx) * dy_diff) / det
        t2 = (gun_dx * dy_diff - gun_dy * dx_diff) / det

        # Both t values must be positive (intersection in the future)
        if t1 <= 0 or t2 <= 0:
            return None

        # t1 is the distance the bullet must travel
        # t2 is the time until enemy reaches intersection (in ticks)
        bullet_distance = t1
        time_to_intersection = t2

        # Required bullet speed
        required_speed = bullet_distance / time_to_intersection

        # Calculate power from bullet speed
        # bullet_speed = 20 - 3 * power
        # power = (20 - bullet_speed) / 3
        power = (20 - required_speed) / 3

        # Validate power range
        if power < 0.1:
            # Bullet too slow even at minimum power, enemy too fast
            return None
        elif power > 3.0:
            # Need more power than possible, use max
            power = 3.0

        # Additional validation: check if intersection is reasonable
        # Don't shoot if intersection is too far (likely to miss)
        if bullet_distance > 800:
            return None

        # Don't shoot if enemy is moving very slowly (stationary targets)
        # For stationary targets, traditional aiming is better
        if enemy_speed < 2:
            return None

        return power

    async def on_hit_wall(self, event):
        """Reverse direction when hitting wall"""
        self.move_direction *= -1
        self.target_speed = 50 * self.move_direction

    async def on_hit_by_bullet(self, event):
        """React to being hit by adjusting movement"""
        # Quick dodge by reversing
        self.move_direction *= -1



if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "rambo.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = Rambo(bot_info=bot_info)
    asyncio.run(bot.start())
