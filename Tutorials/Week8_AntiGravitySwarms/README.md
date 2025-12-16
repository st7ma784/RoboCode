# Week 8: Anti-Gravity & Swarm Intelligence! 🧲🤖

> **Note:** This tutorial uses the BaseBot API which uses **property assignments** instead of method calls.
> - Movement: `self.forward = 100` (not `self.forward(100)`)
> - Turning: `self.turn_body = 45` (not `self.turn_right(45)`)
> - All event handlers must be `async` and use `await` for actions like `await self.fire()`

Imagine enemies surrounding you like a pack of wolves! This week you'll learn how to:

1. Use anti-gravity movement to escape from crowds
2. Detect enemy clusters (groups working together)
3. Recognize formations and patterns
4. Find safe zones on the battlefield
5. Apply physics concepts to tank movement
6. Outsmart coordinated attacks!

## Part 1: The Physics of Anti-Gravity 🧲

### What is Anti-Gravity Movement?

Think of each enemy like a magnet that **pushes you away**:
- Close enemy = strong push
- Far enemy = weak push
- Multiple enemies = pushes combine!

Your tank calculates all the "forces" and moves in the safest direction!

### Real-World Analogy

Imagine you're playing tag with multiple friends:
- If one friend is very close, you run away from them
- If two friends are on your left, you run to the right
- If surrounded, you run toward the biggest gap
- You automatically dodge without thinking about each person!

That's what anti-gravity movement does - automatically dodges all threats at once!

## Part 2: Understanding Forces 💪

### Single Enemy Force

```python
import numpy as np

def calculate_force_from_enemy(my_x, my_y, enemy_x, enemy_y):
    """
    Calculate the "push" force from one enemy
    
    Like a magnet pushing you away!
    """
    # Direction to enemy
    dx = enemy_x - my_x
    dy = enemy_y - my_y
    
    # Distance to enemy
    distance = np.sqrt(dx**2 + dy**2)
    
    # Force strength (closer = stronger)
    # We use 1/distance so closer enemies have more influence
    force_strength = 1000 / (distance + 1)
    
    # Force direction (opposite of enemy direction!)
    # Negative because we want to move AWAY
    force_x = -dx / (distance + 1) * force_strength
    force_y = -dy / (distance + 1) * force_strength
    
    return force_x, force_y

# Example
my_x, my_y = 400, 300
enemy_x, enemy_y = 450, 350

fx, fy = calculate_force_from_enemy(my_x, my_y, enemy_x, enemy_y)
print(f"Enemy pushes us with force: ({fx:.1f}, {fy:.1f})")
```

### Multiple Enemy Forces

The magic happens when we add ALL forces together!

```python
def calculate_total_force(my_x, my_y, enemy_x_array, enemy_y_array):
    """
    Calculate combined force from ALL enemies
    
    Each enemy pushes us, and all pushes add up!
    """
    # Direction to each enemy
    dx = enemy_x_array - my_x
    dy = enemy_y_array - my_y
    
    # Distance to each enemy
    distances = np.sqrt(dx**2 + dy**2)
    
    # Force from each enemy (closer = stronger)
    force_strengths = 1000 / (distances + 1)
    
    # Force components from each enemy
    force_x_each = -dx / (distances + 1) * force_strengths
    force_y_each = -dy / (distances + 1) * force_strengths
    
    # Total force = sum of all forces!
    total_force_x = np.sum(force_x_each)
    total_force_y = np.sum(force_y_each)
    
    return total_force_x, total_force_y

# Example with 3 enemies
enemy_x = np.array([450, 350, 400])
enemy_y = np.array([350, 250, 400])

fx, fy = calculate_total_force(my_x, my_y, enemy_x, enemy_y)
print(f"Total force pushing us: ({fx:.1f}, {fy:.1f})")

# Convert force to angle
escape_angle = np.degrees(np.arctan2(fx, fy))
print(f"Best escape direction: {escape_angle:.1f}°")
```

### Visualizing Forces

```
        Enemy1
          ⬇ (pushes down)
          
Enemy2 ➡  YOU  ⬅ Enemy3
(pushes right) (pushes left)

Total force: ⬇ (down)
You move: ⬆ (up and away!)
```

## Part 3: Anti-Gravity Movement System 🚀

### Basic Anti-Gravity Movement

```python
class AntiGravityMovement:
    """
    Movement strategy that avoids crowds of enemies
    
    Uses physics-inspired force calculations to find
    the safest direction to move!
    """
    
    def __init__(self, force_constant=1000):
        self.force_constant = force_constant
    
    def calculate_escape_direction(self, my_x, my_y, tracker):
        """
        Calculate the best direction to move away from all enemies
        
        Returns angle in degrees
        """
        if tracker.count() == 0:
            return None  # No enemies, no forces
        
        # Get all enemy positions
        enemy_x = tracker.x
        enemy_y = tracker.y
        
        # Calculate distances to all enemies
        dx = enemy_x - my_x
        dy = enemy_y - my_y
        distances = np.sqrt(dx**2 + dy**2)
        
        # Calculate repulsive forces
        # Add small number to avoid division by zero
        force_strengths = self.force_constant / (distances + 1)
        
        # Calculate force components
        force_x = -np.sum((dx / (distances + 1)) * force_strengths)
        force_y = -np.sum((dy / (distances + 1)) * force_strengths)
        
        # Convert to angle
        if force_x == 0 and force_y == 0:
            return None  # No clear direction
        
        escape_angle = np.degrees(np.arctan2(force_x, force_y))
        return escape_angle
    
    def move(self, tank, tracker):
        """Apply anti-gravity movement to tank"""
        escape_direction = self.calculate_escape_direction(
            tank.x, tank.y, tracker
        )
        
        if escape_direction is not None:
            # Turn toward escape direction
            tank.turn_to(escape_direction)
            
            # Move in that direction
            tank.ahead(30)
        else:
            # No enemies detected, move normally
            tank.ahead(20)
```

### Using Anti-Gravity in Your Tank

```python
class AntiGravityTank:
    def __init__(self):
        self.name = "AntiGravityTank"
        self.enemies = EnemyTracker()
        self.movement = AntiGravityMovement()
        self.tick = 0
    
    def run(self):
        self.tick += 1
        
        # Use anti-gravity movement!
        self.movement.move(self, self.enemies)
        
        # Scan for enemies
        self.turn_radar_right(45)
```

## Part 4: Advanced Anti-Gravity 🎯

### Weighted Forces

Not all enemies are equally dangerous! Weight forces by threat:

```python
def calculate_weighted_forces(my_x, my_y, tracker):
    """
    Calculate forces weighted by threat level
    
    Close + strong enemy = BIG push
    Far + weak enemy = small push
    """
    if tracker.count() == 0:
        return 0, 0
    
    # Basic distances and directions
    dx = tracker.x - my_x
    dy = tracker.y - my_y
    distances = np.sqrt(dx**2 + dy**2)
    
    # Base force strength
    force_strengths = 1000 / (distances + 1)
    
    # Weight by enemy energy (stronger enemies = bigger threat)
    threat_weights = tracker.energy / 100
    
    # Combine weights
    weighted_forces = force_strengths * threat_weights
    
    # Calculate force components
    force_x = -np.sum((dx / (distances + 1)) * weighted_forces)
    force_y = -np.sum((dy / (distances + 1)) * weighted_forces)
    
    return force_x, force_y
```

### Wall Attraction

Add attraction to walls when enemies are behind you!

```python
def calculate_wall_forces(my_x, my_y, battlefield_width, battlefield_height):
    """
    Calculate gentle attraction to walls for positioning
    
    Walls can be your friend - use them to limit enemy angles!
    """
    margin = 100
    force_x = 0
    force_y = 0
    
    # Attraction to walls (gentle)
    if my_x < battlefield_width / 2:
        # Slight pull toward left wall
        force_x -= 50
    else:
        # Slight pull toward right wall
        force_x += 50
    
    if my_y < battlefield_height / 2:
        # Slight pull toward top wall
        force_y -= 50
    else:
        # Slight pull toward bottom wall
        force_y += 50
    
    return force_x, force_y
```

### Combined Forces

```python
def calculate_movement_forces(tank, tracker):
    """
    Combine multiple force sources for smart movement
    """
    # Repulsion from enemies
    enemy_fx, enemy_fy = calculate_weighted_forces(
        tank.x, tank.y, tracker
    )
    
    # Gentle wall attraction
    wall_fx, wall_fy = calculate_wall_forces(
        tank.x, tank.y,
        tank.battlefield_width,
        tank.battlefield_height
    )
    
    # Wall repulsion (don't hit walls!)
    margin = 80
    wall_repel_fx = 0
    wall_repel_fy = 0
    
    if tank.x < margin:
        wall_repel_fx = 500  # Push right
    elif tank.x > tank.battlefield_width - margin:
        wall_repel_fx = -500  # Push left
    
    if tank.y < margin:
        wall_repel_fy = 500  # Push down
    elif tank.y > tank.battlefield_height - margin:
        wall_repel_fy = -500  # Push up
    
    # Combine all forces
    total_fx = enemy_fx + wall_fx * 0.1 + wall_repel_fx
    total_fy = enemy_fy + wall_fy * 0.1 + wall_repel_fy
    
    # Convert to angle
    escape_angle = np.degrees(np.arctan2(total_fx, total_fy))
    
    return escape_angle
```

## Part 5: Cluster Detection - Finding Enemy Groups 👥

### What is a Cluster?

A cluster is a group of enemies close together. They're extra dangerous because:
- Multiple enemies can attack from the same direction
- They might be coordinating
- You can't dodge them all individually

### Distance-Based Clustering

```python
def find_enemy_clusters(tracker, cluster_distance=150):
    """
    Find groups of enemies that are close together
    
    Returns list of clusters (each cluster is a list of enemy indices)
    """
    if tracker.count() < 2:
        return []
    
    clusters = []
    clustered = set()
    
    for i in range(tracker.count()):
        if i in clustered:
            continue
        
        # Start a new cluster with this enemy
        cluster = [i]
        clustered.add(i)
        
        # Find all enemies close to this one
        for j in range(i + 1, tracker.count()):
            if j in clustered:
                continue
            
            # Distance between enemy i and enemy j
            dx = tracker.x[i] - tracker.x[j]
            dy = tracker.y[i] - tracker.y[j]
            distance = np.sqrt(dx**2 + dy**2)
            
            if distance < cluster_distance:
                cluster.append(j)
                clustered.add(j)
        
        if len(cluster) > 1:
            clusters.append(cluster)
    
    return clusters
```

### Cluster Centers

```python
def calculate_cluster_centers(tracker, clusters):
    """
    Find the center point of each cluster
    
    Useful for treating a cluster as one big threat!
    """
    centers = []
    
    for cluster in clusters:
        # Get positions of enemies in this cluster
        cluster_x = tracker.x[cluster]
        cluster_y = tracker.y[cluster]
        
        # Calculate average position (center)
        center_x = np.mean(cluster_x)
        center_y = np.mean(cluster_y)
        
        centers.append({
            'x': center_x,
            'y': center_y,
            'size': len(cluster),
            'members': cluster
        })
    
    return centers
```

### Using Clusters in Movement

```python
def calculate_cluster_aware_forces(my_x, my_y, tracker):
    """
    Calculate anti-gravity forces treating clusters as single threats
    
    A cluster of 5 enemies pushes harder than 5 separate enemies!
    """
    # Find clusters
    clusters = find_enemy_clusters(tracker)
    cluster_centers = calculate_cluster_centers(tracker, clusters)
    
    force_x = 0
    force_y = 0
    
    # Get indices of all clustered enemies
    clustered_indices = set()
    for cluster in clusters:
        clustered_indices.update(cluster)
    
    # Forces from clusters (treated as single strong enemies)
    for center in cluster_centers:
        dx = center['x'] - my_x
        dy = center['y'] - my_y
        distance = np.sqrt(dx**2 + dy**2)
        
        # Cluster force is stronger based on size
        force_strength = 1000 * center['size'] / (distance + 1)
        
        force_x -= (dx / (distance + 1)) * force_strength
        force_y -= (dy / (distance + 1)) * force_strength
    
    # Forces from individual enemies (not in clusters)
    for i in range(tracker.count()):
        if i not in clustered_indices:
            dx = tracker.x[i] - my_x
            dy = tracker.y[i] - my_y
            distance = np.sqrt(dx**2 + dy**2)
            
            force_strength = 1000 / (distance + 1)
            force_x -= (dx / (distance + 1)) * force_strength
            force_y -= (dy / (distance + 1)) * force_strength
    
    return force_x, force_y
```

## Part 6: Formation Recognition 🎖️

### Detecting Enemy Formations

```python
def detect_formation_type(tracker):
    """
    Try to identify if enemies are in a recognizable pattern
    
    Returns: 'scattered', 'line', 'surrounding', 'clustered'
    """
    if tracker.count() < 3:
        return 'scattered'
    
    # Calculate center of all enemies
    center_x = np.mean(tracker.x)
    center_y = np.mean(tracker.y)
    
    # Calculate distances from center
    distances = np.sqrt(
        (tracker.x - center_x)**2 + 
        (tracker.y - center_y)**2
    )
    
    # Check if enemies are in a line
    # Calculate spread in X vs Y directions
    x_spread = np.std(tracker.x)
    y_spread = np.std(tracker.y)
    
    if x_spread > y_spread * 3:
        return 'horizontal_line'
    elif y_spread > x_spread * 3:
        return 'vertical_line'
    
    # Check if enemies are surrounding a point
    # Even distribution of angles = surrounding
    angles = np.degrees(np.arctan2(
        tracker.x - center_x,
        tracker.y - center_y
    ))
    
    # Check if angles are evenly distributed
    angles_sorted = np.sort(angles)
    angle_diffs = np.diff(angles_sorted)
    
    if np.std(angle_diffs) < 30:  # Relatively even spacing
        return 'surrounding'
    
    # Check if enemies are clustered
    avg_distance_from_center = np.mean(distances)
    if avg_distance_from_center < 200:
        return 'clustered'
    
    return 'scattered'
```

### Reacting to Formations

```python
def choose_strategy_for_formation(formation_type):
    """
    Choose movement strategy based on enemy formation
    
    Different formations need different responses!
    """
    strategies = {
        'scattered': 'anti_gravity',
        'horizontal_line': 'perpendicular_movement',
        'vertical_line': 'perpendicular_movement',
        'surrounding': 'break_through_weakest',
        'clustered': 'stay_far_away'
    }
    
    return strategies.get(formation_type, 'anti_gravity')


def execute_formation_response(tank, tracker, formation_type):
    """
    Execute the appropriate response to enemy formation
    """
    if formation_type == 'perpendicular_movement':
        # Move perpendicular to the line
        center_x = np.mean(tracker.x)
        center_y = np.mean(tracker.y)
        
        # Move at 90 degrees to the line
        angle_to_center = np.degrees(np.arctan2(
            center_x - tank.x,
            center_y - tank.y
        ))
        escape_angle = angle_to_center + 90
        
        tank.turn_to(escape_angle)
        tank.ahead(40)
    
    elif formation_type == 'break_through_weakest':
        # Find the weakest enemy and move toward them aggressively
        weakest_idx = np.argmin(tracker.energy)
        
        angle_to_weakest = np.degrees(np.arctan2(
            tracker.x[weakest_idx] - tank.x,
            tracker.y[weakest_idx] - tank.y
        ))
        
        tank.turn_to(angle_to_weakest)
        tank.ahead(50)
    
    elif formation_type == 'stay_far_away':
        # Use anti-gravity with extra strength
        fx, fy = calculate_weighted_forces(tank.x, tank.y, tracker)
        
        escape_angle = np.degrees(np.arctan2(fx, fy))
        tank.turn_to(escape_angle)
        tank.ahead(50)
    
    else:
        # Default: normal anti-gravity
        fx, fy = calculate_weighted_forces(tank.x, tank.y, tracker)
        escape_angle = np.degrees(np.arctan2(fx, fy))
        tank.turn_to(escape_angle)
        tank.ahead(30)
```

## Part 7: Safe Zone Finder 🛡️

### Finding the Safest Location

```python
def find_safe_zones(tracker, battlefield_width, battlefield_height, grid_size=10):
    """
    Calculate danger level across the battlefield
    
    Returns a grid showing where it's safest to be
    """
    # Create grid
    x_points = np.linspace(0, battlefield_width, grid_size)
    y_points = np.linspace(0, battlefield_height, grid_size)
    
    danger_grid = np.zeros((grid_size, grid_size))
    
    # Calculate danger at each grid point
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            # Calculate total danger from all enemies
            if tracker.count() > 0:
                dx = tracker.x - x
                dy = tracker.y - y
                distances = np.sqrt(dx**2 + dy**2)
                
                # Danger = sum of 1/distance for all enemies
                danger = np.sum(1000 / (distances + 1))
                danger_grid[j, i] = danger
    
    return danger_grid, x_points, y_points


def find_safest_position(danger_grid, x_points, y_points):
    """
    Find the location with lowest danger
    """
    min_idx = np.unravel_index(np.argmin(danger_grid), danger_grid.shape)
    
    safest_x = x_points[min_idx[1]]
    safest_y = y_points[min_idx[0]]
    
    return safest_x, safest_y, danger_grid[min_idx]
```

### Moving Toward Safety

```python
def move_to_safe_zone(tank, tracker):
    """
    Calculate and move toward the safest area
    """
    danger_grid, x_points, y_points = find_safe_zones(
        tracker,
        tank.battlefield_width,
        tank.battlefield_height,
        grid_size=10
    )
    
    safest_x, safest_y, danger_level = find_safest_position(
        danger_grid, x_points, y_points
    )
    
    # Move toward safest position
    angle = np.degrees(np.arctan2(
        safest_x - tank.x,
        safest_y - tank.y
    ))
    
    tank.turn_to(angle)
    tank.ahead(30)
    
    return safest_x, safest_y
```

## Part 8: Complete Anti-Gravity Tank! 🤖

Create `anti_gravity_tank.py`:

```python
"""
Anti-Gravity Tank - Advanced movement with cluster awareness
Uses physics-inspired forces to escape from enemy swarms!
"""
import numpy as np
import math


class TargetingSystem:
    """Math utilities"""
    
    def calculate_distances(self, my_x, my_y, enemy_x, enemy_y):
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.sqrt(x_diff**2 + y_diff**2)
    
    def calculate_angles(self, my_x, my_y, enemy_x, enemy_y):
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        return np.degrees(np.arctan2(x_diff, y_diff))


class EnemyTracker:
    """Track multiple enemies"""
    
    def __init__(self):
        self.enemy_ids = []
        self.x = np.array([])
        self.y = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])
        self.energy = np.array([])
        self.last_seen = np.array([])
    
    def update(self, enemy_id, x, y, vx, vy, energy, tick):
        if enemy_id in self.enemy_ids:
            idx = self.enemy_ids.index(enemy_id)
            self.x[idx] = x
            self.y[idx] = y
            self.vx[idx] = vx
            self.vy[idx] = vy
            self.energy[idx] = energy
            self.last_seen[idx] = tick
        else:
            self.enemy_ids.append(enemy_id)
            self.x = np.append(self.x, x)
            self.y = np.append(self.y, y)
            self.vx = np.append(self.vx, vx)
            self.vy = np.append(self.vy, vy)
            self.energy = np.append(self.energy, energy)
            self.last_seen = np.append(self.last_seen, tick)
    
    def cleanup(self, current_tick, max_age=100):
        if len(self.enemy_ids) == 0:
            return
        
        age = current_tick - self.last_seen
        keep = age < max_age
        
        if not np.any(keep):
            self.__init__()
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
        return len(self.enemy_ids)


class AntiGravityMovement:
    """
    Advanced movement using repulsive forces from enemies
    """
    
    def __init__(self, force_constant=1000):
        self.force_constant = force_constant
    
    def calculate_forces(self, my_x, my_y, tracker):
        """Calculate anti-gravity forces from all enemies"""
        if tracker.count() == 0:
            return 0, 0
        
        # Distances and directions
        dx = tracker.x - my_x
        dy = tracker.y - my_y
        distances = np.sqrt(dx**2 + dy**2)
        
        # Repulsive force (weighted by enemy energy)
        threat_weights = tracker.energy / 100
        force_strengths = self.force_constant * threat_weights / (distances + 1)
        
        # Force components (negative = repulsion)
        force_x = -np.sum((dx / (distances + 1)) * force_strengths)
        force_y = -np.sum((dy / (distances + 1)) * force_strengths)
        
        return force_x, force_y
    
    def add_wall_repulsion(self, my_x, my_y, battlefield_width, battlefield_height):
        """Add forces to avoid walls"""
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
    
    def move(self, tank, tracker):
        """Apply anti-gravity movement"""
        # Enemy repulsion
        fx, fy = self.calculate_forces(tank.x, tank.y, tracker)
        
        # Wall repulsion
        wall_fx, wall_fy = self.add_wall_repulsion(
            tank.x, tank.y,
            tank.battlefield_width,
            tank.battlefield_height
        )
        
        # Combine forces
        total_fx = fx + wall_fx
        total_fy = fy + wall_fy
        
        # Convert to movement
        if total_fx != 0 or total_fy != 0:
            escape_angle = np.degrees(np.arctan2(total_fx, total_fy))
            tank.turn_to(escape_angle)
            tank.ahead(30)
        else:
            # No forces, move freely
            tank.ahead(20)


class ClusterDetector:
    """
    Detect and analyze enemy clusters
    """
    
    def find_clusters(self, tracker, cluster_distance=150):
        """Find groups of enemies close together"""
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
        """Get information about each cluster"""
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
                'members': cluster
            })
        
        return info


class AntiGravityTank:
    """
    Advanced tank with anti-gravity movement and cluster awareness
    """
    
    def __init__(self):
        self.name = "AntiGravityTank"
        
        # Systems
        self.enemies = EnemyTracker()
        self.movement = AntiGravityMovement(force_constant=1200)
        self.cluster_detector = ClusterDetector()
        self.targeting = TargetingSystem()
        
        # State
        self.tick = 0
        self.radar_direction = 1
    
    def run(self):
        """Main loop"""
        self.tick += 1
        
        # Cleanup old data
        if self.tick % 20 == 0:
            self.enemies.cleanup(self.tick)
        
        # Use anti-gravity movement
        self.movement.move(self, self.enemies)
        
        # Radar sweep
        self.turn_radar_right(self.radar_direction * 45)
        if self.tick % 8 == 0:
            self.radar_direction *= -1
        
        # Engage targets
        if self.enemies.count() > 0:
            self.engage_best_target()
        
        # Report clusters periodically
        if self.tick % 100 == 0 and self.enemies.count() > 2:
            clusters = self.cluster_detector.find_clusters(self.enemies)
            if clusters:
                print(f"Detected {len(clusters)} enemy clusters!")
    
    def on_scanned_robot(self, scanned):
        """Update enemy tracking"""
        heading_rad = math.radians(scanned.heading)
        vx = scanned.velocity * math.sin(heading_rad)
        vy = scanned.velocity * math.cos(heading_rad)
        
        self.enemies.update(
            enemy_id=scanned.name,
            x=scanned.x,
            y=scanned.y,
            vx=vx,
            vy=vy,
            energy=scanned.energy,
            tick=self.tick
        )
    
    def engage_best_target(self):
        """Choose and shoot best target"""
        if self.enemies.count() == 0:
            return
        
        # Calculate distances
        distances = self.targeting.calculate_distances(
            self.x, self.y,
            self.enemies.x, self.enemies.y
        )
        
        # Target selection: close + weak
        scores = (1000 / (distances + 1)) + (100 - self.enemies.energy) * 2
        best_idx = np.argmax(scores)
        
        # Predict and shoot
        target_distance = distances[best_idx]
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power
        time_to_hit = target_distance / bullet_speed
        
        # Predict future position
        future_x = self.enemies.x[best_idx] + self.enemies.vx[best_idx] * time_to_hit
        future_y = self.enemies.y[best_idx] + self.enemies.vy[best_idx] * time_to_hit
        
        # Aim and fire
        angle = np.degrees(np.arctan2(
            future_x - self.get_x(),
            future_y - self.get_y()
        ))
        
        self.turn_gun_to(angle)
        
        if target_distance < 200:
            self.fire(3)
        elif target_distance < 400:
            self.fire(2)
        else:
            self.fire(1)
    
    def on_hit_by_bullet(self, event):
        """React to being hit"""
        # Extra boost away from danger
        self.ahead(60)
```

## Part 9: Testing Anti-Gravity 🧪

### Battle Against Multiple Enemies

```bash
# Start RoboCode GUI, then run your tank:
python Tutorials/Week8_AntiGravitySwarms/anti_gravity_tank.py --all-samples
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

### Visualizing Movement

Add this to track where your tank goes:

```python
class AntiGravityTank:
    def __init__(self):
        # ... other init ...
        self.position_history = []
    
    def run(self):
        # ... existing code ...
        
        # Track position
        if self.tick % 10 == 0:
            self.position_history.append((self.get_x(), self.get_y()))
            
            # Print movement pattern periodically
            if len(self.position_history) > 50:
                # Calculate how much area we've covered
                xs = [p[0] for p in self.position_history]
                ys = [p[1] for p in self.position_history]
                coverage = (max(xs) - min(xs)) * (max(ys) - min(ys))
                print(f"Coverage area: {coverage:.0f} square pixels")
                
                self.position_history = []
```

## Part 10: Challenges and Experiments 🚀

### Easy Challenges:
1. **Force Visualizer** - Print the direction and strength of anti-gravity forces
2. **Cluster Counter** - Display number of clusters detected
3. **Danger Level Indicator** - Show total danger from all enemies
4. **Safe Zone Finder** - Calculate and move toward safest area

### Medium Challenges:
1. **Adaptive Force Strength** - Adjust force constant based on number of enemies
2. **Cluster Priority Targeting** - Always shoot at the biggest cluster first
3. **Formation Detector** - Detect if enemies are in a line or surrounding pattern
4. **Energy-Based Weighting** - Stronger enemies push harder

### Hard Challenges:
1. **Predictive Anti-Gravity** - Account for enemy velocity in force calculations
2. **Corner Escape** - Special logic when trapped in corners
3. **Cluster Breaking** - Move to split up enemy clusters
4. **Dynamic Safety Grid** - Update safe zones every few ticks

### Expert Challenges:
1. **Multi-Step Planning** - Plan next 5 moves considering enemy movements
2. **Coordinated Evasion** - If you had allies, coordinate anti-gravity movements
3. **Threat Prediction** - Predict where enemy clusters will form
4. **Optimal Positioning** - Balance safety with shooting opportunities

## Part 11: Understanding the Math 📐

### Why Anti-Gravity Works

```
Physics principle: F = k / r²
F = Force
k = constant
r = distance

For tanks:
- Close enemy (r=50): F = 1000/50 = 20 (strong push!)
- Far enemy (r=500): F = 1000/500 = 2 (weak push)

Multiple enemies: F_total = F1 + F2 + F3 + ...
```

### Vector Addition

```
Enemy1 pushes you: (10, 5)
Enemy2 pushes you: (-3, 8)
Total force: (7, 13)

Escape direction = atan2(7, 13) = ~28 degrees
```

## Part 12: Real-World Applications 🌍

These concepts are used in:

### Robotics
- Swarm robots avoiding collisions
- Drones maintaining formation
- Autonomous vehicles navigating crowds

### Video Games
- NPCs avoiding each other
- Flocking behavior (birds, fish)
- Path finding in crowds

### Computer Graphics
- Particle systems
- Crowd simulation
- Animation

### Biology & Nature
- How fish schools move
- Bird flocking patterns
- Animal herd behavior

## Part 13: Submit Your Anti-Gravity Tank! 🏆

Ready to showcase your advanced movement?

1. Test against 5+ enemies simultaneously
2. Verify cluster detection works
3. Ensure smooth anti-gravity movement
4. Copy to `Submissions/YourName/anti_gravity_tank.py`
5. Create Pull Request: `[Submission] YourName's Anti-Gravity Tank`

In your PR description:
```
## Anti-Gravity Tank Submission

**Tank Name:** AntiGravityTank
**Week:** Week 8 - Anti-Gravity & Swarms

**Features:**
- Physics-based anti-gravity movement
- Cluster detection and analysis
- Smart force weighting by threat level
- Automatic safe zone finding

**Special Abilities:**
- Escapes from surrounded positions
- Detects enemy formations
- Maintains optimal distance from threats

Ready for swarm battles!
```

## Homework

Before moving forward:
1. ✅ Implement basic anti-gravity movement
2. ✅ Add cluster detection
3. ✅ Test with varying numbers of enemies (3, 10, 20+)
4. ✅ Try different force constants (500, 1000, 2000)
5. ✅ Implement at least one challenge
6. ✅ Submit your tank

**Bonus**: Create a heat map showing danger levels across the battlefield!

## Quick Reference

### Anti-Gravity Force Calculation
```python
def calculate_anti_gravity(my_x, my_y, enemy_x, enemy_y):
    dx = enemy_x - my_x
    dy = enemy_y - my_y
    distance = np.sqrt(dx**2 + dy**2)
    force_strength = 1000 / (distance + 1)
    force_x = -dx / (distance + 1) * force_strength
    force_y = -dy / (distance + 1) * force_strength
    return force_x, force_y
```

### Cluster Detection
```python
def find_clusters(tracker, threshold=150):
    clusters = []
    for i in range(tracker.count()):
        for j in range(i+1, tracker.count()):
            dist = np.sqrt(
                (tracker.x[i] - tracker.x[j])**2 +
                (tracker.y[i] - tracker.y[j])**2
            )
            if dist < threshold:
                # Add to cluster
                pass
    return clusters
```

### Escape Angle Calculation
```python
escape_angle = np.degrees(np.arctan2(force_x, force_y))
```

## Help!

**"My tank goes in circles!"**
- Forces might be balanced - add some randomness
- Check wall repulsion is working
- Make sure you're turning toward escape angle correctly

**"Tank doesn't avoid enemies!"**
- Verify force_constant is large enough (try 1000-2000)
- Check that distances are calculated correctly
- Print force values to debug

**"Cluster detection finds too many/few clusters!"**
- Adjust cluster_distance threshold (try 100-200)
- Make sure you're comparing all enemy pairs
- Test with different enemy counts

**"Tank hits walls!"**
- Increase wall repulsion force
- Decrease margin value for earlier detection
- Add stronger forces when very close to walls

---

Congratulations! You've mastered advanced movement AI! 🎉

You now understand:
- Physics-based movement
- Force calculations
- Cluster analysis
- Pattern recognition
- Spatial reasoning

These skills apply to robotics, game AI, and simulation! Keep experimenting!
