"""
ChampionBot - Master tank using all advanced techniques

Difficulty: ★★★★★ (Level 5)

This tank demonstrates ALL concepts from Weeks 1-5:
- Week 1: Basic structure and events
- Week 2: Trigonometry and prediction
- Week 3: Boundary checking and validation
- Week 4: Unpredictable movement and strategy
- Week 5: Hit probability and shot simulation

This is the ultimate opponent!
"""


from robocode_tank_royale.bot_api import Bot, BotInfo, Color
import math
import random
class ChampionBot(Bot):
    """Master tank using all advanced techniques"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set distinctive color - PURPLE!
        self.body_color = Color.from_rgb(156, 39, 176)  # Purple
        self.turret_color = Color.from_rgb(233, 30, 99)  # Pink
        self.radar_color = Color.from_rgb(255, 235, 59)  # Yellow
        
        # Enemy tracking
        self.enemy_energy = None
        self.enemy_history = []  # Track enemy positions

        # Movement strategy
        self.movement_pattern = "adaptive"
        self.pattern_timer = 0

        # Statistics
        self.shots_fired = 0
        self.shots_hit = 0
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

    async def run(self):
        """
        Main loop - adaptive strategy

        Combines:
        - Boundary awareness (Week 3)
        - Unpredictable movement (Week 4)
        - Radar management
        """
        print("🏆 ChampionBot.run() started!")
        print(f"🏆 Colors set: body={self.body_color}, turret={self.turret_color}, radar={self.radar_color}")
        while self.is_running():
            self.time += 1
            
            # Periodic alive check
            if self.time % 100 == 0:
                print(f"🏆 ChampionBot alive at tick {self.time}, energy: {self.get_energy():.1f}")

            # Check boundaries FIRST (Week 3)
            if self.is_too_close_to_wall(50):
                self.avoid_walls()
            else:
                # Change movement pattern occasionally (Week 4)
                if self.pattern_timer <= 0:
                    self.choose_movement_pattern()
                    self.pattern_timer = random.randint(40, 80)

                # Execute current movement
                self.execute_movement()
                self.pattern_timer -= 1

            # Smart radar
            self.radar_turn_rate = 40
            
            await self.go()

    def choose_movement_pattern(self):
        """Select movement based on situation"""
        if self.get_energy() > 70:
            # High energy - be aggressive
            patterns = ["circle", "zigzag", "aggressive"]
        elif self.get_energy() > 30:
            # Medium energy - balanced
            patterns = ["random_walk", "spiral", "circle"]
        else:
            # Low energy - defensive
            patterns = ["evasive", "defensive", "random_walk"]

        old_pattern = self.movement_pattern
        self.movement_pattern = random.choice(patterns)

        # Don't repeat
        while self.movement_pattern == old_pattern and len(patterns) > 1:
            self.movement_pattern = random.choice(patterns)

        print(f"🔄 Pattern: {self.movement_pattern}")

    def execute_movement(self):
        """Execute current movement pattern"""
        if self.movement_pattern == "circle":
            self.target_speed = 50
            self.turn_rate = 18
        elif self.movement_pattern == "zigzag":
            self.target_speed = 60
            if random.random() < 0.5:
                self.turn_rate = 30
            else:
                self.turn_rate = -(30)
        elif self.movement_pattern == "spiral":
            distance = 30 + (self.time % 60)
            self.target_speed = distance
            self.turn_rate = 25
        elif self.movement_pattern == "random_walk":
            self.target_speed = random.randint(30, 80)
            angle = random.randint(-20, 20)
            if angle < 0:
                self.turn_rate = -(abs(angle))
            else:
                self.turn_rate = angle
        elif self.movement_pattern == "aggressive":
            self.target_speed = 70
            self.turn_rate = random.randint(5, 25)
        elif self.movement_pattern == "evasive":
            if random.random() < 0.3:
                self.target_speed = -(40)
            else:
                self.target_speed = 50
            self.turn_rate = random.randint(20, 70)
        elif self.movement_pattern == "defensive":
            self.target_speed = 30
            self.turn_rate = random.randint(30, 90)

    async def on_scanned_bot(self, event):
        """
        Advanced targeting system (Week 5)

        Uses:
        - Hit probability calculation
        - Optimal power selection
        - Position prediction (Week 2)
        - Shot simulation
        - Energy tracking
        """
        # Calculate distance from x,y coordinates
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)
        velocity = event.speed

        # Enemy position is directly from event
        enemy_x = event.x
        enemy_y = event.y

        # Track enemy movement history
        self.enemy_history.append({
            'x': enemy_x,
            'y': enemy_y,
            'time': self.time
        })

        # Keep only recent history
        if len(self.enemy_history) > 10:
            self.enemy_history.pop(0)

        # Detect enemy firing (energy drop of 1-3)
        if self.enemy_energy is not None:
            energy_drop = self.enemy_energy - event.energy
            if 0 < energy_drop <= 3:
                print(f"⚠️  Enemy fired! Power ~{energy_drop}")
                self.emergency_dodge()

        self.enemy_energy = event.energy

        # Choose optimal power (Week 5)
        power = self.choose_optimal_power(distance, velocity)

        # Predict future position (Week 2 + improvements)
        bullet_speed = 20 - (3 * power)
        time_to_hit = distance / bullet_speed
        future_x, future_y = self.predict_position(
            enemy_x, enemy_y,
            velocity, event.direction,
            time_to_hit
        )

        # Validate target (Week 3)
        if not self.is_valid_target(future_x, future_y):
            future_x, future_y = enemy_x, enemy_y

        # Simulate shot (Week 5)
        will_hit, _, _ = self.simulate_shot(future_x, future_y, power)

        # Calculate hit probability
        hit_prob = self.calculate_hit_probability(distance, velocity, power)

        # Only shoot if good chance or desperate
        if will_hit or hit_prob > 0.4 or distance < 100:
            angle = self.calculate_angle(self.get_x(), self.get_y(), future_x, future_y)
            self.gun_turn_rate = self.calc_gun_turn(angle)
            await self.fire(power)
            self.shots_fired += 1
            print(f"🎯 Shot {self.shots_fired}: P{power}, {hit_prob:.0%}")
        else:
            print(f"⏸️  Hold: {hit_prob:.0%}")

    def choose_optimal_power(self, distance, velocity):
        """Choose power maximizing expected damage (Week 5)"""
        if self.get_energy() < 15:
            return 1

        best_power = 1
        best_expected = 0

        max_power = 3 if self.get_energy() > 40 else 2

        for power in range(1, max_power + 1):
            prob = self.calculate_hit_probability(distance, velocity, power)
            expected = prob * (4 * power)

            if expected > best_expected:
                best_expected = expected
                best_power = power

        return best_power

    def calculate_hit_probability(self, distance, velocity, power):
        """Estimate hit probability (Week 5)"""
        bullet_speed = 20 - (3 * power)
        time = distance / bullet_speed
        movement = abs(velocity) * time

        if movement < 36:
            prob = 1.0
        elif movement > 200:
            prob = 0.1
        else:
            prob = 1.0 - ((movement - 36) / 164)

        if distance > 400:
            prob *= 0.7
        if distance > 600:
            prob *= 0.5

        return max(0.0, min(1.0, prob))

    def simulate_shot(self, target_x, target_y, power):
        """Simulate bullet trajectory (Week 5)"""
        angle = self.calculate_angle(self.get_x(), self.get_y(), target_x, target_y)
        angle_rad = math.radians(angle)
        speed = 20 - (3 * power)

        bullet_x, bullet_y = self.get_x(), self.get_y()

        for _ in range(100):
            bullet_x += speed * math.sin(angle_rad)
            bullet_y += speed * math.cos(angle_rad)

            if (bullet_x < 0 or bullet_x > self.get_arena_width() or
                bullet_y < 0 or bullet_y > self.get_arena_height()):
                return (False, bullet_x, bullet_y)

            dist = math.sqrt((bullet_x - target_x)**2 + (bullet_y - target_y)**2)
            if dist < 25:
                return (True, bullet_x, bullet_y)

        return (False, bullet_x, bullet_y)

    def predict_position(self, x, y, velocity, heading, time):
        """Predict future position (Week 2)"""
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y

    def emergency_dodge(self):
        """Quick dodge when enemy fires (Week 4)"""
        dodge_type = random.randint(1, 3)
        if dodge_type == 1:
            self.turn_rate = 90
            self.target_speed = 70
        elif dodge_type == 2:
            self.turn_rate = -(90)
            self.target_speed = 70
        else:
            self.target_speed = -(60)

    async def on_hit_by_bullet(self, event):
        """React to damage (Week 4)"""
        self.shots_hit += 1  # Enemy hit us
        print(f"💥 Hit! Energy: {self.get_energy():.0f}")

        # Force pattern change
        self.pattern_timer = 0

        # Dodge
        self.emergency_dodge()

    def is_too_close_to_wall(self, margin):
        """Boundary check (Week 3)"""
        return (self.get_x() < margin or
                self.get_x() > self.get_arena_width() - margin or
                self.get_y() < margin or
                self.get_y() > self.get_arena_height() - margin)

    def avoid_walls(self):
        """Wall avoidance (Week 3)"""
        center_x = self.get_arena_width() / 2
        center_y = self.get_arena_height() / 2
        angle = self.calculate_angle(self.get_x(), self.get_y(), center_x, center_y)
        self.turn_to(angle)
        self.target_speed = 70

    def is_valid_target(self, x, y):
        """Target validation (Week 3)"""
        margin = 20
        return (margin < x < self.get_arena_width() - margin and
                margin < y < self.get_arena_height() - margin)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Angle calculation (Week 2)"""
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

    async def on_win(self, event):
        """Victory!"""
        print(f"\n🏆 CHAMPION WINS! 🏆")

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "champion_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = ChampionBot(bot_info=bot_info)
    asyncio.run(bot.start())
