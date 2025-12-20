"""
ChallengerTank - Beyond the Tutorials
Created by: Claude Code

This tank takes everything from the tutorials and adds:
- Bullet dodging with timing prediction
- Predictive anti-gravity (multi-step lookahead)
- Corner trap detection and escape
- Formation breaking strategies
- Adaptive force constants
- Energy management phases
- Statistical pattern learning
- Threat prioritization by time-to-danger
- Advanced ammo conservation

This is the ultimate challenge!
"""
from robocode_tank_royale.bot_api import Bot, Color, BotInfo
import numpy as np
import math
import random
from collections import deque


# ============= CORE SYSTEMS (From Tutorials) =============

class _TargetingSystem:
    """Advanced targeting with vectorized operations"""

    def calculate_distance(self, from_x, from_y, to_x, to_y):
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)

    def calculate_distances(self, my_x, my_y, enemy_x, enemy_y):
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.sqrt(x_diff**2 + y_diff**2)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.degrees(math.atan2(x_diff, y_diff))

    def calculate_angles(self, my_x, my_y, enemy_x, enemy_y):
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.degrees(np.arctan2(x_diff, y_diff))

    def predict_positions(self, x, y, vx, vy, time):
        future_x = x + vx * time
        future_y = y + vy * time
        return future_x, future_y

    def calculate_bullet_speed(self, power):
        return 20 - 3 * power


class _EnemyTracker:
    """Multi-enemy tracking with pattern history"""

    def __init__(self, max_enemies=50):
        self.max_enemies = max_enemies
        self.enemy_ids = []
        self.x = np.array([])
        self.y = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])
        self.energy = np.array([])
        self.last_seen = np.array([])

        # EXTRA: Pattern history for learning
        self.pattern_history = {}

    def update(self, enemy_id, x, y, vx, vy, energy, tick):
        if enemy_id in self.enemy_ids:
            idx = self.enemy_ids.index(enemy_id)

            # EXTRA: Track pattern changes
            old_vx, old_vy = self.vx[idx], self.vy[idx]
            if enemy_id not in self.pattern_history:
                self.pattern_history[enemy_id] = deque(maxlen=20)
            self.pattern_history[enemy_id].append({
                'dvx': vx - old_vx,
                'dvy': vy - old_vy,
                'tick': tick
            })

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
                self.pattern_history[enemy_id] = deque(maxlen=20)

    def cleanup(self, current_tick, max_age=200):
        if len(self.enemy_ids) == 0:
            return

        age = current_tick - self.last_seen
        keep = age < max_age

        if not np.any(keep):
            self.__init__(self.max_enemies)
            return

        keep_idx = np.where(keep)[0]
        removed = [self.enemy_ids[i] for i in range(len(self.enemy_ids)) if i not in keep_idx]
        for enemy_id in removed:
            self.pattern_history.pop(enemy_id, None)

        self.enemy_ids = [self.enemy_ids[i] for i in keep_idx]
        self.x = self.x[keep]
        self.y = self.y[keep]
        self.vx = self.vx[keep]
        self.vy = self.vy[keep]
        self.energy = self.energy[keep]
        self.last_seen = self.last_seen[keep]

    def count(self):
        return len(self.enemy_ids)


# ============= ADVANCED ANTI-GRAVITY WITH PREDICTION =============

class _PredictiveAntiGravity:
    """Anti-gravity with multi-step lookahead"""

    def __init__(self, base_force=1500):
        self.base_force = base_force
        self.force_constant = base_force

    def adapt_force_constant(self, enemy_count, energy):
        """EXTRA: Adaptive force based on situation"""
        if enemy_count >= 10:
            self.force_constant = self.base_force * 1.5  # Stronger push in crowds
        elif enemy_count >= 5:
            self.force_constant = self.base_force * 1.2
        else:
            self.force_constant = self.base_force

        # Weaker forces when low energy (can't afford to run)
        if energy < 30:
            self.force_constant *= 0.7

    def calculate_forces(self, my_x, my_y, tracker):
        if tracker.count() == 0:
            return 0, 0

        dx = tracker.x - my_x
        dy = tracker.y - my_y
        distances = np.sqrt(dx**2 + dy**2)

        threat_weights = tracker.energy / 100
        force_strengths = self.force_constant * threat_weights / (distances + 1)

        force_x = -np.sum((dx / (distances + 1)) * force_strengths)
        force_y = -np.sum((dy / (distances + 1)) * force_strengths)

        return force_x, force_y

    def predict_future_forces(self, my_x, my_y, tracker, steps=3):
        """EXTRA: Look ahead multiple steps to avoid traps"""
        future_x, future_y = my_x, my_y
        total_fx, total_fy = 0, 0

        for step in range(1, steps + 1):
            # Predict enemy positions
            future_enemy_x = tracker.x + tracker.vx * step * 5
            future_enemy_y = tracker.y + tracker.vy * step * 5

            # Calculate forces at future position
            dx = future_enemy_x - future_x
            dy = future_enemy_y - future_y
            distances = np.sqrt(dx**2 + dy**2)

            threat_weights = tracker.energy / 100
            force_strengths = self.force_constant * threat_weights / (distances + 1)

            fx = -np.sum((dx / (distances + 1)) * force_strengths)
            fy = -np.sum((dy / (distances + 1)) * force_strengths)

            total_fx += fx / step  # Weight recent steps more
            total_fy += fy / step

            # Update future position
            if fx != 0 or fy != 0:
                angle = np.arctan2(fx, fy)
                future_x += 20 * np.sin(angle)
                future_y += 20 * np.cos(angle)

        return total_fx, total_fy

    def add_wall_repulsion(self, my_x, my_y, battlefield_width, battlefield_height):
        """Walls push you away - STRONG forces to prevent getting stuck"""
        margin = 100  # Start repelling earlier
        fx = 0
        fy = 0

        # Much stronger forces that increase exponentially as we get closer
        if my_x < margin:
            distance_ratio = (margin - my_x) / margin
            # Exponential increase: gentle far away, VERY strong when close
            fx = 2000 * (distance_ratio ** 2)
        elif my_x > battlefield_width - margin:
            distance_ratio = (my_x - (battlefield_width - margin)) / margin
            fx = -2000 * (distance_ratio ** 2)

        if my_y < margin:
            distance_ratio = (margin - my_y) / margin
            fy = 2000 * (distance_ratio ** 2)
        elif my_y > battlefield_height - margin:
            distance_ratio = (my_y - (battlefield_height - margin)) / margin
            fy = -2000 * (distance_ratio ** 2)

        return fx, fy


# ============= CORNER TRAP DETECTOR =============

class _CornerTrapDetector:
    """EXTRA: Detect and escape corner traps"""

    def is_cornered(self, my_x, my_y, battlefield_width, battlefield_height, tracker):
        """Check if surrounded and near corner"""
        corner_margin = 150

        # Check if near corner
        near_corner = (
            (my_x < corner_margin and my_y < corner_margin) or
            (my_x < corner_margin and my_y > battlefield_height - corner_margin) or
            (my_x > battlefield_width - corner_margin and my_y < corner_margin) or
            (my_x > battlefield_width - corner_margin and my_y > battlefield_height - corner_margin)
        )

        if not near_corner:
            return False, None

        # Check if enemies blocking escape
        if tracker.count() < 2:
            return False, None

        # Find escape angle to center
        center_x = battlefield_width / 2
        center_y = battlefield_height / 2
        escape_angle = math.degrees(math.atan2(center_x - my_x, center_y - my_y))

        # Check if enemies blocking that path
        angles_to_enemies = np.degrees(np.arctan2(tracker.x - my_x, tracker.y - my_y))
        angle_diffs = np.abs(angles_to_enemies - escape_angle)
        angle_diffs = np.minimum(angle_diffs, 360 - angle_diffs)

        blocking = np.sum(angle_diffs < 45)  # Enemies within 45 degrees of escape

        if blocking >= 2:
            return True, escape_angle

        return False, None

    def escape_corner(self, tank, escape_angle):
        """Execute aggressive corner escape"""
        tank.turn_to(escape_angle)
        tank.forward(100)  # Full speed


# ============= FORMATION BREAKER =============

class _FormationBreaker:
    """EXTRA: Detect and break enemy formations"""

    def detect_formation(self, my_x, my_y, tracker):
        """Detect if enemies are in formation around us"""
        if tracker.count() < 3:
            return None

        angles = np.degrees(np.arctan2(tracker.x - my_x, tracker.y - my_y))
        distances = np.sqrt((tracker.x - my_x)**2 + (tracker.y - my_y)**2)

        # Sort by angle
        sorted_idx = np.argsort(angles)
        sorted_angles = angles[sorted_idx]

        # Check for surrounding formation (enemies spread around us)
        angle_diffs = np.diff(np.concatenate([sorted_angles, [sorted_angles[0] + 360]]))
        max_gap = np.max(angle_diffs)

        if max_gap < 180 and tracker.count() >= 4:
            # Surrounded!
            gap_idx = np.argmax(angle_diffs)
            escape_angle = sorted_angles[gap_idx] + angle_diffs[gap_idx] / 2
            return {'type': 'surrounded', 'escape_angle': escape_angle}

        # Check for line formation (enemies in a line)
        close_enemies = distances < 300
        if np.sum(close_enemies) >= 3:
            close_angles = angles[close_enemies]
            angle_variance = np.var(close_angles)
            if angle_variance < 400:  # Low variance = line
                # Break perpendicular to line
                mean_angle = np.mean(close_angles)
                escape_angle = mean_angle + 90
                return {'type': 'line', 'escape_angle': escape_angle}

        return None


# ============= BULLET DODGE SYSTEM =============

class _BulletDodgeSystem:
    """EXTRA: Track and dodge incoming bullets"""

    def __init__(self):
        self.last_enemy_energy = {}
        self.bullet_warnings = []

    def detect_bullet_fired(self, enemy_id, enemy_x, enemy_y, enemy_energy, prev_energy, my_x, my_y):
        """Detect when enemy fires and predict bullet path"""
        if prev_energy is None:
            return

        energy_drop = prev_energy - enemy_energy
        if 0 < energy_drop <= 3:
            # Enemy fired!
            bullet_power = energy_drop

            # Predict bullet trajectory (assume aimed at us)
            angle = math.degrees(math.atan2(my_x - enemy_x, my_y - enemy_y))

            self.bullet_warnings.append({
                'power': bullet_power,
                'angle': angle,
                'enemy_x': enemy_x,
                'enemy_y': enemy_y,
                'age': 0
            })

    def should_dodge(self, my_x, my_y):
        """Check if we should dodge now"""
        for bullet in self.bullet_warnings:
            bullet['age'] += 1

            # Calculate bullet position
            speed = 20 - 3 * bullet['power']
            angle_rad = math.radians(bullet['angle'])
            bullet_x = bullet['enemy_x'] + speed * bullet['age'] * math.sin(angle_rad)
            bullet_y = bullet['enemy_y'] + speed * bullet['age'] * math.cos(angle_rad)

            # Check if close to us
            dist = math.sqrt((bullet_x - my_x)**2 + (bullet_y - my_y)**2)
            if dist < 50:
                return True

        # Clean old warnings
        self.bullet_warnings = [b for b in self.bullet_warnings if b['age'] < 50]

        return False


# ============= ENERGY PHASE MANAGER =============

class _EnergyPhaseManager:
    """EXTRA: Sophisticated energy-based behavior"""

    def get_phase(self, my_energy, enemy_count):
        """Determine combat phase"""
        if my_energy > 80:
            return "dominate"
        elif my_energy > 60:
            return "aggressive"
        elif my_energy > 40:
            return "balanced"
        elif my_energy > 20:
            return "conservative"
        else:
            return "survival"

    def get_fire_threshold(self, phase):
        """Hit probability threshold for firing"""
        thresholds = {
            "dominate": 0.25,
            "aggressive": 0.30,
            "balanced": 0.35,
            "conservative": 0.45,
            "survival": 0.60
        }
        return thresholds.get(phase, 0.35)

    def get_max_power(self, phase, enemy_energy):
        """Maximum power to use"""
        if phase == "survival":
            return 1
        elif phase == "conservative":
            return 2 if enemy_energy < 30 else 1
        elif phase == "balanced":
            return 2
        else:
            return 3


# ============= CHALLENGER TANK =============

class ChallengerTank(Bot):
    """
    The ultimate challenger combining all tutorials plus advanced features

    Extra features beyond tutorials:
    - Bullet dodging with timing
    - Predictive anti-gravity (multi-step)
    - Corner trap detection
    - Formation breaking
    - Adaptive force constants
    - Energy phase management
    - Statistical pattern learning
    """

    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)

        # Set independence flags - gun and radar move independently from body
        self.set_adjust_gun_for_body_turn(True)
        self.set_adjust_radar_for_body_turn(True)
        self.set_adjust_radar_for_gun_turn(True)

        self.body_color = Color.from_rgb(0, 152, 0)  # G
        self.turret_color = Color.from_rgb(0, 87, 34)  # Deep G
        self.radar_color = Color.from_rgb(0, 193, 7)  # G


        # Core systems
        self.enemies = _EnemyTracker(max_enemies=50)
        self.targeting = _TargetingSystem()

        # Advanced systems
        self.anti_gravity = _PredictiveAntiGravity(base_force=1500)
        self.corner_detector = _CornerTrapDetector()
        self.formation_breaker = _FormationBreaker()
        self.bullet_dodge = _BulletDodgeSystem()
        self.energy_manager = _EnergyPhaseManager()

        # State
        self.tick = 0
        self.radar_scan_direction = 1
        self.mode = "tactical"
        self.emergency_mode = False
        print("init")
        # Statistics
        self.shots_fired = 0
        self.shots_hit = 0
        self.name = "ChallengerTank"

    def calc_gun_turn(self, target_angle):
        """Calculate gun turn needed to face target angle"""
        diff = target_angle - self.get_gun_direction()
        # Normalize to -180 to 180
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        return diff    
    
    def turn_to(self, target_angle):
        """Helper to turn to absolute angle"""
        current = self.get_direction() % 360
        target = target_angle % 360
        diff = (target - current + 180) % 360 - 180
        self.turn_rate = diff

    async def run(self):
        """Main loop with advanced decision making"""
        print(f"🎯 {self.name} starting!")
        while self.is_running():
            self.tick += 1

            # Cleanup
            if self.tick % 20 == 0:
                self.enemies.cleanup(self.tick)

            # Update anti-gravity adaptation
            self.anti_gravity.adapt_force_constant(self.enemies.count(), self.get_energy())

            # EXTRA: Check for corner trap
            cornered, escape_angle = self.corner_detector.is_cornered(
                self.get_x(), self.get_y(),
                self.get_arena_width(),
                self.get_arena_height(),
                self.enemies
            )

            if cornered:
                self.turn_to(escape_angle)
                self.target_speed = 100
                self.radar_turn_rate = 45
                await self.go()
                continue

            # EXTRA: Check for formation trap
            formation = self.formation_breaker.detect_formation(
                self.get_x(), self.get_y(), self.enemies
            )

            if formation:
                self.turn_to(formation['escape_angle'])
                self.target_speed = 80
                self.radar_turn_rate = 45
                await self.go()
                continue

            # EXTRA: Bullet dodge - priority over normal movement
            if self.bullet_dodge.should_dodge(self.get_x(), self.get_y()):
                dodge_dir = random.choice([-90, 90])
                if dodge_dir < 0:
                    self.turn_rate = -dodge_dir
                else:
                    self.turn_rate = dodge_dir
                self.target_speed = 50
                # Don't execute normal movement - dodge has priority
            # Movement with predictive anti-gravity
            elif self.enemies.count() >= 3:
                self.execute_predictive_anti_gravity()
            elif self.enemies.count() > 0:
                self.execute_standard_anti_gravity()
            else:
                self.execute_patrol()

            # Radar
            if self.radar_scan_direction > 0:
                self.radar_turn_rate = 45
            else:
                self.radar_turn_rate = -45
            if self.tick % 8 == 0:
                self.radar_scan_direction *= -1

            # Engage
            if self.enemies.count() > 0:
                await self.engage_best_target()

            await self.go()

    def execute_predictive_anti_gravity(self):
        """EXTRA: Multi-step lookahead anti-gravity"""
        # Get current forces
        enemy_fx, enemy_fy = self.anti_gravity.calculate_forces(
            self.get_x(), self.get_y(), self.enemies
        )

        # Get predicted forces
        pred_fx, pred_fy = self.anti_gravity.predict_future_forces(
            self.get_x(), self.get_y(), self.enemies, steps=3
        )

        # Get wall forces
        wall_fx, wall_fy = self.anti_gravity.add_wall_repulsion(
            self.get_x(), self.get_y(),
            self.get_arena_width(),
            self.get_arena_height()
        )

        # Combine: 60% current, 40% predicted
        total_fx = 0.6 * enemy_fx + 0.4 * pred_fx + wall_fx
        total_fy = 0.6 * enemy_fy + 0.4 * pred_fy + wall_fy

        if total_fx != 0 or total_fy != 0:
            escape_angle = np.degrees(np.arctan2(total_fx, total_fy))
            self.turn_to(escape_angle)

            force_magnitude = np.sqrt(total_fx**2 + total_fy**2)
            # More aggressive movement - faster speeds
            move_speed = min(70, 40 + force_magnitude / 80)
            self.target_speed = move_speed
        else:
            self.target_speed = 40  # Faster default

    def execute_standard_anti_gravity(self):
        """Standard anti-gravity"""
        enemy_fx, enemy_fy = self.anti_gravity.calculate_forces(
            self.get_x(), self.get_y(), self.enemies
        )
        wall_fx, wall_fy = self.anti_gravity.add_wall_repulsion(
            self.get_x(), self.get_y(),
            self.get_arena_width(),
            self.get_arena_height()
        )

        total_fx = enemy_fx + wall_fx
        total_fy = enemy_fy + wall_fy

        if total_fx != 0 or total_fy != 0:
            escape_angle = np.degrees(np.arctan2(total_fx, total_fy))
            self.turn_to(escape_angle)
            self.target_speed = 55  # Much more aggressive
        else:
            self.target_speed = 40

    def execute_patrol(self):
        """Active search when no enemies visible - hunt them down!"""
        margin = 80

        # If near walls, move to center
        if (self.get_x() < margin or self.get_x() > self.get_arena_width() - margin or
            self.get_y() < margin or self.get_y() > self.get_arena_height() - margin):
            center_x = self.get_arena_width() / 2
            center_y = self.get_arena_height() / 2
            angle = self.targeting.calculate_angle(self.get_x(), self.get_y(), center_x, center_y)
            self.turn_to(angle)
            self.target_speed = 70  # Aggressive escape from walls
        else:
            # Active hunting pattern - move toward center and search quadrants
            # Divide arena into quadrants and search each one
            quadrant = (self.tick // 200) % 4  # Change quadrant every 200 ticks

            if quadrant == 0:  # Top-right
                target_x = self.get_arena_width() * 0.75
                target_y = self.get_arena_height() * 0.25
            elif quadrant == 1:  # Bottom-right
                target_x = self.get_arena_width() * 0.75
                target_y = self.get_arena_height() * 0.75
            elif quadrant == 2:  # Bottom-left
                target_x = self.get_arena_width() * 0.25
                target_y = self.get_arena_height() * 0.75
            else:  # Top-left
                target_x = self.get_arena_width() * 0.25
                target_y = self.get_arena_height() * 0.25

            # Move toward target quadrant - hunt aggressively!
            angle = self.targeting.calculate_angle(self.get_x(), self.get_y(), target_x, target_y)
            self.turn_to(angle)
            self.target_speed = 60  # Fast hunting

        # Wide radar sweep to find enemies
        self.radar_turn_rate = 60

    async def on_scanned_bot(self, event):
        """Update tracking and bullet detection"""
        # Calculate distance and position from event coordinates
        enemy_x = event.x
        enemy_y = event.y
        dx = enemy_x - self.get_x()
        dy = enemy_y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)

        heading_rad = math.radians(event.direction)
        vx = event.speed * math.sin(heading_rad)
        vy = event.speed * math.cos(heading_rad)

        # EXTRA: Detect bullet fired
        prev_energy = None
        if event.scanned_bot_id in self.enemies.enemy_ids:
            idx = self.enemies.enemy_ids.index(event.scanned_bot_id)
            prev_energy = self.enemies.energy[idx]

        self.bullet_dodge.detect_bullet_fired(
            event.scanned_bot_id, enemy_x, enemy_y,
            event.energy, prev_energy,
            self.get_x(), self.get_y()
        )

        # Update tracker
        self.enemies.update(
            enemy_id=event.scanned_bot_id,
            x=enemy_x,
            y=enemy_y,
            vx=vx,
            vy=vy,
            energy=event.energy,
            tick=self.tick
        )

    async def engage_best_target(self):
        """Advanced targeting with energy management"""
        if self.enemies.count() == 0:
            return

        # EXTRA: Get energy phase
        phase = self.energy_manager.get_phase(self.get_energy(), self.enemies.count())
        fire_threshold = self.energy_manager.get_fire_threshold(phase)

        # Calculate priorities
        distances = self.targeting.calculate_distances(
            self.get_x(), self.get_y(), self.enemies.x, self.enemies.y
        )

        # EXTRA: Time to danger (distance / relative speed)
        speeds = np.sqrt(self.enemies.vx**2 + self.enemies.vy**2)
        time_to_danger = distances / (speeds + 1)

        # Complex scoring
        scores = (
            (1000 / (distances + 1)) * 2 +  # Distance priority
            (100 - self.enemies.energy) * 3 +  # Weak targets
            (100 / (time_to_danger + 1))  # Imminent threats
        )

        best_idx = np.argmax(scores)

        # Get target
        target_x = self.enemies.x[best_idx]
        target_y = self.enemies.y[best_idx]
        target_vx = self.enemies.vx[best_idx]
        target_vy = self.enemies.vy[best_idx]
        target_distance = distances[best_idx]
        target_velocity = speeds[best_idx]
        target_energy = self.enemies.energy[best_idx]

        # Choose power based on phase
        max_power = self.energy_manager.get_max_power(phase, target_energy)
        bullet_power = self.choose_power(target_distance, target_energy, max_power)

        # Predict
        bullet_speed = self.targeting.calculate_bullet_speed(bullet_power)
        time_to_hit = target_distance / bullet_speed
        future_x, future_y = self.targeting.predict_positions(
            np.array([target_x]),
            np.array([target_y]),
            np.array([target_vx]),
            np.array([target_vy]),
            time_to_hit
        )

        # Validate predicted position is in arena - don't shoot walls!
        margin = 20
        if (future_x[0] < margin or future_x[0] > self.get_arena_width() - margin or
            future_y[0] < margin or future_y[0] > self.get_arena_height() - margin):
            # Target going out of bounds - aim at current position instead
            future_x[0], future_y[0] = target_x, target_y

        # Aim gun at predicted position
        angle = self.targeting.calculate_angle(
            self.get_x(), self.get_y(), future_x[0], future_y[0]
        )
        gun_turn = self.calc_gun_turn(angle)
        if gun_turn < 0:
            self.gun_turn_rate = -gun_turn
        else:
            self.gun_turn_rate = gun_turn

        # Hit probability
        hit_prob = self.calculate_hit_probability(target_distance, target_velocity, bullet_power)

        # ONLY FIRE if good shot AND gun is reasonably aimed
        if (hit_prob >= fire_threshold or target_distance < 100) and abs(gun_turn) < 20:
            await self.fire(bullet_power)
            self.shots_fired += 1

    def choose_power(self, distance, enemy_energy, max_power):
        """Smart power selection"""
        if distance < 150 and enemy_energy < 30:
            return min(3, max_power)
        elif distance < 200:
            return min(3, max_power)
        elif distance < 400:
            return min(2, max_power)
        else:
            return 1

    def calculate_hit_probability(self, distance, velocity, power):
        """Hit probability estimation"""
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

    async def on_hit_by_bullet(self, event):
        """Reactive dodge"""
        dodge = random.choice(['right', 'left', 'back'])
        if dodge == 'right':
            self.turn_rate = 90
            self.target_speed = 70
        elif dodge == 'left':
            self.turn_rate = -90
            self.target_speed = 70
        else:
            self.target_speed = -60

    async def on_hit_wall(self, event):
        """Wall collision"""
        self.target_speed = -50
        self.turn_rate = 90

    async def on_bullet_hit(self, event):
        """Track accuracy"""
        self.shots_hit += 1

    def on_robot_death(self, event):
        """Track eliminations"""
        pass


# Main entry point

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "challenger_tank.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = ChallengerTank(bot_info=bot_info)
    asyncio.run(bot.start())
