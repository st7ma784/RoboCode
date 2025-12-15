"""
FinalBossTank - The Ultimate Tutorial Synthesis
Created by: Claude Code

This tank combines ALL concepts from Weeks 1-8:
- Week 1: Basic structure and events
- Week 2: Trigonometry and prediction
- Week 3: Boundary checking and validation
- Week 4: Unpredictable movement patterns
- Week 5: Hit probability and shot simulation
- Week 6: Modular class architecture
- Week 7: Multi-enemy tracking with NumPy
- Week 8: Anti-gravity movement and cluster detection

This is the culmination of the entire tutorial series!
"""
from robocode_tank_royale.bot_api import BaseBot, BotInfo
import numpy as np
import math
import random


# ============= WEEK 6: MODULAR ARCHITECTURE =============

class _TargetingSystem:
    """Week 2 & 7: Math utilities with NumPy optimization"""

    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """Calculate distance using Pythagorean theorem"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)

    def calculate_distances(self, my_x, my_y, enemy_x, enemy_y):
        """Calculate distance to ALL enemies at once (vectorized)"""
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.sqrt(x_diff**2 + y_diff**2)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle to target"""
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.degrees(math.atan2(x_diff, y_diff))

    def calculate_angles(self, my_x, my_y, enemy_x, enemy_y):
        """Calculate angles to ALL enemies at once"""
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.degrees(np.arctan2(x_diff, y_diff))

    def predict_position(self, x, y, velocity, heading, time):
        """Predict future position of moving target"""
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y

    def predict_positions(self, x, y, vx, vy, time):
        """Predict future positions of ALL enemies"""
        future_x = x + vx * time
        future_y = y + vy * time
        return future_x, future_y

    def calculate_bullet_speed(self, power):
        """Calculate bullet speed from power"""
        return 20 - 3 * power


# ============= WEEK 7: MULTI-ENEMY TRACKING =============

class _EnemyTracker:
    """Efficiently track multiple enemies using NumPy arrays"""

    def __init__(self, max_enemies=50):
        self.max_enemies = max_enemies
        self.enemy_ids = []
        self.x = np.array([])
        self.y = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])
        self.energy = np.array([])
        self.last_seen = np.array([])

    def update(self, enemy_id, x, y, vx, vy, energy, tick):
        """Add or update enemy in tracking system"""
        if enemy_id in self.enemy_ids:
            idx = self.enemy_ids.index(enemy_id)
            self.x[idx] = x
            self.y[idx] = y
            self.vx[idx] = vx
            self.vy[idx] = vy
            self.energy[idx] = energy
            self.last_seen[idx] = tick
        else:
            if len(self.enemy_ids) < self.max_enemies:
                self.enemy_ids.append(enemy_id)
                self.x = np.append(self.x, x)
                self.y = np.append(self.y, y)
                self.vx = np.append(self.vx, vx)
                self.vy = np.append(self.vy, vy)
                self.energy = np.append(self.energy, energy)
                self.last_seen = np.append(self.last_seen, tick)

    def cleanup(self, current_tick, max_age=100):
        """Remove stale enemy data"""
        if len(self.enemy_ids) == 0:
            return

        age = current_tick - self.last_seen
        keep = age < max_age

        if not np.any(keep):
            self.__init__(self.max_enemies)
            return

        keep_idx = np.where(keep)[0]
        self.enemy_ids = [self.enemy_ids[i] for i in keep_idx]
        self.x = self.x[keep]
        self.y = self.y[keep]
        self.vx = self.vx[keep]
        self.vy = self.vy[keep]
        self.energy = self.energy[keep]
        self.last_seen = self.last_seen[keep]

    def count(self):
        """Number of tracked enemies"""
        return len(self.enemy_ids)


# ============= WEEK 8: ANTI-GRAVITY & CLUSTER DETECTION =============

class _AntiGravityMovement:
    """Physics-based repulsive forces from enemies"""

    def __init__(self, force_constant=1500):
        self.force_constant = force_constant

    def calculate_forces(self, my_x, my_y, tracker):
        """Calculate anti-gravity forces from all enemies"""
        if tracker.count() == 0:
            return 0, 0

        dx = tracker.x - my_x
        dy = tracker.y - my_y
        distances = np.sqrt(dx**2 + dy**2)

        # Weight by threat (energy)
        threat_weights = tracker.energy / 100
        force_strengths = self.force_constant * threat_weights / (distances + 1)

        # Negative to push away
        force_x = -np.sum((dx / (distances + 1)) * force_strengths)
        force_y = -np.sum((dy / (distances + 1)) * force_strengths)

        return force_x, force_y

    def add_wall_repulsion(self, my_x, my_y, battlefield_width, battlefield_height):
        """Walls push you away too"""
        margin = 80
        fx = 0
        fy = 0

        if my_x < margin:
            fx = 500 * (margin - my_x) / margin
        elif my_x > battlefield_width - margin:
            fx = -500 * (my_x - (battlefield_width - margin)) / margin

        if my_y < margin:
            fy = 500 * (margin - my_y) / margin
        elif my_y > battlefield_height - margin:
            fy = -500 * (my_y - (battlefield_height - margin)) / margin

        return fx, fy


class _ClusterDetector:
    """Detect groups of enemies"""

    def find_clusters(self, tracker, cluster_distance=150):
        """Find enemy clusters within distance threshold"""
        if tracker.count() < 2:
            return []

        clusters = []
        clustered = set()

        for i in range(tracker.count()):
            if i in clustered:
                continue

            cluster = [i]
            clustered.add(i)

            for j in range(i + 1, tracker.count()):
                if j in clustered:
                    continue

                dx = tracker.x[i] - tracker.x[j]
                dy = tracker.y[i] - tracker.y[j]
                distance = np.sqrt(dx**2 + dy**2)

                if distance < cluster_distance:
                    cluster.append(j)
                    clustered.add(j)

            if len(cluster) > 1:
                clusters.append(cluster)

        return clusters

    def get_cluster_info(self, tracker, clusters):
        """Calculate cluster statistics"""
        info = []
        for cluster in clusters:
            center_x = np.mean(tracker.x[cluster])
            center_y = np.mean(tracker.y[cluster])
            total_energy = np.sum(tracker.energy[cluster])

            info.append({
                'center_x': center_x,
                'center_y': center_y,
                'size': len(cluster),
                'total_energy': total_energy,
                'threat_level': len(cluster) * total_energy / 100,
                'members': cluster
            })

        return info


# ============= WEEK 4: MOVEMENT PATTERNS =============

class _MovementPatternController:
    """Manages multiple unpredictable movement patterns"""

    def __init__(self):
        self.current_pattern = "adaptive"
        self.pattern_timer = 0
        self.counter = 0
        self.last_pattern = None

    def choose_pattern(self, energy):
        """Select pattern based on energy level"""
        if energy > 70:
            patterns = ["circle", "zigzag", "aggressive", "spiral"]
        elif energy > 30:
            patterns = ["random_walk", "circle", "zigzag"]
        else:
            patterns = ["evasive", "defensive", "random_walk"]

        # Don't repeat last pattern
        available = [p for p in patterns if p != self.last_pattern]
        if not available:
            available = patterns

        self.current_pattern = random.choice(available)
        self.last_pattern = self.current_pattern
        self.pattern_timer = random.randint(40, 80)

    def execute(self, tank):
        """Execute current movement pattern"""
        self.counter += 1

        if self.current_pattern == "circle":
            tank.forward(50)
            tank.turn_right(18)
        elif self.current_pattern == "zigzag":
            tank.forward(60)
            tank.turn_right(30 if random.random() < 0.5 else -30)
        elif self.current_pattern == "spiral":
            distance = 30 + (self.counter % 60)
            tank.forward(distance)
            tank.turn_right(25)
        elif self.current_pattern == "random_walk":
            tank.forward(random.randint(30, 80))
            tank.turn_right(random.randint(-20, 20))
        elif self.current_pattern == "aggressive":
            tank.forward(70)
            tank.turn_right(random.randint(5, 25))
        elif self.current_pattern == "evasive":
            if random.random() < 0.3:
                tank.back(40)
            else:
                tank.forward(50)
            tank.turn_right(random.randint(20, 70))
        elif self.current_pattern == "defensive":
            tank.forward(30)
            tank.turn_right(random.randint(30, 90))


# ============= WEEK 5: ADVANCED TARGETING =============

class _AdvancedTargetingSystem:
    """Hit probability, shot simulation, optimal power selection"""

    def __init__(self):
        self.targeting = _TargetingSystem()

    def calculate_hit_probability(self, distance, velocity, power):
        """Estimate hit probability based on distance and velocity"""
        bullet_speed = 20 - (3 * power)
        time = distance / bullet_speed
        movement = abs(velocity) * time

        if movement < 36:
            prob = 1.0
        elif movement > 200:
            prob = 0.1
        else:
            prob = 1.0 - ((movement - 36) / 164)

        # Distance penalty
        if distance > 400:
            prob *= 0.7
        if distance > 600:
            prob *= 0.5

        return max(0.0, min(1.0, prob))

    def simulate_shot(self, my_x, my_y, target_x, target_y, power, battlefield_width, battlefield_height):
        """Simulate bullet trajectory to verify hit"""
        angle = self.targeting.calculate_angle(my_x, my_y, target_x, target_y)
        angle_rad = math.radians(angle)
        speed = 20 - (3 * power)

        bullet_x, bullet_y = my_x, my_y

        for _ in range(100):
            bullet_x += speed * math.sin(angle_rad)
            bullet_y += speed * math.cos(angle_rad)

            # Hit wall
            if (bullet_x < 0 or bullet_x > battlefield_width or
                bullet_y < 0 or bullet_y > battlefield_height):
                return False

            # Hit target
            dist = math.sqrt((bullet_x - target_x)**2 + (bullet_y - target_y)**2)
            if dist < 25:
                return True

        return False

    def choose_optimal_power(self, distance, velocity, energy):
        """Select power that maximizes expected damage"""
        if energy < 15:
            return 1

        best_power = 1
        best_expected = 0
        max_power = 3 if energy > 40 else 2

        for power in range(1, max_power + 1):
            prob = self.calculate_hit_probability(distance, velocity, power)
            expected = prob * (4 * power)

            if expected > best_expected:
                best_expected = expected
                best_power = power

        return best_power


# ============= WEEK 3: BOUNDARY CHECKING =============

class _BoundaryValidator:
    """Validate positions and avoid walls"""

    def is_valid_target(self, x, y, battlefield_width, battlefield_height):
        """Check if target position is inside arena"""
        margin = 20
        return (margin < x < battlefield_width - margin and
                margin < y < battlefield_height - margin)

    def is_too_close_to_wall(self, x, y, battlefield_width, battlefield_height, margin=50):
        """Check if too close to any wall"""
        return (x < margin or x > battlefield_width - margin or
                y < margin or y > battlefield_height - margin)


# ============= FINAL BOSS TANK =============

class FinalBossTank(BaseBot):
    """
    The ultimate tank combining all 8 weeks of tutorials

    Features:
    - Anti-gravity movement with cluster awareness
    - Multi-enemy tracking with NumPy
    - Advanced targeting with hit probability
    - Shot simulation before firing
    - Unpredictable movement patterns
    - Boundary checking and validation
    - Modular, clean architecture
    """

    def __init__(self):
        super().__init__()
        self.name = "FinalBossTank"

        # Week 7: Enemy tracking
        self.enemies = _EnemyTracker(max_enemies=50)

        # Week 6: Modular systems
        self.targeting = _TargetingSystem()
        self.advanced_targeting = _AdvancedTargetingSystem()
        self.boundary = _BoundaryValidator()

        # Week 8: Anti-gravity & clusters
        self.anti_gravity = _AntiGravityMovement(force_constant=1500)
        self.cluster_detector = _ClusterDetector()

        # Week 4: Movement patterns
        self.movement_controller = _MovementPatternController()

        # State
        self.tick = 0
        self.radar_direction = 1
        self.mode = "hybrid"  # hybrid, pattern, anti_gravity
        self.mode_timer = 0

        # Statistics
        self.shots_fired = 0
        self.max_enemies_seen = 0
    
    def turn_to(self, target_angle):
        """Helper to turn to absolute angle"""
        current = self.direction % 360
        target = target_angle % 360
        diff = (target - current + 180) % 360 - 180
        if diff < 0:
            self.turn_left(abs(diff))
        else:
            self.turn_right(diff)

    async def run(self):
        """Main loop - Week 1 structure with advanced logic"""
        while True:
            self.tick += 1

            # Week 7: Periodic cleanup
            if self.tick % 20 == 0:
                self.enemies.cleanup(self.tick)
                if self.enemies.count() > self.max_enemies_seen:
                    self.max_enemies_seen = self.enemies.count()

            # Week 3: Emergency wall avoidance
            if self.boundary.is_too_close_to_wall(self.x, self.y,
                                                   self.arena_width,
                                                   self.arena_height, margin=50):
                self.emergency_wall_escape()
                self.turn_radar_right(45)
                await self.go()
                continue

            # Adaptive mode selection
            self.select_mode()

            # Execute movement based on mode
            if self.mode == "anti_gravity" and self.enemies.count() > 0:
                # Week 8: Anti-gravity when enemies nearby
                self.execute_anti_gravity_movement()
            elif self.mode == "hybrid" and self.enemies.count() > 0:
                # Combine anti-gravity with patterns
                self.execute_hybrid_movement()
            else:
                # Week 4: Pattern-based movement
                self.execute_pattern_movement()

            # Radar sweep
            self.turn_radar_right(self.radar_direction * 45)
            if self.tick % 8 == 0:
                self.radar_direction *= -1

            # Week 5 & 7: Engage best target
            if self.enemies.count() > 0:
                self.engage_best_target()
            
            await self.go()

    def select_mode(self):
        """Choose movement mode based on situation"""
        if self.mode_timer <= 0:
            enemy_count = self.enemies.count()

            if enemy_count >= 5:
                self.mode = "anti_gravity"
                self.mode_timer = 80
            elif enemy_count >= 2:
                self.mode = "hybrid"
                self.mode_timer = 60
            else:
                self.mode = "pattern"
                self.mode_timer = 100

    def execute_anti_gravity_movement(self):
        """Week 8: Pure anti-gravity movement"""
        enemy_fx, enemy_fy = self.anti_gravity.calculate_forces(
            self.x, self.y, self.enemies
        )
        wall_fx, wall_fy = self.anti_gravity.add_wall_repulsion(
            self.x, self.y,
            self.arena_width,
            self.arena_height
        )

        total_fx = enemy_fx + wall_fx
        total_fy = enemy_fy + wall_fy

        if total_fx != 0 or total_fy != 0:
            escape_angle = np.degrees(np.arctan2(total_fx, total_fy))
            self.turn_to(escape_angle)

            force_magnitude = np.sqrt(total_fx**2 + total_fy**2)
            move_speed = min(40, 20 + force_magnitude / 100)
            self.forward(move_speed)
        else:
            self.forward(20)

    def execute_hybrid_movement(self):
        """Combine anti-gravity with pattern variations"""
        # Get anti-gravity suggestion
        enemy_fx, enemy_fy = self.anti_gravity.calculate_forces(
            self.x, self.y, self.enemies
        )
        wall_fx, wall_fy = self.anti_gravity.add_wall_repulsion(
            self.x, self.y,
            self.arena_width,
            self.arena_height
        )

        # Apply 50% anti-gravity, 50% pattern
        if enemy_fx != 0 or enemy_fy != 0:
            escape_angle = np.degrees(np.arctan2(enemy_fx + wall_fx, enemy_fy + wall_fy))
            self.turn_to(escape_angle)

        # Add pattern variation
        self.movement_controller.execute(self)

    def execute_pattern_movement(self):
        """Week 4: Pattern-based movement"""
        if self.movement_controller.pattern_timer <= 0:
            self.movement_controller.choose_pattern(self.energy)

        self.movement_controller.execute(self)
        self.movement_controller.pattern_timer -= 1

    def emergency_wall_escape(self):
        """Week 3: Escape from walls"""
        center_x = self.arena_width / 2
        center_y = self.arena_height / 2
        angle = self.targeting.calculate_angle(self.x, self.y, center_x, center_y)
        self.turn_to(angle)
        self.forward(70)

    def on_scanned_bot(self, event):
        """Week 1: Event handler with Week 2 calculations"""
        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.x + event.distance * math.sin(bearing_rad)
        enemy_y = self.y + event.distance * math.cos(bearing_rad)
        
        # Convert to velocity components
        heading_rad = math.radians(event.direction)
        vx = event.speed * math.sin(heading_rad)
        vy = event.speed * math.cos(heading_rad)

        # Week 7: Update tracker
        self.enemies.update(
            enemy_id=event.scanned_bot_id,
            x=enemy_x,
            y=enemy_y,
            vx=vx,
            vy=vy,
            energy=event.energy,
            tick=self.tick
        )

    def engage_best_target(self):
        """Week 5 & 7: Advanced target selection and engagement"""
        if self.enemies.count() == 0:
            return

        # Calculate distances to all enemies
        distances = self.targeting.calculate_distances(
            self.x, self.y,
            self.enemies.x, self.enemies.y
        )

        # Target selection: close + weak enemies
        scores = (1000 / (distances + 1)) + (100 - self.enemies.energy) * 2
        best_idx = np.argmax(scores)

        # Get target info
        target_x = self.enemies.x[best_idx]
        target_y = self.enemies.y[best_idx]
        target_vx = self.enemies.vx[best_idx]
        target_vy = self.enemies.vy[best_idx]
        target_distance = distances[best_idx]
        target_velocity = np.sqrt(target_vx**2 + target_vy**2)

        # Week 5: Choose optimal power
        bullet_power = self.advanced_targeting.choose_optimal_power(
            target_distance, target_velocity, self.energy
        )

        # Week 2: Predict position
        bullet_speed = self.targeting.calculate_bullet_speed(bullet_power)
        time_to_hit = target_distance / bullet_speed
        future_x, future_y = self.targeting.predict_positions(
            np.array([target_x]),
            np.array([target_y]),
            np.array([target_vx]),
            np.array([target_vy]),
            time_to_hit
        )

        # Week 3: Validate target
        if not self.boundary.is_valid_target(future_x[0], future_y[0],
                                             self.arena_width,
                                             self.arena_height):
            future_x[0], future_y[0] = target_x, target_y

        # Week 5: Calculate hit probability
        hit_prob = self.advanced_targeting.calculate_hit_probability(
            target_distance, target_velocity, bullet_power
        )

        # Week 5: Simulate shot
        will_hit = self.advanced_targeting.simulate_shot(
            self.x, self.y, future_x[0], future_y[0],
            bullet_power, self.arena_width, self.arena_height
        )

        # Fire if good shot or desperate
        if will_hit or hit_prob > 0.35 or target_distance < 150:
            angle = self.targeting.calculate_angle(
                self.x, self.y, future_x[0], future_y[0]
            )
            self.turn_gun_to(angle)
            self.fire(bullet_power)
            self.shots_fired += 1

    def on_hit_by_bullet(self, event):
        """Week 4: Reactive dodging"""
        # Force mode/pattern change
        self.mode_timer = 0
        self.movement_controller.pattern_timer = 0

        # Emergency dodge
        dodge = random.choice(['right', 'left', 'back'])
        if dodge == 'right':
            self.turn_right(90)
            self.forward(70)
        elif dodge == 'left':
            self.turn_left(90)
            self.forward(70)
        else:
            self.back(60)

    def on_hit_wall(self, event):
        """Week 1 & 3: Wall collision handler"""
        self.back(50)
        self.turn_right(90)

    def on_robot_death(self, event):
        """Track eliminations"""
        pass


# Main entry point
if __name__ == "__main__":
    bot = FinalBossTank()
    bot.start()
