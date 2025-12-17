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

        # Set independence flags - gun and radar move independently
        self.set_adjust_gun_for_body_turn(True)
        self.set_adjust_radar_for_body_turn(True)
        self.set_adjust_radar_for_gun_turn(True)

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

        # Calculate distance once
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

        # Calculate fire power once (reuse for prediction and firing)
        fire_power = self.choose_fire_power(distance)

        # Predict future position using calculated fire power
        future_x, future_y = self.predict_position(event, distance, fire_power)

        # Aim at predicted position
        aim_angle = self.calculate_angle(self.get_x(), self.get_y(), future_x, future_y)
        gun_turn = self.calc_gun_turn(aim_angle)

        # Set gun turn rate (use property API, not method call)
        self.gun_turn_rate = gun_turn

        # ONLY FIRE if target has been linear for enough scans AND gun is nearly aligned
        if self.consecutive_linear_scans >= self.linear_threshold and abs(gun_turn) < 15:
            await self.fire(fire_power)
            # print(f"💥 FIRING! Target predictable for {self.consecutive_linear_scans} scans")

    def detect_linear_movement(self):
        """
        Detect if enemy is moving in a straight line

        Returns True if recent positions form roughly a straight line.
        Optimized to check angles on-the-fly without intermediate list.
        """
        if len(self.target_history) < 3:
            return False

        positions = list(self.target_history)

        # Calculate baseline angle from first movement
        dx = positions[1]['x'] - positions[0]['x']
        dy = positions[1]['y'] - positions[0]['y']

        # If no movement, can't determine linearity
        if dx == 0 and dy == 0:
            return False

        baseline_angle = math.degrees(math.atan2(dx, dy))

        # Check subsequent movements against baseline
        for i in range(1, len(positions) - 1):
            dx = positions[i+1]['x'] - positions[i]['x']
            dy = positions[i+1]['y'] - positions[i]['y']

            # Skip stationary frames
            if dx == 0 and dy == 0:
                continue

            # Calculate angle of this movement
            angle = math.degrees(math.atan2(dx, dy))

            # Calculate normalized angle difference
            diff = abs(angle - baseline_angle)
            if diff > 180:
                diff = 360 - diff

            # If deviation exceeds threshold, movement is not linear
            if diff > 20:
                return False

        return True

    def predict_position(self, event, distance, fire_power):
        """
        Predict where enemy will be when bullet arrives

        Args:
            event: Scanned bot event
            distance: Distance to target
            fire_power: Bullet power to use (pre-calculated)

        Returns:
            (future_x, future_y): Predicted position
        """
        # Calculate bullet travel time using provided fire power
        bullet_speed = 20 - (3 * fire_power)
        time_to_hit = distance / bullet_speed

        # Calculate future position based on current velocity
        heading_rad = math.radians(event.direction)
        future_x = event.x + event.speed * time_to_hit * math.sin(heading_rad)
        future_y = event.y + event.speed * time_to_hit * math.cos(heading_rad)

        # Validate prediction is in arena bounds
        margin = 20
        if (future_x < margin or future_x > self.get_arena_width() - margin or
            future_y < margin or future_y > self.get_arena_height() - margin):
            # Out of bounds - use current position as fallback
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
        """
        Simple, effective wall avoidance:
        1. Back up at full speed
        2. Turn 90 degrees away from nearest wall
        """
        # Always back up when near walls
        self.target_speed = -80  # FULL REVERSE!

        # Determine which wall is nearest and turn perpendicular to it
        x = self.get_x()
        y = self.get_y()
        arena_width = self.get_arena_width()
        arena_height = self.get_arena_height()

        dist_left = x
        dist_right = arena_width - x
        dist_top = arena_height - y
        dist_bottom = y

        # Find nearest wall and turn 90° away from it
        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        if min_dist == dist_left:
            # Near left wall - turn right (East)
            self.turn_rate = 20
        elif min_dist == dist_right:
            # Near right wall - turn left (West)
            self.turn_rate = -20
        elif min_dist == dist_top:
            # Near top wall - turn down (South)
            self.turn_rate = 20
        else:
            # Near bottom wall - turn up (North)
            self.turn_rate = -20

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
