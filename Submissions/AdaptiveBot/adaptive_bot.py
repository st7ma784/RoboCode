"""
AdaptiveBot - Field-Based Movement with Predictive Shooting

This bot uses a sophisticated field-based movement system:
- Anti-gravity field to avoid enemies
- Wall repulsion field to stay away from boundaries
- Bullet track penalties to dodge incoming fire
- Evaluates reachable positions within 3 turns
- Rewards safe positions and penalizes dangerous ones
- Predictive shooting with hit probability calculation

Movement Strategy:
1. Generate field map covering arena
2. Apply enemy repulsion forces
3. Apply wall avoidance forces
4. Mark bullet trajectories as danger zones
5. Evaluate all positions within 3 turns of movement
6. Move toward highest-value safe position

Shooting Strategy:
- Predict enemy position based on velocity
- Calculate hit probability
- Only fire when probability > 40%
"""

from robocode_tank_royale.bot_api import Bot, BotInfo, Color
import math
import numpy as np


class FieldBasedMovement:
    """Calculates movement using field-based analysis"""
    
    def __init__(self):
        self.field_resolution = 20  # Grid squares per field
        self.max_move_distance = 8 * 3  # Max speed * 3 turns
        
    def create_field(self, width, height):
        """Create empty field grid"""
        w_cells = int(width / self.field_resolution)
        h_cells = int(height / self.field_resolution)
        return np.zeros((h_cells, w_cells))
    
    def add_enemy_repulsion(self, field, my_x, my_y, enemies_x, enemies_y, enemies_energy, width, height):
        """Add anti-gravity forces from enemies"""
        if len(enemies_x) == 0:
            return field
            
        h_cells, w_cells = field.shape
        
        for enemy_x, enemy_y, energy in zip(enemies_x, enemies_y, enemies_energy):
            # Calculate threat level based on energy
            threat = max(0.5, energy / 100)
            
            for i in range(h_cells):
                for j in range(w_cells):
                    cell_x = j * self.field_resolution + self.field_resolution / 2
                    cell_y = i * self.field_resolution + self.field_resolution / 2
                    
                    # Distance from this cell to enemy
                    dx = cell_x - enemy_x
                    dy = cell_y - enemy_y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    # Repulsion strength (inverse square with threat scaling)
                    if distance > 0:
                        repulsion = (threat * 5000) / (distance**2 + 100)
                        field[i, j] -= repulsion
        
        return field
    
    def add_wall_penalties(self, field, width, height, margin=50):
        """Penalize positions near walls"""
        h_cells, w_cells = field.shape
        
        for i in range(h_cells):
            for j in range(w_cells):
                cell_x = j * self.field_resolution + self.field_resolution / 2
                cell_y = i * self.field_resolution + self.field_resolution / 2
                
                # Distance to each wall
                dist_left = cell_x
                dist_right = width - cell_x
                dist_top = cell_y
                dist_bottom = height - cell_y
                
                min_wall_dist = min(dist_left, dist_right, dist_top, dist_bottom)
                
                # Heavy penalty if too close to wall
                if min_wall_dist < margin:
                    penalty = (margin - min_wall_dist) * 100
                    field[i, j] -= penalty
        
        return field
    
    def add_bullet_penalties(self, field, bullets, width, height):
        """Mark bullet trajectories as danger zones"""
        if len(bullets) == 0:
            return field
            
        h_cells, w_cells = field.shape
        
        for bullet in bullets:
            bx, by, heading, speed = bullet
            
            # Project bullet path for next 50 ticks
            heading_rad = math.radians(heading)
            for t in range(50):
                future_x = bx + speed * t * math.sin(heading_rad)
                future_y = by + speed * t * math.cos(heading_rad)
                
                # Check if still in arena
                if future_x < 0 or future_x >= width or future_y < 0 or future_y >= height:
                    break
                
                # Mark area around bullet path as dangerous
                cell_j = int(future_x / self.field_resolution)
                cell_i = int(future_y / self.field_resolution)
                
                if 0 <= cell_i < h_cells and 0 <= cell_j < w_cells:
                    # Penalty decreases over time
                    time_factor = max(0.3, 1 - t / 50)
                    field[cell_i, cell_j] -= 500 * time_factor
                    
                    # Also mark adjacent cells
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = cell_i + di, cell_j + dj
                            if 0 <= ni < h_cells and 0 <= nj < w_cells:
                                field[ni, nj] -= 250 * time_factor
        
        return field
    
    def find_best_reachable_position(self, field, my_x, my_y, my_direction, width, height):
        """Find best position reachable within 3 turns"""
        h_cells, w_cells = field.shape
        
        best_value = -float('inf')
        best_x = my_x
        best_y = my_y
        
        # Check positions within max move distance
        search_radius = self.max_move_distance
        
        for angle in range(0, 360, 15):  # Check every 15 degrees
            angle_rad = math.radians(angle)
            
            # Check multiple distances
            for distance in [search_radius * 0.3, search_radius * 0.6, search_radius]:
                test_x = my_x + distance * math.sin(angle_rad)
                test_y = my_y + distance * math.cos(angle_rad)
                
                # Check if position is in bounds
                if test_x < 20 or test_x >= width - 20 or test_y < 20 or test_y >= height - 20:
                    continue
                
                # Get field value at this position
                cell_j = int(test_x / self.field_resolution)
                cell_i = int(test_y / self.field_resolution)
                
                if 0 <= cell_i < h_cells and 0 <= cell_j < w_cells:
                    value = field[cell_i, cell_j]
                    
                    # Bonus for positions that maintain distance from current position
                    # (encourages movement, not sitting still)
                    movement_bonus = min(distance, 50) * 2
                    value += movement_bonus
                    
                    if value > best_value:
                        best_value = value
                        best_x = test_x
                        best_y = test_y
        
        return best_x, best_y, best_value


class PredictiveTargeting:
    """Predictive shooting with hit probability"""
    
    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """Calculate angle to target"""
        dx = to_x - from_x
        dy = to_y - from_y
        return math.degrees(math.atan2(dx, dy))
    
    def predict_position(self, x, y, vx, vy, time):
        """Predict future position"""
        future_x = x + vx * time
        future_y = y + vy * time
        return future_x, future_y
    
    def calculate_hit_probability(self, distance, velocity, power):
        """Estimate probability of hitting target"""
        bullet_speed = 20 - 3 * power
        time_to_hit = distance / bullet_speed
        
        # Target will move this far
        potential_miss = velocity * time_to_hit
        
        # Hit probability decreases with distance and target speed
        base_prob = 1.0
        distance_factor = max(0, 1 - distance / 800)
        speed_factor = max(0, 1 - potential_miss / 100)
        
        return base_prob * distance_factor * speed_factor
    
    def is_valid_target(self, x, y, width, height, margin=30):
        """Check if predicted position is in arena"""
        return margin < x < width - margin and margin < y < height - margin


class BulletTracker:
    """Track detected bullets"""
    
    def __init__(self):
        self.bullets = []  # List of (x, y, heading, speed)
    
    def detect_from_enemy_energy(self, enemy_id, enemy_x, enemy_y, current_energy, prev_energy):
        """Detect bullet fired based on energy drop"""
        if prev_energy is None:
            return
        
        energy_drop = prev_energy - current_energy
        
        # Energy drop between 0.1 and 3.0 indicates a bullet fired
        if 0.1 <= energy_drop <= 3.0:
            # Estimate bullet heading (toward us is most dangerous)
            # We'll mark this area as dangerous in the field
            power = energy_drop
            speed = 20 - 3 * power
            
            # For simplicity, we'll add this in the update method
            # Store as a potential bullet track
            pass
    
    def add_bullet(self, x, y, heading, speed):
        """Add detected bullet"""
        self.bullets.append((x, y, heading, speed))
    
    def update(self, current_tick):
        """Update bullet positions (simple tracking)"""
        # For now, keep bullets for a limited time
        # More sophisticated: update positions and remove when they hit walls
        if len(self.bullets) > 10:
            self.bullets = self.bullets[-10:]
    
    def get_active_bullets(self):
        """Get list of active bullets"""
        return self.bullets


class AdaptiveBot(Bot):
    """Field-based adaptive bot with predictive shooting"""
    
    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        
        # Set independence flags - gun and radar move independently from body
        self.set_adjust_gun_for_body_turn(True)
        self.set_adjust_radar_for_body_turn(True)
        self.set_adjust_radar_for_gun_turn(True)
        
        self.movement = FieldBasedMovement()
        self.targeting = PredictiveTargeting()
        self.bullet_tracker = BulletTracker()
        
        # Enemy tracking
        self.enemies = {}  # id -> {'x', 'y', 'vx', 'vy', 'energy', 'prev_energy'}
        
        # Movement state
        self.target_position = None
        self.ticks = 0
        
    async def run(self):
        """Main loop"""
        while self.is_running():
            self.ticks += 1
            
            # Update bullet tracker
            self.bullet_tracker.update(self.ticks)
            
            # Create field and evaluate positions
            field = self.movement.create_field(self.get_arena_width(), self.get_arena_height())
            
            # Get enemy data
            enemies_x = [e['x'] for e in self.enemies.values()]
            enemies_y = [e['y'] for e in self.enemies.values()]
            enemies_energy = [e['energy'] for e in self.enemies.values()]
            
            # Apply forces to field
            field = self.movement.add_enemy_repulsion(
                field, self.get_x(), self.get_y(),
                enemies_x, enemies_y, enemies_energy,
                self.get_arena_width(), self.get_arena_height()
            )
            
            field = self.movement.add_wall_penalties(
                field, self.get_arena_width(), self.get_arena_height()
            )
            
            field = self.movement.add_bullet_penalties(
                field, self.bullet_tracker.get_active_bullets(),
                self.get_arena_width(), self.get_arena_height()
            )
            
            # Find best reachable position
            best_x, best_y, value = self.movement.find_best_reachable_position(
                field, self.get_x(), self.get_y(), self.get_direction(),
                self.get_arena_width(), self.get_arena_height()
            )
            
            # Move toward best position
            angle_to_target = self.targeting.calculate_angle(
                self.get_x(), self.get_y(), best_x, best_y
            )
            
            # Turn toward target angle
            turn_amount = angle_to_target - self.get_direction()
            while turn_amount > 180:
                turn_amount -= 360
            while turn_amount < -180:
                turn_amount += 360
            
            if turn_amount < 0:
                self.turn_left(abs(turn_amount))
            else:
                self.turn_right(turn_amount)
            
            # Set speed based on field value
            if value > 0:
                self.forward(8)  # Full speed to good position
            elif value > -500:
                self.forward(5)  # Moderate speed
            else:
                self.forward(8)  # Fast escape from danger
            
            # Radar sweep
            if self.ticks % 10 == 0:
                self.turn_radar_left(45)
            else:
                self.turn_radar_right(45)
            
            # Engage targets
            if len(self.enemies) > 0:
                self.engage_best_target()
            
            await self.go()
    
    def engage_best_target(self):
        """Find and shoot at best target"""
        best_target = None
        best_score = -float('inf')
        
        # Find best target (closest with lowest energy)
        for enemy_id, enemy in self.enemies.items():
            dx = enemy['x'] - self.get_x()
            dy = enemy['y'] - self.get_y()
            distance = math.sqrt(dx**2 + dy**2)
            
            # Score: closer and weaker enemies are better
            score = (1000 / (distance + 1)) + (100 - enemy['energy'])
            
            if score > best_score:
                best_score = score
                best_target = enemy
        
        if best_target is None:
            return
        
        # Calculate distance and velocity
        dx = best_target['x'] - self.get_x()
        dy = best_target['y'] - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)
        
        vx = best_target.get('vx', 0)
        vy = best_target.get('vy', 0)
        velocity = math.sqrt(vx**2 + vy**2)
        
        # Choose power based on distance
        if distance < 200:
            power = 3
        elif distance < 400:
            power = 2
        else:
            power = 1
        
        # Predict position
        bullet_speed = 20 - 3 * power
        time_to_hit = distance / bullet_speed if bullet_speed > 0 else 1
        
        future_x, future_y = self.targeting.predict_position(
            best_target['x'], best_target['y'],
            vx, vy, time_to_hit
        )
        
        # Validate target
        if not self.targeting.is_valid_target(
            future_x, future_y,
            self.get_arena_width(), self.get_arena_height()
        ):
            future_x, future_y = best_target['x'], best_target['y']
        
        # Calculate hit probability
        hit_prob = self.targeting.calculate_hit_probability(distance, velocity, power)
        
        # Only shoot if reasonable chance
        if hit_prob > 0.4 or distance < 150:
            angle = self.targeting.calculate_angle(
                self.get_x(), self.get_y(), future_x, future_y
            )
            
            # Aim gun
            gun_turn = angle - self.get_gun_direction()
            while gun_turn > 180:
                gun_turn -= 360
            while gun_turn < -180:
                gun_turn += 360
            
            if gun_turn < 0:
                self.turn_gun_left(abs(gun_turn))
            else:
                self.turn_gun_right(gun_turn)
            
            # Fire if gun is roughly aimed
            if abs(gun_turn) < 5:
                self.fire(power)
    
    async def on_scanned_bot(self, event):
        """Track enemy position and velocity"""
        enemy_id = event.scanned_bot_id
        
        # Get position
        enemy_x = event.x
        enemy_y = event.y
        
        # Calculate velocity components
        heading_rad = math.radians(event.direction)
        vx = event.speed * math.sin(heading_rad)
        vy = event.speed * math.cos(heading_rad)
        
        # Detect bullet firing
        if enemy_id in self.enemies:
            prev_energy = self.enemies[enemy_id]['energy']
            energy_drop = prev_energy - event.energy
            
            # Bullet fired!
            if 0.1 <= energy_drop <= 3.0:
                # Calculate angle from enemy to us (approximate bullet heading)
                angle_to_us = self.targeting.calculate_angle(
                    enemy_x, enemy_y, self.get_x(), self.get_y()
                )
                bullet_speed = 20 - 3 * energy_drop
                
                # Add bullet to tracker
                self.bullet_tracker.add_bullet(
                    enemy_x, enemy_y, angle_to_us, bullet_speed
                )
        
        # Update enemy data
        self.enemies[enemy_id] = {
            'x': enemy_x,
            'y': enemy_y,
            'vx': vx,
            'vy': vy,
            'energy': event.energy,
            'prev_energy': self.enemies.get(enemy_id, {}).get('energy', event.energy)
        }
    
    async def on_hit_by_bullet(self, event):
        """React to being hit"""
        # Emergency dodge - move perpendicular
        current_dir = self.get_direction()
        dodge_angle = current_dir + 90 if self.ticks % 2 == 0 else current_dir - 90
        
        turn_amount = dodge_angle - current_dir
        while turn_amount > 180:
            turn_amount -= 360
        while turn_amount < -180:
            turn_amount += 360
        
        if turn_amount < 0:
            self.turn_left(abs(turn_amount))
        else:
            self.turn_right(turn_amount)
        self.forward(8)
    
    async def on_bot_death(self, event):
        """Remove dead bot from tracking"""
        victim_id = event.victim_id
        if victim_id in self.enemies:
            del self.enemies[victim_id]
    
    async def on_win(self, event):
        """Victory!"""
        print("🏆 AdaptiveBot wins!")


if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "adaptive_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = AdaptiveBot(bot_info=bot_info)
    asyncio.run(bot.start())
