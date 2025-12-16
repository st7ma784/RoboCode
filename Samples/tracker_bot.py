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
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class TrackerBot(BaseBot):
    """Tracks and hunts down enemies with predictive aiming"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        # Tracking state
        self.target_x = None
        self.target_y = None
        self.target_heading = None
        self.target_velocity = None
        self.target_distance = None

        # Preferred combat distance
        self.optimal_distance = 200

    async def run(self):
        """
        Main loop - hunt the enemy!

        Strategy:
        - Find enemy with radar
        - Move toward them (but not too close)
        - Maintain optimal combat distance
        """
        while True:
            # Spin radar to find enemies
            self.turn_radar_right(45)

            # If we have a target, pursue
            if self.target_x is not None:
                self.pursue_target()
            else:
                # No target yet - search
                self.forward(20)
                self.turn_right(10)

            # Boundary checking
            if self.is_too_close_to_wall(40):
                self.avoid_walls()
            
            await self.go()

    def pursue_target(self):
        """Chase after the target we've locked onto"""
        if self.target_distance is None:
            return

        # Calculate angle to target
        angle_to_target = self.calculate_angle(
            self.x, self.y,
            self.target_x, self.target_y
        )

        if self.target_distance > self.optimal_distance + 50:
            # Too far - move closer
            print(f"Closing distance... {self.target_distance:.0f} > {self.optimal_distance}")
            self.turn_to(angle_to_target)
            self.forward(50)

        elif self.target_distance < self.optimal_distance - 50:
            # Too close - back away
            print(f"Backing away... {self.target_distance:.0f} < {self.optimal_distance}")
            self.turn_to(angle_to_target + 180)  # Turn away
            self.forward(40)

        else:
            # Good distance - circle strafe
            print(f"Optimal distance! Strafing...")
            self.turn_to(angle_to_target + 90)  # Perpendicular
            self.forward(30)

    def on_scanned_bot(self, event):
        """
        When we see an enemy - track and attack!

        Uses prediction for better accuracy.
        """
        # Update tracking info from bearing and distance
        bearing_rad = math.radians(event.bearing)
        self.target_x = self.x + event.distance * math.sin(bearing_rad)
        self.target_y = self.y + event.distance * math.cos(bearing_rad)
        self.target_distance = event.distance
        
        # Estimate velocity and heading from event
        self.target_velocity = event.speed
        self.target_heading = event.direction

        print(f"Target locked: dist={event.distance:.0f}, "
              f"vel={event.speed:.1f}")

        # Predict where enemy will be
        future_x, future_y = self.predict_position(event)

        # Aim at predicted position
        aim_angle = self.calculate_angle(self.x, self.y, future_x, future_y)
        self.turn_gun_to(aim_angle)

        # Choose power based on distance and energy
        power = self.choose_fire_power(event.distance)

        # Fire!
        self.fire(power)

    def predict_position(self, event):
        """
        Predict where enemy will be when bullet arrives

        Uses simple linear prediction from Week 2
        """
        # Estimate bullet travel time
        bullet_speed = 20 - (3 * 2)  # Assuming power 2
        time_to_hit = event.distance / bullet_speed

        # Calculate future position
        heading_rad = math.radians(event.direction)
        future_x = self.target_x + event.speed * time_to_hit * math.sin(heading_rad)
        future_y = self.target_y + event.speed * time_to_hit * math.cos(heading_rad)

        return future_x, future_y

    def choose_fire_power(self, distance):
        """
        Choose bullet power based on distance and our energy

        Returns: power level (1-3)
        """
        # Energy management
        if self.energy < 20:
            return 1  # Conserve energy

        # Distance-based power
        if distance < 150:
            return 3  # Close range - maximum power
        elif distance < 350:
            return 2  # Medium range
        else:
            return 1  # Long range - fast bullet

    def on_hit_by_bullet(self, event):
        """React when hit - dodge!"""
        print(f"Hit! Energy: {self.energy:.0f} - Dodging!")

        # Emergency dodge
        if self.energy > 30:
            # Aggressive counter
            self.turn_right(90)
            self.forward(100)
        else:
            # Defensive retreat
            self.back(80)
            self.turn_right(135)

    def is_too_close_to_wall(self, margin):
        """Check if near walls (from Week 3)"""
        return (self.x < margin or
                self.x > self.arena_width - margin or
                self.y < margin or
                self.y > self.arena_height - margin)

    def avoid_walls(self):
        """Turn away from walls"""
        # Simple avoidance: turn toward center
        center_x = self.arena_width / 2
        center_y = self.arena_height / 2
        angle = self.calculate_angle(self.x, self.y, center_x, center_y)
        self.turn_to(angle)
        self.forward(60)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle from one point to another"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))
    
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
