"""
TricksterBot - A tank that's impossible to predict!

Week 4 Tutorial - Strategy and Unpredictable Movement
This tank changes movement patterns randomly and reacts differently to events.
"""
import random
import math
from robocode_tank_royale.bot_api import Bot, BotInfo

class TricksterBot(Bot):
    """Uses unpredictable movement patterns to avoid being hit"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        # Time tracking
        self.time = 0


    def calc_gun_turn(self, target_angle):
        """Calculate gun turn needed to face target angle"""
        diff = target_angle - self.get_gun_direction()
        # Normalize to -180 to 180
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        return diff

        # Strategy state
        self.current_pattern = "random_walk"
        self.pattern_change_countdown = 50  # Change pattern every 50 ticks

    async def run(self):
        """Main loop with changing strategies"""
        while self.is_running():
            self.time += 1

            # Time to change patterns?
            if self.pattern_change_countdown <= 0:
                old_pattern = self.current_pattern
                self.current_pattern = random.choice([
                    "zigzag",
                    "spiral",
                    "random_walk",
                    "stop_and_go"
                ])
                # Don't repeat the same pattern
                while self.current_pattern == old_pattern:
                    self.current_pattern = random.choice([
                        "zigzag",
                    "spiral",
                    "random_walk",
                    "stop_and_go"
                ])

            self.pattern_change_countdown = random.randint(40, 70)  # Random duration
            print(f"🔄 Switching to {self.current_pattern} pattern!")

            # Execute current pattern
            if self.current_pattern == "zigzag":
                self.zigzag_movement()
            elif self.current_pattern == "spiral":
                self.spiral_movement()
            elif self.current_pattern == "random_walk":
                self.random_walk()
            elif self.current_pattern == "stop_and_go":
                self.stop_and_go()

            self.pattern_change_countdown -= 1

            # Keep radar spinning independently
            self.radar_turn_rate = 45
            
            await self.go()

    def zigzag_movement(self):
        """Move in a zigzag pattern"""
        self.target_speed = 80

        # Random zigzag
        if random.random() < 0.5:
            self.turn_rate = random.randint(25, 35)
        else:
            self.turn_rate = -(random.randint(25, 35))

    def spiral_movement(self):
        """Spiral outward from current position"""
        # Distance increases over time
        distance = 20 + (self.time % 80)
        self.target_speed = distance
        self.turn_rate = 25

    def random_walk(self):
        """Random but smooth movement"""
        # Random distance
        distance = random.randint(40, 100)
        self.target_speed = distance

        # Small random turns for smooth movement
        angle = random.randint(-25, 25)
        if angle < 0:
            self.turn_rate = -(abs(angle))
        else:
            self.turn_rate = angle

    def stop_and_go(self):
        """Unpredictable stops and starts"""
        if random.random() < 0.25:
            # 25% chance to stop and turn
            print("🛑 Sudden stop!")
            self.turn_rate = random.randint(60, 180)
        else:
            # Keep moving
            self.target_speed = 60
            self.turn_rate = 12

    async def on_scanned_bot(self, event):
        """Adaptive tactics based on distance and situation"""
        # Enemy position is directly from event
        enemy_x = event.x
        enemy_y = event.y
        
        # Calculate distance from coordinates
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)

        # Calculate aim angle
        angle = self.calculate_angle(self.get_x(), self.get_y(), enemy_x, enemy_y)

        # Choose tactics based on range
        if distance < 150:
            # CLOSE COMBAT - Be aggressive!
            print("⚔️ CLOSE COMBAT MODE!")
            self.gun_turn_rate = self.calc_gun_turn(angle)
            await self.fire(3)  # Maximum power

            # Charge forward (risky but aggressive)
            if self.get_energy() > 50:
                self.target_speed = 30
            else:
                # Low energy - retreat!
                self.target_speed = -(30)

        elif distance < 350:
            # MEDIUM RANGE - Tactical approach
            print("🎯 TACTICAL MODE")
            self.gun_turn_rate = self.calc_gun_turn(angle)
            await self.fire(2)  # Medium power

            # Strafe (move sideways) to dodge
            if random.random() < 0.5:
                self.turn_rate = 90
            else:
                self.turn_rate = -(90)
            self.target_speed = 40

        else:
            # LONG RANGE - Sniper mode
            print("🔭 SNIPER MODE")
            self.gun_turn_rate = self.calc_gun_turn(angle)
            await self.fire(1)  # Low power = faster bullet

            # Maintain distance
            if random.random() < 0.3:
                self.target_speed = -(40)

    async def on_hit_by_bullet(self, event):
        """React unpredictably when hit"""
        print(f"💥 HIT! Energy: {self.get_energy()}")

        # Choose random reaction (1-5)
        reaction = random.randint(1, 5)

        if reaction == 1:
            # Quick forward dodge
            print("  → Quick dodge forward!")
            self.target_speed = 100

        elif reaction == 2:
            # Sharp turn and retreat
            print("  → Retreat!")
            self.turn_rate = 135
            self.target_speed = -(80)

        elif reaction == 3:
            # Aggressive counter-attack
            print("  → Counter-attack!")
            self.turn_rate = -(90)
            self.target_speed = 120

        elif reaction == 4:
            # Spin move (confuse enemy)
            print("  → Spin move!")
            self.turn_rate = random.randint(120, 240)
            self.target_speed = 60

        else:
            # Stop and shoot back
            print("  → Shoot back!")
            # Turn gun toward where bullet came from
            self.gun_turn_rate = self.calc_gun_turn(self.get_direction() + event.bullet_bearing)
            await self.fire(3)

        # Force immediate pattern change after being hit
        self.pattern_change_countdown = 0

    async def on_hit_wall(self, event):
        """Tactical wall bounce"""
        print("🧱 Wall collision! Bouncing off...")

        # Back away from wall
        self.target_speed = -(60)

        # Random escape angle
        angle = random.choice([60, 90, 120, 150])
        if random.random() < 0.5:
            self.turn_rate = angle
        else:
            self.turn_rate = -(angle)

        # Burst forward
        self.target_speed = 80

        # Change pattern after wall hit
        self.pattern_change_countdown = 0

    def on_death(self, event):
        """Called when bot dies"""
        print("💀 Defeated!")

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """
        Calculate angle from one point to another

        Returns: angle in degrees
        """
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "trickster_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = TricksterBot(bot_info=bot_info)
    asyncio.run(bot.start())
