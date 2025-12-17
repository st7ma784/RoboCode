"""SniperBot - The ultimate targeting machine!

Week 5 Tutorial - Advanced Targeting
Combines all skills from Weeks 1-5:
- Smart power selection based on hit probability
- Shot simulation before firing
- Energy management
- Position prediction
- Boundary checking
- Strategic movement
"""
import math
import random
from robocode_tank_royale.bot_api import Bot, BotInfo

class SniperBot(Bot):
    """Advanced targeting with hit probability calculations"""

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set independence flags for independent gun/radar control

        # Statistics tracking
        self.shots_fired = 0
        self.shots_hit = 0
        self.enemy_energy = None
        self.enemy_last_position = None

    async def run(self):
        """Main loop - smart movement and scanning"""
        while True:
            # Use boundary checking (Week 3)
            if not self.is_too_close_to_wall(50):
                # Safe to move
                self.forward(40)
                self.turn_right(15)
            else:
                # Avoid walls
                self.avoid_walls()

            # Keep radar sweeping
            self.turn_radar_right(45)
            
            await self.go()

    def on_scanned_bot(self, event):
        """
        Advanced targeting system - the heart of Week 5!

        Uses:
        - Hit probability calculation
        - Optimal power selection
        - Position prediction (Week 2)
        - Shot simulation
        - Energy management
        """
        distance = event.distance
        velocity = event.speed

        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.x + distance * math.sin(bearing_rad)
        enemy_y = self.y + distance * math.cos(bearing_rad)

        # Step 1: Choose optimal power based on hit probability
        power = self.choose_optimal_power(distance, velocity)

        # Step 2: Predict where enemy will be
        bullet_speed = 20 - (3 * power)
        time_to_hit = distance / bullet_speed

        future_x, future_y = self.predict_position(
            enemy_x,
            enemy_y,
            velocity,
            event.direction,
            time_to_hit
        )

        # Step 3: Validate prediction is in bounds (Week 3)
        if not self.is_valid_target(future_x, future_y):
            print("⚠️  Predicted position out of bounds - using current position")
            future_x, future_y = enemy_x, enemy_y

        # Step 4: Simulate the shot
        will_hit, hit_x, hit_y = self.simulate_shot(future_x, future_y, power)

        # Step 5: Decide whether to shoot
        hit_prob = self.calculate_hit_probability(distance, velocity, power)

        # Shoot if simulation passed OR we're very close (emergency)
        if will_hit or distance < 100:
            angle = self.calculate_angle(self.x, self.y, future_x, future_y)
            self.turn_gun_to(angle)
            self.fire(power)
            self.shots_fired += 1

            print(f"🎯 Shot #{self.shots_fired}: Power {power}, "
                  f"Prob {hit_prob:.0%}, Dist {distance:.0f}")
        else:
            print(f"⏸️  Holding fire - prob {hit_prob:.0%}, simulation failed")

        # Step 6: Track enemy energy to detect when they fire
        if self.enemy_energy is not None:
            energy_drop = self.enemy_energy - event.energy

            if 0 < energy_drop <= 3:
                # Enemy just fired!
                print(f"⚠️  Enemy fired power ~{energy_drop}! Dodging...")
                self.dodge()
            elif energy_drop > 3:
                # Enemy took damage
                print(f"✓ Enemy took {energy_drop:.1f} damage!")

        self.enemy_energy = event.energy
        self.enemy_last_position = (enemy_x, enemy_y)

    def choose_optimal_power(self, distance, velocity):
        """
        Choose bullet power that maximizes expected damage

        Expected damage = hit_probability × bullet_damage
        We want the highest expected damage per energy spent

        Returns: optimal power (1, 2, or 3)
        """
        # Limit power based on our energy
        if self.energy < 20:
            max_power = 1  # Conserve energy
        elif self.energy < 50:
            max_power = 2  # Be cautious
        else:
            max_power = 3  # Go for it!

        # Calculate expected damage for each power level
        best_power = 1
        best_expected_dmg = 0

        for power in range(1, max_power + 1):
            # Calculate hit probability
            prob = self.calculate_hit_probability(distance, velocity, power)

            # Calculate damage if we hit
            damage = 4 * power

            # Expected damage = probability × damage
            expected_damage = prob * damage

            if expected_damage > best_expected_dmg:
                best_expected_dmg = expected_damage
                best_power = power

        return best_power

    def calculate_hit_probability(self, distance, enemy_velocity, bullet_power):
        """
        Estimate probability of hitting target (0.0 to 1.0)

        Factors considered:
        - Enemy movement during bullet travel time
        - Distance to target
        - Bullet speed (affected by power)
        """
        # Calculate bullet speed
        bullet_speed = 20 - (3 * bullet_power)

        # Time for bullet to reach target
        time_to_hit = distance / bullet_speed

        # How far will enemy move during that time?
        enemy_movement = abs(enemy_velocity) * time_to_hit

        # Base probability from enemy movement
        # Tank width is ~36 pixels
        if enemy_movement < 36:
            # Enemy won't move much - high probability
            prob = 1.0
        elif enemy_movement > 200:
            # Enemy will move a lot - low probability
            prob = 0.1
        else:
            # Linear interpolation
            prob = 1.0 - ((enemy_movement - 36) / 164)

        # Apply distance penalty
        if distance > 400:
            prob *= 0.7  # 30% penalty
        if distance > 600:
            prob *= 0.5  # Additional 50% penalty

        # Clamp to valid range
        return max(0.0, min(1.0, prob))

    def simulate_shot(self, target_x, target_y, bullet_power):
        """
        Simulate a bullet traveling to target position

        Returns: (will_hit, final_x, final_y)
        - will_hit: True if bullet reaches target before hitting wall
        - final_x, final_y: where bullet ends up
        """
        # Calculate angle to target
        angle = self.calculate_angle(self.x, self.y, target_x, target_y)
        angle_rad = math.radians(angle)

        # Bullet speed
        bullet_speed = 20 - (3 * bullet_power)

        # Start bullet at our position
        bullet_x = self.x
        bullet_y = self.y

        # Simulate bullet path (max 100 steps)
        for _ in range(100):
            # Move bullet one step
            bullet_x += bullet_speed * math.sin(angle_rad)
            bullet_y += bullet_speed * math.cos(angle_rad)

            # Check if hit wall
            if (bullet_x < 0 or bullet_x > self.arena_width or
                bullet_y < 0 or bullet_y > self.arena_height):
                # Bullet went out of bounds
                return (False, bullet_x, bullet_y)

            # Check if reached target area
            distance_to_target = math.sqrt(
                (bullet_x - target_x)**2 +
                (bullet_y - target_y)**2
            )

            if distance_to_target < 25:  # Within hit radius
                # Bullet will hit target!
                return (True, bullet_x, bullet_y)

        # Bullet traveled too far without hitting
        return (False, bullet_x, bullet_y)

    def predict_position(self, x, y, velocity, heading, time):
        """
        Predict future position of moving tank (from Week 2)

        x, y: current position
        velocity: speed
        heading: direction (degrees)
        time: how many ticks in future

        Returns: (future_x, future_y)
        """
        heading_rad = math.radians(heading)

        # Calculate displacement
        dx = velocity * time * math.sin(heading_rad)
        dy = velocity * time * math.cos(heading_rad)

        future_x = x + dx
        future_y = y + dy

        return future_x, future_y

    def dodge(self):
        """Quick evasive maneuver (from Week 4)"""
        dodge_move = random.randint(1, 3)

        if dodge_move == 1:
            # Quick turn and advance
            self.turn_right(90)
            self.forward(80)
        elif dodge_move == 2:
            # Turn and retreat
            self.turn_left(90)
            self.back(60)
        else:
            # Sudden direction change
            self.turn_right(135)
            self.forward(70)

    def is_too_close_to_wall(self, margin):
        """Check if near any wall (from Week 3)"""
        return (self.x < margin or
                self.x > self.arena_width - margin or
                self.y < margin or
                self.y > self.arena_height - margin)

    def avoid_walls(self):
        """Turn away from nearest wall (from Week 3)"""
        # Simple avoidance: back up and turn
        self.back(50)

        # Turn toward center
        center_x = self.arena_width / 2
        center_y = self.arena_height / 2
        angle_to_center = self.calculate_angle(self.x, self.y, center_x, center_y)
        self.turn_to(angle_to_center)

    def is_valid_target(self, x, y):
        """Check if target is in bounds (from Week 3)"""
        margin = 20
        return (margin < x < self.arena_width - margin and
                margin < y < self.arena_height - margin)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle from one point to another (from Week 2)"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    def turn_to(self, angle):
        """Turn to absolute angle"""
        turn_amount = angle - self.direction
        while turn_amount > 180:
            turn_amount -= 360
        while turn_amount < -180:
            turn_amount += 360
        self.turn_right(turn_amount)

    def on_hit_by_bullet(self, event):
        """React to being hit"""
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"💥 Hit! Energy: {self.energy:.0f}, My accuracy: {accuracy:.1f}%")
        self.dodge()

    def on_bullet_hit(self, event):
        """Track successful hits"""
        self.shots_hit += 1
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"✓ CONFIRMED HIT! Accuracy: {accuracy:.1f}% ({self.shots_hit}/{self.shots_fired})")

    def on_bullet_missed(self, event):
        """Track misses for learning"""
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"✗ Miss. Accuracy: {accuracy:.1f}%")

    def on_won(self, event):
        """Victory statistics"""
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"\n🏆 VICTORY! 🏆")
        print(f"Final stats:")
        print(f"  Accuracy: {accuracy:.1f}%")
        print(f"  Shots: {self.shots_hit}/{self.shots_fired}")
        print(f"  Energy remaining: {self.energy:.0f}")

    def on_death(self, event):
        """Defeat statistics"""
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"\n💀 Defeated...")
        print(f"Final stats:")
        print(f"  Accuracy: {accuracy:.1f}%")
        print(f"  Shots: {self.shots_hit}/{self.shots_fired}")

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "sniper_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = SniperBot(bot_info=bot_info)
    asyncio.run(bot.start())
