"""
Property API Demonstration Bot
===============================

This bot demonstrates WHY we use property API instead of method API.

Run this bot and watch it work perfectly using property API!
Then look at the commented-out "wrong way" to see why method API fails.

Difficulty: ★☆☆☆☆ (Tutorial)
Focus: Understanding the Property API pattern
"""

from robocode_tank_royale.bot_api import Bot, BotInfo, Color
import math


class PropertyAPIDemo(Bot):
    """
    A simple bot that demonstrates correct property API usage.

    This bot will:
    - Move forward while scanning
    - Turn in a circle
    - Aim gun and radar independently
    - Fire at enemies

    All using the PROPERTY API!
    """

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)

        # CRITICAL: Enable independence so gun/radar can move separately from body
        self.set_adjust_gun_for_body_turn(True)
        self.set_adjust_radar_for_body_turn(True)
        self.set_adjust_radar_for_gun_turn(True)

        # Set a friendly color
        self.body_color = Color.from_rgb(50, 150, 255)  # Blue
        self.turret_color = Color.from_rgb(255, 200, 50)  # Gold
        self.radar_color = Color.from_rgb(50, 255, 150)  # Green

        print("📚 Property API Demo Bot Starting!")
        print("Watch me move, scan, and shoot - all using property API!")

    async def run(self):
        """
        Main loop - demonstrates the CORRECT way to control your tank
        """
        print("\n✅ USING PROPERTY API (THE CORRECT WAY)")
        print("=" * 50)

        tick = 0
        while self.is_running():
            tick += 1

            # Print status every 50 ticks
            if tick % 50 == 0:
                print(f"✓ Tick {tick}: Moving at {self.get_speed():.1f} speed, "
                      f"direction {self.get_direction():.0f}°")

            # ═══════════════════════════════════════════════════════
            # STEP 1: CALCULATE what you want to do
            # ═══════════════════════════════════════════════════════
            # This is your "thinking" phase - do all calculations here!

            # Circle movement calculation
            desired_speed = 50
            desired_turn = 15  # Turn right slowly (makes a circle)

            # Radar sweep calculation
            radar_sweep = 45  # Always sweep right

            # ═══════════════════════════════════════════════════════
            # STEP 2: SET properties (no await needed!)
            # ═══════════════════════════════════════════════════════
            # This is your "planning" phase - set what you want to happen

            self.target_speed = desired_speed      # Body will move forward
            self.turn_rate = desired_turn          # Body will turn right
            self.radar_turn_rate = radar_sweep     # Radar sweeps independently

            # NOTE: We haven't used 'await' yet, but we've planned everything!
            # The tank hasn't moved yet - we're still in "planning mode"

            # ═══════════════════════════════════════════════════════
            # STEP 3: EXECUTE everything together with ONE await!
            # ═══════════════════════════════════════════════════════

            await self.go()  # ← Magic happens here! All commands execute!

            # After this line:
            # - Body moved forward at speed 50
            # - Body turned right 15 degrees
            # - Radar swept right 45 degrees
            # ALL AT THE SAME TIME! ✨

    async def on_scanned_bot(self, event):
        """
        When we spot an enemy - demonstrate independent gun control
        """
        print(f"👁️  Spotted enemy at ({event.x:.0f}, {event.y:.0f})")

        # ═══════════════════════════════════════════════════════
        # STEP 1: CALCULATE where to aim
        # ═══════════════════════════════════════════════════════

        # Calculate angle to enemy
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        angle_to_enemy = math.degrees(math.atan2(dx, dy))

        # Calculate how much to turn gun
        gun_turn_needed = angle_to_enemy - self.get_gun_direction()

        # Normalize angle to -180 to 180
        while gun_turn_needed > 180:
            gun_turn_needed -= 360
        while gun_turn_needed < -180:
            gun_turn_needed += 360

        # ═══════════════════════════════════════════════════════
        # STEP 2: SET gun property (independent of body!)
        # ═══════════════════════════════════════════════════════

        self.gun_turn_rate = gun_turn_needed

        # Notice: We didn't use await yet!
        # The gun will turn when we call await self.go() in the main loop

        # ═══════════════════════════════════════════════════════
        # STEP 3: Fire if gun is aimed (separate await)
        # ═══════════════════════════════════════════════════════

        if abs(gun_turn_needed) < 10:  # Gun is roughly aimed
            distance = math.sqrt(dx**2 + dy**2)

            # Choose power based on distance
            if distance < 200:
                power = 3
            elif distance < 400:
                power = 2
            else:
                power = 1

            print(f"💥 Firing at enemy! Distance: {distance:.0f}, Power: {power}")
            await self.fire(power)  # Fire needs separate await!

    async def on_hit_by_bullet(self, event):
        """React to being hit"""
        print(f"😵 Ouch! Hit by bullet with power {event.bullet.power}")

        # Emergency dodge - just set properties!
        self.turn_rate = 90  # Turn hard right
        self.target_speed = -50  # Reverse!
        # These will execute on the next await self.go() in main loop

    async def on_win(self, event):
        """Victory!"""
        print("\n🏆 Property API Demo Bot WINS!")
        print("See how clean and simple the code is? That's the power of property API!")


# ═══════════════════════════════════════════════════════════════════════
# COMPARISON: The WRONG way (commented out so bot works)
# ═══════════════════════════════════════════════════════════════════════

"""
Here's what the WRONG way would look like:

async def run_the_wrong_way(self):
    # ❌ WRONG - Using method API
    while self.is_running():
        # Problem 1: These create coroutines but don't execute!
        self.forward(50)          # Creates coroutine, does nothing! 😱
        self.turn_right(15)       # Creates coroutine, does nothing! 😱
        self.turn_radar_right(45) # Creates coroutine, does nothing! 😱

        await self.go()  # Tank is still stationary!

        # The tank would just sit there doing nothing!
        # Python would warn: "RuntimeWarning: coroutine was never awaited"

    # To make method API work, you'd need:
    # ❌ MESSY - Await every single command
    while self.is_running():
        await self.forward(50)          # Wait...
        await self.turn_right(15)       # Wait...
        await self.turn_radar_right(45) # Wait...
        await self.go()                 # Wait...

        # Problem 2: Too many awaits! Slow and messy!
        # Problem 3: Gun/radar might not sync with body movement!
        # Problem 4: Hard to organize code into helper functions

# ═══════════════════════════════════════════════════════════════════════
# WHY PROPERTY API IS BETTER:
# ═══════════════════════════════════════════════════════════════════════

# 1. ✅ Clean code - one await instead of many
# 2. ✅ Fast execution - all commands happen together
# 3. ✅ Easy to organize - helper functions don't need async
# 4. ✅ Perfect sync - gun/radar/body move together
# 5. ✅ Flexible - can override properties before await self.go()

# Example of clean organization with property API:

def calculate_escape_route(self):
    '''Helper function - NO async needed!'''
    angle = some_calculation()
    self.turn_rate = angle        # Just set property
    self.target_speed = 80        # Just set property
    # Caller will do await self.go()

async def run(self):
    while self.is_running():
        self.calculate_escape_route()  # No await needed!
        self.scan_for_enemies()        # No await needed!
        self.aim_at_target()           # No await needed!

        await self.go()  # Execute everything together!

# Beautiful! Clean! Easy to read and maintain! ✨
"""

# ═══════════════════════════════════════════════════════════════════════
# LEARNING EXERCISE
# ═══════════════════════════════════════════════════════════════════════

"""
Try these exercises to master property API:

1. BASIC: Modify the bot to move in a square pattern instead of a circle
   Hint: Use different turn_rate values (0, 90, 180, 270)

2. INTERMEDIATE: Add wall avoidance using property API
   Hint: Check distance to walls, set turn_rate to turn away

3. ADVANCED: Make the radar lock onto enemies instead of sweeping
   Hint: Calculate angle to enemy, set radar_turn_rate to that angle

4. EXPERT: Add anti-gravity movement (move away from enemies)
   Hint: Calculate repulsion force, convert to angle and speed properties

Remember: Always think in three steps:
1. CALCULATE (math and logic)
2. SET (properties)
3. EXECUTE (await self.go())
"""


if __name__ == "__main__":
    import asyncio
    from pathlib import Path

    # Create bot info
    bot_info = BotInfo(
        name="PropertyAPIDemo",
        version="1.0",
        authors=["Tutorial"],
        description="Demonstrates why property API is better than method API",
        country_code="US",
        game_types=["classic", "melee"]
    )

    # Create and start the bot
    print("\n" + "="*60)
    print("  PROPERTY API DEMONSTRATION BOT")
    print("="*60)
    print("\nThis bot shows you THE CORRECT WAY to control your tank!")
    print("\nWatch the console output to see what's happening.")
    print("Read the code to understand WHY property API is better.\n")

    bot = PropertyAPIDemo(bot_info=bot_info)
    asyncio.run(bot.start())
