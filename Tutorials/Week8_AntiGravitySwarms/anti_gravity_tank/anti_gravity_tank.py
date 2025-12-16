"""
Anti-Gravity Tank - Advanced movement with cluster awareness
Week 8: Anti-Gravity & Swarm Intelligence

This tank demonstrates:
- Physics-based anti-gravity movement
- Repulsive forces from enemies
- Cluster detection and analysis
- Smart force weighting
- Formation recognition

Perfect for escaping from enemy swarms!
"""
from robocode_tank_royale.bot_api import Bot, BotInfo
import numpy as np
import math


class TargetingSystem:
    """Math utilities for targeting"""
    
    def calculate_distances(self, my_x, my_y, enemy_x, enemy_y):
        """Calculate distance to ALL enemies at once"""
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angles(self, my_x, my_y, enemy_x, enemy_y):
        """Calculate angle to ALL enemies at once"""
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.degrees(np.arctan2(x_diff, y_diff))


class EnemyTracker:
    """
    Track multiple enemies efficiently using NumPy arrays
    """
    
    def __init__(self):
        self.enemy_ids = []
        self.get_x() = np.array([])
        self.get_y() = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])
        self.get_energy() = np.array([])
        self.last_seen = np.array([])
    
    def update(self, enemy_id, x, y, vx, vy, energy, tick):
        """Add or update enemy"""
        if enemy_id in self.enemy_ids:
            idx = self.enemy_ids.index(enemy_id)
            self.get_x()[idx] = x
            self.get_y()[idx] = y
            self.vx[idx] = vx
            self.vy[idx] = vy
            self.get_energy()[idx] = energy
            self.last_seen[idx] = tick
        else:
            self.enemy_ids.append(enemy_id)
            self.get_x() = np.append(self.get_x(), x)
            self.get_y() = np.append(self.get_y(), y)
            self.vx = np.append(self.vx, vx)
            self.vy = np.append(self.vy, vy)
            self.get_energy() = np.append(self.get_energy(), energy)
            self.last_seen = np.append(self.last_seen, tick)
    
    def cleanup(self, current_tick, max_age=100):
        """Remove old enemy data"""
        if len(self.enemy_ids) == 0:
            return
        
        age = current_tick - self.last_seen
        keep = age < max_age
        
        if not np.any(keep):
            self.__init__()
            return
        
        keep_idx = np.where(keep)[0]
        self.enemy_ids = [self.enemy_ids[i] for i in keep_idx]
        self.get_x() = self.get_x()[keep]
        self.get_y() = self.get_y()[keep]
        self.vx = self.vx[keep]
        self.vy = self.vy[keep]
        self.get_energy() = self.get_energy()[keep]
        self.last_seen = self.last_seen[keep]
    
    def count(self):
        """Number of tracked enemies"""
        return len(self.enemy_ids)


class AntiGravityMovement:
    """
    Movement strategy using repulsive forces from enemies
    
    Think of each enemy as a magnet that pushes you away.
    Close enemies push harder than far enemies.
    All forces combine to find the safest direction!
    """
    
    def __init__(self, force_constant=1200):
        """
        Initialize anti-gravity system
        
        force_constant: How strong the repulsion is (higher = stronger push)
        """
        self.force_constant = force_constant
    
    def calculate_forces(self, my_x, my_y, tracker):
        """
        Calculate anti-gravity forces from all enemies
        
        Returns (force_x, force_y) - the combined push direction
        """
        if tracker.count() == 0:
            return 0, 0
        
        # Calculate directions to each enemy
        dx = tracker.x - my_x
        dy = tracker.y - my_y
        
        # Calculate distances to each enemy
        distances = np.sqrt(dx**2 + dy**2)
        
        # Weight forces by enemy threat (stronger enemies push harder)
        threat_weights = tracker.energy / 100
        
        # Calculate force strength: closer = stronger push
        # We use 1/distance so nearby enemies dominate
        force_strengths = self.force_constant * threat_weights / (distances + 1)
        
        # Calculate force components
        # Negative because we want to move AWAY from enemies
        force_x = -np.sum((dx / (distances + 1)) * force_strengths)
        force_y = -np.sum((dy / (distances + 1)) * force_strengths)
        
        return force_x, force_y
    
    def add_wall_repulsion(self, my_x, my_y, battlefield_width, battlefield_height):
        """
        Add repulsive forces from walls to avoid collisions
        
        Returns (force_x, force_y) from wall repulsion
        """
        margin = 80
        fx = 0
        fy = 0
        
        # Left/right walls
        if my_x < margin:
            # Push right when near left wall
            fx = 500 * (margin - my_x) / margin
        elif my_x > battlefield_width - margin:
            # Push left when near right wall
            fx = -500 * (my_x - (battlefield_width - margin)) / margin
        
        # Top/bottom walls
        if my_y < margin:
            # Push down when near top wall
            fy = 500 * (margin - my_y) / margin
        elif my_y > battlefield_height - margin:
            # Push up when near bottom wall
            fy = -500 * (my_y - (battlefield_height - margin)) / margin
        
        return fx, fy
    
    def move(self, tank, tracker):
        """
        Apply anti-gravity movement to the tank
        
        Calculates total forces and moves in safest direction
        """
        # Get repulsion from enemies
        enemy_fx, enemy_fy = self.calculate_forces(tank.x, tank.y, tracker)
        
        # Get repulsion from walls
        wall_fx, wall_fy = self.add_wall_repulsion(
            tank.x, tank.y,
            tank.arena_width,
            tank.arena_height
        )
        
        # Combine all forces
        total_fx = enemy_fx + wall_fx
        total_fy = enemy_fy + wall_fy
        
        # Convert forces to movement
        if total_fx != 0 or total_fy != 0:
            # Calculate escape angle
            escape_angle = np.degrees(np.arctan2(total_fx, total_fy))
            
            # Turn toward escape direction
            tank.turn_to(escape_angle)
            
            # Move faster when in danger (high forces)
            force_magnitude = np.sqrt(total_fx**2 + total_fy**2)
            move_speed = min(40, 20 + force_magnitude / 100)
            
            tank.forward(move_speed)
        else:
            # No forces, move normally
            tank.forward(20)


class ClusterDetector:
    """
    Detect and analyze groups of enemies that are close together
    
    Clusters are dangerous because multiple enemies can
    attack from similar directions!
    """
    
    def find_clusters(self, tracker, cluster_distance=150):
        """
        Find groups of enemies within cluster_distance of each other
        
        Returns list of clusters (each cluster is a list of enemy indices)
        """
        if tracker.count() < 2:
            return []
        
        clusters = []
        clustered = set()
        
        # Check each enemy
        for i in range(tracker.count()):
            if i in clustered:
                continue  # Already in a cluster
            
            # Start new cluster with this enemy
            cluster = [i]
            clustered.add(i)
            
            # Find all enemies close to this one
            for j in range(i + 1, tracker.count()):
                if j in clustered:
                    continue
                
                # Calculate distance between enemies i and j
                dx = tracker.x[i] - tracker.x[j]
                dy = tracker.y[i] - tracker.y[j]
                distance = np.sqrt(dx**2 + dy**2)
                
                # If close enough, add to cluster
                if distance < cluster_distance:
                    cluster.append(j)
                    clustered.add(j)
            
            # Only keep clusters with 2+ enemies
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def get_cluster_info(self, tracker, clusters):
        """
        Calculate information about each cluster
        
        Returns list of dicts with cluster details
        """
        info = []
        
        for cluster in clusters:
            # Calculate cluster center (average position)
            center_x = np.mean(tracker.x[cluster])
            center_y = np.mean(tracker.y[cluster])
            
            # Calculate total energy in cluster
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


class AntiGravityTank(Bot):
    """
    Advanced tank with physics-based anti-gravity movement
    
    Uses repulsive forces to automatically escape from
    dangerous situations and enemy swarms!
    
    Key Features:
    - Anti-gravity movement (enemies push you away)
    - Cluster detection (find enemy groups)
    - Smart force weighting (stronger enemies = bigger push)
    - Wall avoidance (walls push you away too!)
    """
    
    def __init__(self, bot_info=None):
        super().__init__(bot_info=bot_info)
        self.name = "AntiGravityTank"
        
        # Systems
        self.enemies = EnemyTracker()
        self.movement = AntiGravityMovement(force_constant=1200)
        self.cluster_detector = ClusterDetector()
        self.targeting = TargetingSystem()
        
        # State
        self.tick = 0
        self.get_radar_direction() = 1
        
        # Statistics
        self.max_enemies_seen = 0
        self.clusters_detected = 0
    
    def turn_to(self, target_angle):
        """Helper to turn to absolute angle"""
        current = self.get_direction() % 360
        target = target_angle % 360
        diff = (target - current + 180) % 360 - 180
        if diff < 0:
            self.turn_rate = -(abs(diff))
        else:
            self.turn_rate = diff
    
    async def run(self):
        """
        Main loop - runs every game tick
        """
        while self.is_running():
            self.tick += 1
            
            # Cleanup old enemy data periodically
            if self.tick % 20 == 0:
                self.enemies.cleanup(self.tick)
            
            # Use anti-gravity movement!
            # This automatically moves away from all enemies
            self.movement.move(self, self.enemies)
            
            # Sweep radar to find enemies
            self.radar_turn_rate = self.get_radar_direction() * 45
            if self.tick % 8 == 0:
                self.get_radar_direction() *= -1  # Reverse direction
            
            # Engage targets
            if self.enemies.count() > 0:
                await self.engage_best_target()
            
            # Detect and report clusters periodically
            if self.tick % 100 == 0 and self.enemies.count() > 2:
                clusters = self.cluster_detector.find_clusters(self.enemies)
                if clusters:
                    cluster_info = self.cluster_detector.get_cluster_info(
                        self.enemies, clusters
                    )
                    self.clusters_detected += len(clusters)
                    
                    # Find most dangerous cluster
                    most_dangerous = max(cluster_info, key=lambda c: c['threat_level'])
                    print(f"⚠️  Detected {len(clusters)} enemy clusters! "
                          f"Biggest threat: {most_dangerous['size']} enemies")
            
            # Track statistics
            if self.enemies.count() > self.max_enemies_seen:
                self.max_enemies_seen = self.enemies.count()
            
            await self.go()
    
    async def on_scanned_bot(self, event):
        """
        Called when radar detects an enemy
        
        Updates our enemy tracking system
        """
        # Enemy position is directly from event
        enemy_x = event.x
        enemy_y = event.y
        
        # Convert enemy direction and velocity to velocity components
        heading_rad = math.radians(event.direction)
        vx = event.speed * math.sin(heading_rad)
        vy = event.speed * math.cos(heading_rad)
        
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
        """
        Choose and shoot at the best target
        
        Targets closest weak enemies preferentially
        """
        if self.enemies.count() == 0:
            return
        
        # Calculate distances to all enemies
        distances = self.targeting.calculate_distances(
            self.get_x(), self.get_y(),
            self.enemies.x, self.enemies.y
        )
        
        # Target selection: prioritize close + weak enemies
        # Close enemies are immediate threats
        # Weak enemies are easy kills
        scores = (1000 / (distances + 1)) + (100 - self.enemies.energy) * 2
        
        # Find best target
        best_idx = np.argmax(scores)
        
        # Get target info
        target_x = self.enemies.x[best_idx]
        target_y = self.enemies.y[best_idx]
        target_vx = self.enemies.vx[best_idx]
        target_vy = self.enemies.vy[best_idx]
        target_distance = distances[best_idx]
        
        # Predict where target will be when bullet arrives
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power
        time_to_hit = target_distance / bullet_speed
        
        future_x = target_x + target_vx * time_to_hit
        future_y = target_y + target_vy * time_to_hit
        
        # Calculate aim angle
        angle = np.degrees(np.arctan2(
            future_x - self.get_x(),
            future_y - self.get_y()
        ))
        
        # Aim gun
        self.gun_turn_rate = self.calc_gun_turn(angle)
        
        # Choose power based on distance
        if target_distance < 200:
            await self.fire(3)  # High power for close targets
        elif target_distance < 400:
            await self.fire(2)  # Medium power
        else:
            await self.fire(1)  # Low power for distant targets
    
    async def on_hit_by_bullet(self, event):
        """
        React when we get hit
        
        Give ourselves an extra boost to escape danger!
        """
        # Quick acceleration away from danger
        self.target_speed = 60
    
    async def on_hit_wall(self, event):
        """React when we hit a wall"""
        # Back up and turn around
        self.target_speed = -(50)
        self.turn_rate = 90
    
    def on_robot_death(self, event):
        """Called when any robot dies"""
        # Could track successful eliminations here
        pass


    def calc_gun_turn(self, target_angle):
        """Calculate gun turn needed to face target angle"""
        diff = target_angle - self.get_gun_direction()
        # Normalize to -180 to 180
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        return diff


# Main entry point

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "anti_gravity_tank.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = AntiGravityTank(bot_info=bot_info)
    asyncio.run(bot.start())
