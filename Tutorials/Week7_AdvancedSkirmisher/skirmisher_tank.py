"""
Skirmisher Tank - Handles multiple enemies efficiently
Week 7: Advanced Skirmisher - Data Structures and NumPy

This tank demonstrates:
- Data structures for tracking multiple enemies
- NumPy arrays for fast calculations
- Matrix operations for processing all enemies at once
- Smart target selection algorithms
- Efficient memory usage

Perfect for battle royale scenarios with 10+ enemies!
"""
import numpy as np
import math
import random


class TargetingSystem:
    """
    Fast math utilities using NumPy for vectorized operations
    
    Instead of calculating one enemy at a time, we calculate
    ALL enemies simultaneously using NumPy arrays!
    """
    
    def calculate_distances(self, my_x, my_y, enemy_x, enemy_y):
        """
        Calculate distance to ALL enemies at once
        
        This is much faster than looping through enemies!
        """
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angles(self, my_x, my_y, enemy_x, enemy_y):
        """Calculate angle to ALL enemies at once"""
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.degrees(np.arctan2(x_diff, y_diff))
    
    def predict_positions(self, x, y, vx, vy, time):
        """
        Predict future position of ALL enemies at once
        
        x, y: Current positions (arrays)
        vx, vy: Velocities (arrays)
        time: Time steps to predict forward
        """
        future_x = x + vx * time
        future_y = y + vy * time
        return future_x, future_y
    
    def calculate_bullet_speed(self, power):
        """Calculate bullet speed based on power"""
        return 20 - 3 * power


class EnemyTracker:
    """
    Track multiple enemies efficiently using parallel NumPy arrays
    
    Think of this like a spreadsheet:
    Row 1: Enemy1 -> x=100, y=200, vx=3, vy=2, energy=100
    Row 2: Enemy2 -> x=300, y=400, vx=-2, vy=1, energy=80
    Row 3: Enemy3 -> x=500, y=100, vx=0, vy=-3, energy=50
    
    But stored as columns (arrays) for fast math!
    """
    
    def __init__(self, max_enemies=50):
        """Initialize empty tracking arrays"""
        self.max_enemies = max_enemies
        
        # Each array holds one property for ALL enemies
        self.enemy_ids = []  # Names/IDs (can't vectorize strings easily)
        self.x = np.array([])  # X positions
        self.y = np.array([])  # Y positions
        self.vx = np.array([])  # X velocities
        self.vy = np.array([])  # Y velocities
        self.energy = np.array([])  # Health
        self.last_seen = np.array([])  # Last update tick
    
    def update(self, enemy_id, x, y, vx, vy, energy, tick):
        """
        Add or update an enemy in our tracking system
        
        If enemy exists: update their data
        If enemy is new: add them to our arrays
        """
        if enemy_id in self.enemy_ids:
            # Update existing enemy
            idx = self.enemy_ids.index(enemy_id)
            self.x[idx] = x
            self.y[idx] = y
            self.vx[idx] = vx
            self.vy[idx] = vy
            self.energy[idx] = energy
            self.last_seen[idx] = tick
        else:
            # Add new enemy (if not at max)
            if len(self.enemy_ids) < self.max_enemies:
                self.enemy_ids.append(enemy_id)
                self.x = np.append(self.x, x)
                self.y = np.append(self.y, y)
                self.vx = np.append(self.vx, vx)
                self.vy = np.append(self.vy, vy)
                self.energy = np.append(self.energy, energy)
                self.last_seen = np.append(self.last_seen, tick)
    
    def cleanup(self, current_tick, max_age=100):
        """
        Remove enemies we haven't seen recently
        
        This prevents tracking destroyed or distant enemies
        """
        if len(self.enemy_ids) == 0:
            return
        
        # Calculate age of each enemy's data
        age = current_tick - self.last_seen
        keep = age < max_age
        
        # If nothing to keep, reset
        if not np.any(keep):
            self.__init__(self.max_enemies)
            return
        
        # Keep only fresh data
        keep_idx = np.where(keep)[0]
        self.enemy_ids = [self.enemy_ids[i] for i in keep_idx]
        self.x = self.x[keep]
        self.y = self.y[keep]
        self.vx = self.vx[keep]
        self.vy = self.vy[keep]
        self.energy = self.energy[keep]
        self.last_seen = self.last_seen[keep]
    
    def count(self):
        """Return number of tracked enemies"""
        return len(self.enemy_ids)
    
    def get_positions(self):
        """Get all enemy positions as arrays"""
        return self.x.copy(), self.y.copy()


class TargetSelector:
    """
    Choose the best enemy to shoot at from many options
    
    Considers multiple factors:
    - Distance (closer is better)
    - Energy (weaker is better for easy kills)
    - Hit probability (don't waste shots)
    - Threat level (who's most dangerous)
    """
    
    def __init__(self):
        self.targeting = TargetingSystem()
    
    def calculate_hit_probabilities(self, my_x, my_y, tracker):
        """
        Estimate hit probability for ALL enemies
        
        Close + slow = high probability
        Far + fast = low probability
        """
        if tracker.count() == 0:
            return np.array([])
        
        # Get distances to all enemies
        distances = self.targeting.calculate_distances(
            my_x, my_y, tracker.x, tracker.y
        )
        
        # Calculate speed for all enemies
        speeds = np.sqrt(tracker.vx**2 + tracker.vy**2)
        
        # Probability factors
        distance_factor = 1.0 / (1.0 + distances / 100)
        speed_factor = 1.0 / (1.0 + speeds / 5)
        
        # Combined probability
        probabilities = distance_factor * speed_factor
        
        return probabilities
    
    def calculate_threat_scores(self, my_x, my_y, tracker):
        """
        Calculate how dangerous each enemy is to us
        
        Close + strong = very threatening
        """
        if tracker.count() == 0:
            return np.array([])
        
        distances = self.targeting.calculate_distances(
            my_x, my_y, tracker.x, tracker.y
        )
        
        # Closer = more threatening
        distance_threat = 1000 / (distances + 1)
        
        # More energy = more threatening
        energy_threat = tracker.energy / 10
        
        return distance_threat + energy_threat
    
    def select_best_target(self, my_x, my_y, tracker):
        """
        Choose the single best enemy to shoot at
        
        Uses a scoring system that balances:
        - Opportunity (weak enemies)
        - Threat (dangerous enemies)
        - Hit chance (likely to hit)
        """
        if tracker.count() == 0:
            return None
        
        # Calculate all factors for ALL enemies at once
        distances = self.targeting.calculate_distances(
            my_x, my_y, tracker.x, tracker.y
        )
        hit_probs = self.calculate_hit_probabilities(my_x, my_y, tracker)
        threats = self.calculate_threat_scores(my_x, my_y, tracker)
        
        # Calculate target priority scores
        scores = np.zeros(tracker.count())
        
        # Prefer close targets
        scores += (1000 / (distances + 1))
        
        # Prefer weak targets (easy kills)
        scores += (100 - tracker.energy) * 2
        
        # Prefer high hit probability
        scores += hit_probs * 150
        
        # Prefer threatening targets
        scores += threats * 0.5
        
        # Find best target
        best_idx = np.argmax(scores)
        
        return {
            "index": best_idx,
            "id": tracker.enemy_ids[best_idx],
            "x": tracker.x[best_idx],
            "y": tracker.y[best_idx],
            "vx": tracker.vx[best_idx],
            "vy": tracker.vy[best_idx],
            "energy": tracker.energy[best_idx],
            "distance": distances[best_idx],
            "hit_probability": hit_probs[best_idx],
            "threat": threats[best_idx],
            "score": scores[best_idx]
        }


class SkirmisherTank:
    """
    Advanced tank optimized for multi-enemy battles
    
    Uses data structures and NumPy for efficient tracking
    and targeting of many enemies simultaneously.
    
    Key Features:
    - Tracks up to 50 enemies at once
    - Vectorized math for speed
    - Smart target selection
    - Threat assessment
    - Resource management
    """
    
    def __init__(self):
        self.name = "SkirmisherTank"
        
        # Enemy tracking system
        self.enemies = EnemyTracker(max_enemies=50)
        
        # Targeting utilities
        self.targeting = TargetingSystem()
        self.target_selector = TargetSelector()
        
        # State tracking
        self.tick = 0
        self.radar_direction = 1
        
        # Statistics
        self.shots_fired = 0
        self.enemies_tracked_max = 0
    
    def run(self):
        """
        Main loop - runs every game tick
        """
        self.tick += 1
        
        # Periodic cleanup of old enemy data
        if self.tick % 20 == 0:
            self.enemies.cleanup(self.tick, max_age=100)
            
            # Track statistics
            current_count = self.enemies.count()
            if current_count > self.enemies_tracked_max:
                self.enemies_tracked_max = current_count
        
        # Movement - wall avoidance
        self.move_with_wall_avoidance()
        
        # Radar - sweep to find enemies
        self.sweep_radar()
        
        # If we have tracked enemies, engage the best one
        if self.enemies.count() > 0:
            self.engage_best_target()
    
    def move_with_wall_avoidance(self):
        """
        Move around the battlefield avoiding walls
        
        Simple but effective movement strategy
        """
        margin = 80
        
        # Check if near walls
        if self.x < margin:
            self.turn_right(90)
        elif self.x > self.battlefield_width - margin:
            self.turn_left(90)
        elif self.y < margin:
            self.turn_right(90)
        elif self.y > self.battlefield_height - margin:
            self.turn_left(90)
        
        # Add some randomness for unpredictability
        if self.tick % 30 == 0:
            self.turn_right(random.randint(-30, 30))
        
        # Move forward
        self.ahead(20)
    
    def sweep_radar(self):
        """
        Sweep radar back and forth to find enemies
        
        More efficient than spinning in circles
        """
        self.turn_radar_right(self.radar_direction * 45)
        
        # Reverse direction periodically
        if self.tick % 8 == 0:
            self.radar_direction *= -1
    
    def on_scanned_robot(self, scanned):
        """
        Called when radar detects an enemy
        
        Add or update enemy in our tracking system
        """
        # Convert heading and velocity to velocity components
        heading_rad = math.radians(scanned.heading)
        vx = scanned.velocity * math.sin(heading_rad)
        vy = scanned.velocity * math.cos(heading_rad)
        
        # Update tracker with this enemy's data
        self.enemies.update(
            enemy_id=scanned.name,
            x=scanned.x,
            y=scanned.y,
            vx=vx,
            vy=vy,
            energy=scanned.energy,
            tick=self.tick
        )
        
        # Print status occasionally
        if self.tick % 50 == 0:
            print(f"Tracking {self.enemies.count()} enemies (max: {self.enemies_tracked_max})")
    
    def engage_best_target(self):
        """
        Choose and shoot at the best target among all tracked enemies
        
        Uses sophisticated target selection algorithm
        """
        # Select best target
        target = self.target_selector.select_best_target(
            self.x, self.y, self.enemies
        )
        
        if target is None:
            return
        
        # Predict where target will be when bullet arrives
        bullet_power = self.choose_bullet_power(target["distance"], target["energy"])
        bullet_speed = self.targeting.calculate_bullet_speed(bullet_power)
        time_to_hit = target["distance"] / bullet_speed
        
        # Predict future position
        future_x, future_y = self.targeting.predict_positions(
            np.array([target["x"]]),
            np.array([target["y"]]),
            np.array([target["vx"]]),
            np.array([target["vy"]]),
            time_to_hit
        )
        
        # Calculate aim angle
        angle = self.targeting.calculate_angles(
            self.x, self.y, future_x, future_y
        )[0]
        
        # Aim gun
        self.turn_gun_to(angle)
        
        # Fire if we have a good shot
        if self.should_fire(target):
            self.fire(bullet_power)
            self.shots_fired += 1
    
    def choose_bullet_power(self, distance, enemy_energy):
        """
        Choose appropriate bullet power based on situation
        
        Close + weak = high power (finish them!)
        Far + strong = low power (conserve energy)
        """
        # Very close and weak - finish them!
        if distance < 150 and enemy_energy < 30:
            return 3
        
        # Close range - use power
        if distance < 200:
            return 3
        
        # Medium range - balanced
        if distance < 400:
            return 2
        
        # Long range - conserve energy
        return 1
    
    def should_fire(self, target):
        """
        Decide if we should take this shot
        
        Don't waste energy on bad shots!
        """
        # Don't shoot if low on energy
        if self.energy < 15:
            return False
        
        # Don't shoot if hit probability is too low
        if target["hit_probability"] < 0.2:
            return False
        
        # Don't waste shots on nearly dead enemies far away
        if target["energy"] < 10 and target["distance"] > 300:
            return False
        
        return True
    
    def on_hit_by_bullet(self, event):
        """
        React when we get hit
        
        Quick dodge to avoid follow-up shots
        """
        # Turn perpendicular to dodge
        self.turn_right(90)
        self.ahead(50)
    
    def on_hit_wall(self, event):
        """
        React when we hit a wall
        
        Back up and turn around
        """
        self.back(50)
        self.turn_right(90)
    
    def on_bullet_hit(self, event):
        """Track successful hits"""
        # Could track accuracy here
        pass
    
    def on_robot_death(self, event):
        """
        Called when any robot dies
        
        We could remove them from tracking, but cleanup
        will handle it automatically
        """
        pass
