"""
BoundaryBot - A smart tank that never hits walls!

Week 3 Tutorial - Boundary Checking
This tank checks boundaries before moving and validates targets before shooting.
"""
import math
from robocode_tank_royale.bot_api import Bot, BotInfo

class BoundaryBot(Bot):
    """Demonstrates boundary checking and wall avoidance"""

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
        """Main loop with boundary checking"""
        while self.is_running():
            # Check for walls before moving
            if self.is_too_close_to_wall(50):
                print("⚠️ Wall detected! Avoiding...")
                self.avoid_walls()
            else:
                # Safe to move forward
                self.target_speed = 50
                self.turn_rate = 10

            # Keep radar spinning to find enemies
            self.radar_turn_rate = 45
            
            await self.go()

    def is_too_close_to_wall(self, margin=50):
        """
        Check if we're dangerously close to any wall

        margin: how many pixels from edge is "too close" (default 50)
        Returns: True if too close to any wall, False if safe
        """
        # Check each edge
        too_close_left = self.get_x() < margin
        too_close_right = self.get_x() > (self.get_arena_width() - margin)
        too_close_top = self.get_y() < margin
        too_close_bottom = self.get_y() > (self.get_arena_height() - margin)

        # Return True if ANY edge is too close
        return too_close_left or too_close_right or too_close_top or too_close_bottom

    def find_nearest_wall(self):
        """
        Determine which wall is closest to us

        Returns: "left", "right", "top", or "bottom"
        """
        # Calculate distance to each wall
        distances = {
            "left": self.get_x(),
            "right": self.get_arena_width() - self.get_x(),
            "top": self.get_y(),
            "bottom": self.get_arena_height() - self.get_y()
        }

        # Return the wall with the smallest distance
        return min(distances, key=distances.get)

    def avoid_walls(self):
        """Turn away from the nearest wall and move to safety"""
        nearest = self.find_nearest_wall()

        # Turn to face away from the wall
        if nearest == "left":
            self.turn_to(90)   # Face right (east)
        elif nearest == "right":
            self.turn_to(270)  # Face left (west)
        elif nearest == "top":
            self.turn_to(180)  # Face down (south)
        elif nearest == "bottom":
            self.turn_to(0)    # Face up (north)

        # Move away from danger
        self.target_speed = 100
        print(f"Moved away from {nearest} wall")

    def is_valid_target(self, x, y):
        """
        Check if coordinates are inside the arena

        x, y: coordinates to check
        Returns: True if inside arena, False if outside
        """
        margin = 20  # Safety margin

        # Check X bounds
        x_ok = margin < x < (self.get_arena_width() - margin)
        # Check Y bounds
        y_ok = margin < y < (self.get_arena_height() - margin)

        return x_ok and y_ok

    async def on_scanned_bot(self, event):
        """When we detect an enemy - validate and shoot"""
        # Enemy position is directly from event
        target_x = event.x
        target_y = event.y

        # Validate target is in bounds
        if self.is_valid_target(target_x, target_y):
            # Calculate angle to target
            angle = self.calculate_angle(self.get_x(), self.get_y(), target_x, target_y)

            # Aim and fire
            self.gun_turn_rate = self.calc_gun_turn(angle)
            await self.fire(2)
            print(f"🎯 Firing at valid target at ({target_x:.0f}, {target_y:.0f})")
        else:
            print("❌ Enemy is outside valid range - not shooting")

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """
        Calculate angle from one point to another

        Returns: angle in degrees
        """
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    async def on_hit_wall(self, event):
        """
        Emergency response if we actually hit a wall
        This shouldn't happen if our boundary checking works!
        """
        print("🚨 ERROR: Hit a wall! This shouldn't happen!")
        self.target_speed = -(100)
        self.turn_rate = 135

    async def on_hit_by_bullet(self, event):
        """React when hit by enemy fire"""
        print("💥 Hit! Taking evasive action!")
        # Quick dodge
        self.turn_rate = 90
        self.target_speed = 100

    def turn_to(self, angle):
        """Turn to absolute angle"""
        turn_amount = angle - self.get_direction()
        while turn_amount > 180:
            turn_amount -= 360
        while turn_amount < -180:
            turn_amount += 360
        self.turn_rate = turn_amount


# ============================================
# Testing code
# ============================================
def test_boundary_checking():
    """Test our boundary logic works correctly"""
    print("Running boundary check tests...")

    bot = BoundaryBot()

    # Test 1: Safe position (center)
    bot.x = 400
    bot.y = 300
    assert not bot.is_too_close_to_wall(), "❌ Test 1 failed: Should be safe in center!"
    print("✅ Test 1 passed: Center is safe")

    # Test 2: Near left wall
    bot.x = 30
    bot.y = 300
    assert bot.is_too_close_to_wall(), "❌ Test 2 failed: Should detect left wall!"
    assert bot.find_nearest_wall() == "left", "❌ Test 2 failed: Should identify left wall!"
    print("✅ Test 2 passed: Left wall detected")

    # Test 3: Near top wall
    bot.x = 400
    bot.y = 30
    assert bot.is_too_close_to_wall(), "❌ Test 3 failed: Should detect top wall!"
    assert bot.find_nearest_wall() == "top", "❌ Test 3 failed: Should identify top wall!"
    print("✅ Test 3 passed: Top wall detected")

    # Test 4: Near corner
    bot.x = 30
    bot.y = 30
    assert bot.is_too_close_to_wall(), "❌ Test 4 failed: Should detect corner danger!"
    print("✅ Test 4 passed: Corner danger detected")

    # Test 5: Valid target check
    assert bot.is_valid_target(400, 300), "❌ Test 5 failed: Center should be valid target!"
    assert not bot.is_valid_target(10, 300), "❌ Test 5 failed: Edge should be invalid target!"
    print("✅ Test 5 passed: Target validation works")

    print("\n🎉 All tests passed!")

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "boundary_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = BoundaryBot(bot_info=bot_info)
    asyncio.run(bot.start())
