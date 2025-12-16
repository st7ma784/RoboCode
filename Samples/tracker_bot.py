"""
TrackerBot - Relentless Ramming Hunter

Difficulty: 4/5 stars (Level 4)

This tank demonstrates:
- Aggressive ramming strategy
- Always targets nearest enemy
- Switches targets dynamically
- Full-speed pursuit
- Close-range combat

Good for:
- Learning aggressive tactics
- Understanding pursuit strategies
- Practicing ramming techniques
"""

import math
from robocode_tank_royale.bot_api import Bot, BotInfo

class TrackerBot(Bot):
    """Tracks and hunts down enemies with predictive aiming"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        # Tracking state - always pursue nearest
        self.target_x = None
        self.target_y = None
        self.target_heading = None
        self.target_velocity = None
        self.target_distance = None

    async def run(self):
        """
        Main loop - RAM THE ENEMY!

        Strategy:
        - Find nearest enemy with radar
        - Charge directly at them at full speed
        - Switch to closer targets if found
        - No mercy, full ramming mode!
        """
        while True:
            # Spin radar to find enemies
            self.turn_radar_right(45)

            # Boundary checking FIRST
            if self.is_too_close_to_wall(50):
                self.avoid_walls()
            elif self.target_x is not None:
                # If we have a target and not near wall, RAM IT!
                self.ram_target()
            else:
                # No target yet - search aggressively
                self.forward(50)
                self.turn_right(15)
            
            await self.go()

    def ram_target(self):
        """RAM THE TARGET! Full speed ahead!"""
        if self.target_distance is None:
            return

        # Calculate angle to target
        angle_to_target = self.calculate_angle(
            self.x, self.y,
            self.target_x, self.target_y
        )

        # ALWAYS charge directly at target!
        print(f"🎯 RAMMING TARGET! Distance: {self.target_distance:.0f}")
        self.turn_to(angle_to_target)
        
        # Maximum speed ramming!
        if self.target_distance > 50:
            self.forward(100)  # Full speed!
        else:
            # Close range - keep the pressure on
            self.forward(80)

    def on_scanned_bot(self, event):
        """
        When we see an enemy - switch to it if it's closer!
        Always pursue the NEAREST target.
        """
        # Calculate enemy position from bearing and distance
        bearing_rad = math.radians(event.bearing)
        scanned_x = self.x + event.distance * math.sin(bearing_rad)
        scanned_y = self.y + event.distance * math.cos(bearing_rad)
        
        # Always switch to this target if it's closer (or we have no target)
        if self.target_distance is None or event.distance < self.target_distance:
            if self.target_distance is not None:
                print(f"⚡ SWITCHING to closer target! {event.distance:.0f} < {self.target_distance:.0f}")
            
            # Lock onto this closer target
            self.target_x = scanned_x
            self.target_y = scanned_y
            self.target_distance = event.distance
            self.target_velocity = event.speed
            self.target_heading = event.direction
            
            print(f"🎯 NEAREST target locked: dist={event.distance:.0f}")

        # Aim gun at target (current position for ramming - we're getting close fast!)
        aim_angle = self.calculate_angle(self.x, self.y, scanned_x, scanned_y)
        self.turn_gun_to(aim_angle)

        # Fire while ramming - maximum power at close range!
        if event.distance < 150:
            self.fire(3)  # Maximum power when close!
        elif event.distance < 300:
            self.fire(2)



    def on_hit_by_bullet(self, event):
        """React when hit - COUNTER ATTACK!"""
        print(f"💥 Hit! Energy: {self.energy:.0f} - Charging harder!")

        # Quick jink but keep charging
        if self.energy > 20:
            # Quick dodge but maintain aggression
            self.turn_right(45)
        else:
            # Low energy - bigger dodge
            self.turn_right(90)

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
        self.forward(70)

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
    
    def turn_gun_to(self, angle):
        """Turn gun to absolute angle"""
        gun_turn_amount = angle - self.gun_direction
        # Normalize to -180 to 180
        while gun_turn_amount > 180:
            gun_turn_amount -= 360
        while gun_turn_amount < -180:
            gun_turn_amount += 360
        self.gun_turn_rate = gun_turn_amount


# Strengths:
# ✓ Always pursues nearest target
# ✓ Switches targets dynamically
# ✓ Extremely aggressive ramming
# ✓ Maximum power at close range
# ✓ Full-speed charging
# ✓ Wall avoidance
# ✓ Never backs down

# Weaknesses:
# ❌ Very predictable movement (straight line)
# ❌ Vulnerable to skilled opponents
# ❌ May take heavy damage from ramming
# ❌ No energy conservation

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
