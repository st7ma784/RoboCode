"""
StalkerBot - Patient sniper that kites and waits for predictable targets

Difficulty: ★★★★☆ (Level 4)

This tank demonstrates:
- Target tracking across multiple scans
- Linear movement detection
- Distance management (kiting)
- Selective firing based on predictability
- Advanced wall avoidance while maneuvering

Good for:
- Learning pattern recognition
- Understanding kiting mechanics
- Practicing patience over aggression
- Advanced distance control
"""

import math
from collections import deque
from robocode_tank_royale.bot_api import Bot, BotInfo, Color


class StalkerBot(Bot):
    """Patient sniper that kites enemies and only fires at predictable targets"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)

        # Set distinctive color - DARK BLUE (stealthy)
        self.body_color = Color.from_rgb(63, 81, 181)  # Indigo
        self.turret_color = Color.from_rgb(48, 63, 159)  # Dark Indigo
        self.radar_color = Color.from_rgb(92, 107, 192)  # Light Indigo

        # Target tracking
        self.target_id = None
        self.target_x = None
        self.target_y = None
        self.target_speed = 0
        self.target_direction = None

        # Movement history for linearity detection
        self.target_history = deque(maxlen=5)  # Last 5 positions

        # Kiting parameters
        self.optimal_distance = 350  # Sniping range
        self.min_distance = 250      # Too close
        self.max_distance = 500      # Too far

        # Linearity detection
        self.consecutive_linear_scans = 0
        self.linear_threshold = 3  # Need 3 consecutive linear scans to fire


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
        Main loop - stalk, kite, and snipe!

        Strategy:
        - Find and lock onto a target
        - Maintain optimal sniping distance
        - Track enemy movement patterns
        - Only fire when enemy is predictable
        """
        # print("👻 StalkerBot.run() started!")
        while self.is_running():
            # print(f"👻 Stalking... tick {tick}, energy: {self.get_energy():.1f}, target: {self.target_x is not None}")

            # Wide radar sweep to find/track target
            self.radar_turn_rate = 30

            # PRIORITY 1: Wall avoidance (critical for kiting bot)
            if self.is_too_close_to_wall(30):
                # print(f"⚠️ Wall avoidance triggered at ({self.get_x():.0f}, {self.get_y():.0f})")
                self.avoid_walls()
            # PRIORITY 2: Kite if we have a target
            elif self.target_x is not None:
                self.kite_target()
            # PRIORITY 3: Search for targets
            else:
                self.search_pattern()

            await self.go()

    def kite_target(self):
        """Maintain optimal distance from target - kiting mechanics"""
        # Calculate distance to target
        dx = self.target_x - self.get_x()
        dy = self.target_y - self.get_y()
        distance = math.sqrt(dx*dx + dy*dy)

        # Calculate angle to target
        angle_to_target = self.calculate_angle(
            self.get_x(), self.get_y(),
            self.target_x, self.target_y
        )

        # Kiting logic: maintain optimal distance
        if distance < self.min_distance:
            # TOO CLOSE - Kite away while facing target
            # print(f"⚠️ Too close ({distance:.0f}) - kiting away!")
            # Move away from target
            retreat_angle = angle_to_target + 180
            self.turn_to(retreat_angle)
            self.target_speed = 60

        elif distance > self.max_distance:
            # TOO FAR - Move closer
            # print(f"🎯 Too far ({distance:.0f}) - closing in...")
            self.turn_to(angle_to_target)
            self.target_speed = 50

        else:
            # OPTIMAL DISTANCE - Strafe to stay mobile
            # print(f"✓ Optimal range ({distance:.0f}) - strafing...")
            # Strafe perpendicular to target
            strafe_angle = angle_to_target + 90
            self.turn_to(strafe_angle)
            self.target_speed = 40

    def search_pattern(self):
        """Search for targets when none locked"""
        # Gentle circular search pattern
        self.target_speed = 30
        self.turn_rate = 15

    async def on_scanned_bot(self, event):
        """
        When we see an enemy - track and analyze!

        Key feature: Only fire if enemy is moving predictably (linearly)
        """
        # Lock onto first target we see (sticky targeting)
        if self.target_id is None:
            self.target_id = event.scanned_bot_id
            # print(f"🎯 Target locked: {self.target_id}")

        # Only track our locked target
        if event.scanned_bot_id != self.target_id:
            return

        # Update target position
        self.target_x = event.x
        self.target_y = event.y
        self.target_speed = event.speed
        self.target_direction = event.direction

        # Calculate distance
        dx = self.target_x - self.get_x()
        dy = self.target_y - self.get_y()
        distance = math.sqrt(dx*dx + dy*dy)

        # Add to history for linearity detection
        self.target_history.append({
            'x': event.x,
            'y': event.y,
            'tick': self.get_turn_number()
        })

        # Check if target is moving linearly
        is_linear = self.detect_linear_movement()

        if is_linear:
            self.consecutive_linear_scans += 1
            # print(f"📈 Linear movement detected! ({self.consecutive_linear_scans}/{self.linear_threshold})")
        else:
            self.consecutive_linear_scans = 0
            # print(f"🔀 Erratic movement - holding fire")

        # Predict future position
        future_x, future_y = self.predict_position(event, distance)

        # Aim at predicted position
        aim_angle = self.calculate_angle(self.get_x(), self.get_y(), future_x, future_y)
        gun_turn = self.calc_gun_turn(aim_angle)
        self.gun_turn_rate = gun_turn

        # ONLY FIRE if target has been linear for enough scans AND gun is aimed
        if self.consecutive_linear_scans >= self.linear_threshold and abs(gun_turn) < 15:
            power = self.choose_fire_power(distance)
            await self.fire(power)
            # print(f"💥 FIRING! Target predictable for {self.consecutive_linear_scans} scans")

    def detect_linear_movement(self):
        """
        Detect if enemy is moving in a straight line

        Returns True if recent positions form roughly a straight line
        """
        if len(self.target_history) < 3:
            return False

        positions = list(self.target_history)

        # Calculate movement vectors between consecutive positions
        vectors = []
        for i in range(len(positions) - 1):
            dx = positions[i+1]['x'] - positions[i]['x']
            dy = positions[i+1]['y'] - positions[i]['y']

            # Calculate angle of movement
            if dx != 0 or dy != 0:
                angle = math.degrees(math.atan2(dx, dy))
                vectors.append(angle)

        if len(vectors) < 2:
            return False

        # Check if all movement angles are similar (within 20 degrees)
        first_angle = vectors[0]
        for angle in vectors[1:]:
            diff = abs(angle - first_angle)
            # Normalize angle difference
            if diff > 180:
                diff = 360 - diff

            if diff > 20:  # Not linear enough
                return False

        return True

    def predict_position(self, event, distance):
        """
        Predict where enemy will be when bullet arrives

        Uses linear prediction from Week 2
        """
        # Estimate bullet travel time
        bullet_power = self.choose_fire_power(distance)
        bullet_speed = 20 - (3 * bullet_power)
        time_to_hit = distance / bullet_speed

        # Calculate future position
        heading_rad = math.radians(event.direction)
        future_x = event.x + event.speed * time_to_hit * math.sin(heading_rad)
        future_y = event.y + event.speed * time_to_hit * math.cos(heading_rad)

        # Validate prediction is in arena
        margin = 20
        if (future_x < margin or future_x > self.get_arena_width() - margin or
            future_y < margin or future_y > self.get_arena_height() - margin):
            # Out of bounds - use current position
            future_x = event.x
            future_y = event.y

        return future_x, future_y

    def choose_fire_power(self, distance):
        """
        Choose bullet power based on distance

        Returns: power level (1-3)
        """
        # Energy management
        if self.get_energy() < 20:
            return 1

        # Distance-based power - sniper prefers accuracy over damage
        if distance < 200:
            return 2  # Medium power at close range
        elif distance < 400:
            return 2  # Sweet spot for sniping
        else:
            return 1  # Long range - fast bullet for accuracy

    async def on_hit_by_bullet(self, event):
        """React when hit - immediate evasion!"""
        # print(f"💥 Hit! Energy: {self.get_energy():.0f} - Evading!")

        # Emergency evasion - break pattern
        self.turn_rate = 90
        self.target_speed = 70

    def is_too_close_to_wall(self, margin):
        """Check if near walls"""
        return (self.get_x() < margin or
                self.get_x() > self.get_arena_width() - margin or
                self.get_y() < margin or
                self.get_y() > self.get_arena_height() - margin)

    def avoid_walls(self):
        """Turn away from walls - critical for kiting bot"""
        # If very close, back up
        if self.is_too_close_to_wall(20):
            self.target_speed = -50
            # Turn toward center
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
# ✓ Patient - only fires at predictable targets
# ✓ Maintains optimal sniping distance
# ✓ Tracks enemy movement patterns
# ✓ Kites to stay safe
# ✓ Strong wall avoidance
# ✓ Energy management
# ✓ Selective aggression

# Weaknesses:
# ❌ May miss opportunities waiting for linear movement
# ❌ Sticky targeting (won't switch targets)
# ❌ Can be overwhelmed by erratic opponents
# ❌ Requires time to detect patterns

if __name__ == "__main__":
    import asyncio
    from pathlib import Path

    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "stalker_bot.json"

    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))

    # Create and start the bot
    bot = StalkerBot(bot_info=bot_info)
    asyncio.run(bot.start())
