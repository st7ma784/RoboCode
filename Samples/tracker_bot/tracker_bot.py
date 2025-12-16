"""
TrackerBot - Follows and hunts enemies

Difficulty: ★★★★☆ (Level 4)

This tank demonstrates:
- Enemy tracking and pursuit
- Distance management
- Predictive aiming
- Tactical positioning
- Energy awareness

Good for:
- Learning pursuit strategies
- Understanding distance control
- Practicing against aggressive opponents
"""

import math
from robocode_tank_royale.bot_api import Bot, BotInfo, Color

class TrackerBot(Bot):
    """Tracks and hunts down enemies with predictive aiming"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set distinctive color - GREEN!
        self.body_color = Color.from_rgb(76, 175, 80)  # Green
        self.turret_color = Color.from_rgb(139, 195, 74)  # Light Green
        self.radar_color = Color.from_rgb(205, 220, 57)  # Lime
        
        # Tracking state
        self.target_x = None
        self.target_y = None
        self.target_heading = None
        self.target_velocity = None
        self.target_distance = None
        
        # Preferred combat distance
        self.optimal_distance = 200
        
        print("🎯 TrackerBot initialized! Hunting mode activated!")

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
        Main loop - hunt the enemy!

        Strategy:
        - Find enemy with radar
        - Move toward them (but not too close)
        - Maintain optimal combat distance
        """
        print("🎯 TrackerBot.run() started!")
        tick = 0
        while self.is_running():
            tick += 1
            if tick % 100 == 0:
                print(f"🎯 TrackerBot tick {tick}, energy: {self.get_energy():.1f}")
            
            # Spin radar to find enemies
            self.radar_turn_rate = 45

            # Boundary checking FIRST (priority over pursuit)
            # Use larger margin to avoid getting stuck
            if self.is_too_close_to_wall(60):
                self.avoid_walls()
            # If we have a target and not near wall, pursue
            elif self.target_x is not None:
                self.pursue_target()
            else:
                # No target yet - search
                self.target_speed = 20
                self.turn_rate = 10

            await self.go()

    def pursue_target(self):
        """Chase after the target we've locked onto - with wall awareness!"""
        if self.target_distance is None:
            return

        # Calculate angle to target
        angle_to_target = self.calculate_angle(
            self.get_x(), self.get_y(),
            self.target_x, self.target_y
        )

        # CRITICAL: Check if close to walls - override pursuit if needed
        if self.is_too_close_to_wall(70):
            # Too close to wall - prioritize escaping over pursuit
            print(f"⚠️ Near wall during pursuit - escaping!")
            center_x = self.get_arena_width() / 2
            center_y = self.get_arena_height() / 2
            angle = self.calculate_angle(self.get_x(), self.get_y(), center_x, center_y)
            self.turn_to(angle)
            self.target_speed = 60
            return

        if self.target_distance > self.optimal_distance + 50:
            # Too far - move closer (but check if path is safe)
            print(f"Closing distance... {self.target_distance:.0f} > {self.optimal_distance}")
            self.turn_to(angle_to_target)
            self.target_speed = 50

        elif self.target_distance < self.optimal_distance - 50:
            # Too close - back away (but check we're not backing into wall)
            print(f"Backing away... {self.target_distance:.0f} < {self.optimal_distance}")
            retreat_angle = angle_to_target + 180

            # Don't back into walls - adjust retreat angle if needed
            if not self.is_direction_safe(retreat_angle):
                # Try perpendicular instead
                retreat_angle = angle_to_target + 90
                if not self.is_direction_safe(retreat_angle):
                    retreat_angle = angle_to_target - 90

            self.turn_to(retreat_angle)
            self.target_speed = 40

        else:
            # Good distance - circle strafe (but avoid walls)
            print(f"Optimal distance! Strafing...")
            strafe_angle = angle_to_target + 90  # Perpendicular

            # Check if strafing toward wall - reverse direction if needed
            if not self.is_direction_safe(strafe_angle):
                strafe_angle = angle_to_target - 90

            self.turn_to(strafe_angle)
            self.target_speed = 30

    async def on_scanned_bot(self, event):
        """
        When we see an enemy - track and attack!

        Uses prediction for better accuracy.
        """
        # Calculate distance from x,y coordinates
        distance_x = self.get_x() - event.x
        distance_y = self.get_y() - event.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        # Update tracking info directly from event
        self.target_x = event.x
        self.target_y = event.y
        self.target_distance = distance
        
        # Estimate velocity and heading from event
        self.target_velocity = event.speed
        self.target_heading = event.direction

        print(f"Target locked: dist={distance:.0f}, vel={event.speed:.1f}")

        # Predict where enemy will be
        future_x, future_y = self.predict_position(event, distance)

        # Aim at predicted position
        aim_angle = self.calculate_angle(self.get_x(), self.get_y(), future_x, future_y)
        self.gun_turn_rate = self.calc_gun_turn(aim_angle)

        # Choose power based on distance and energy
        power = self.choose_fire_power(distance)

        # Fire!
        await self.fire(power)

    def predict_position(self, event, distance):
        """
        Predict where enemy will be when bullet arrives

        Uses simple linear prediction from Week 2
        """
        # Estimate bullet travel time
        bullet_speed = 20 - (3 * 2)  # Assuming power 2
        time_to_hit = distance / bullet_speed

        # Calculate future position
        heading_rad = math.radians(event.direction)
        future_x = event.x + event.speed * time_to_hit * math.sin(heading_rad)
        future_y = event.y + event.speed * time_to_hit * math.cos(heading_rad)

        return future_x, future_y

    def choose_fire_power(self, distance):
        """
        Choose bullet power based on distance and our energy

        Returns: power level (1-3)
        """
        # Energy management
        if self.get_energy() < 20:
            return 1  # Conserve energy

        # Distance-based power
        if distance < 150:
            return 3  # Close range - maximum power
        elif distance < 350:
            return 2  # Medium range
        else:
            return 1  # Long range - fast bullet

    async def on_hit_by_bullet(self, event):
        """React when hit - dodge!"""
        print(f"Hit! Energy: {self.get_energy():.0f} - Dodging!")

        # Emergency dodge
        if self.get_energy() > 30:
            # Aggressive counter
            self.turn_rate = 90
            self.target_speed = 100
        else:
            # Defensive retreat
            self.target_speed = -(80)
            self.turn_rate = 135

    def is_too_close_to_wall(self, margin):
        """Check if near walls (from Week 3)"""
        return (self.get_x() < margin or
                self.get_x()  > self.get_arena_width() - margin or
                self.get_y()  < margin or
                self.get_y()  > self.get_arena_height() - margin)

    def is_direction_safe(self, angle):
        """Check if moving in this direction will lead toward a wall"""
        # Project position 100 pixels in the given direction
        angle_rad = math.radians(angle)
        future_x = self.get_x() + 100 * math.sin(angle_rad)
        future_y = self.get_y() + 100 * math.cos(angle_rad)

        # Check if future position is too close to walls
        margin = 60
        return (future_x > margin and
                future_x < self.get_arena_width() - margin and
                future_y > margin and
                future_y < self.get_arena_height() - margin)

    def avoid_walls(self):
        """Turn away from walls"""
        # If very close, back up first
        if self.is_too_close_to_wall(30):
            self.target_speed = -40
            # Turn toward center while backing up
            center_x = self.get_arena_width() / 2
            center_y = self.get_arena_height() / 2
            angle = self.calculate_angle(self.get_x(), self.get_y(), center_x, center_y)
            self.turn_to(angle)
        else:
            # Turn toward center and move forward
            center_x = self.get_arena_width() / 2
            center_y = self.get_arena_height() / 2
            angle = self.calculate_angle(self.get_x(), self.get_y(), center_x, center_y)
            self.turn_to(angle)
            self.target_speed = 60

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle from one point to another"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))
    
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
# ✓ Actively pursues enemies
# ✓ Maintains optimal combat distance
# ✓ Uses prediction for better aiming
# ✓ Adjusts power based on distance
# ✓ Energy management
# ✓ Wall avoidance
# ✓ Reactive dodging

# Weaknesses:
# ❌ Can be predictable in pursuit
# ❌ Simple linear prediction (doesn't account for direction changes)
# ❌ May get cornered while pursuing
# ❌ Doesn't handle multiple enemies well

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "tracker_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = TrackerBot(bot_info=bot_info)
    asyncio.run(bot.start())
