# Week 7: Battle Royale - Fighting 30+ Tanks at Once! 🎯⚔️

Imagine you're in an arena with **30 enemy tanks** all shooting at you! You can't think about each one individually - you need to think about them as a **crowd**. This week you'll learn:

1. Data structures - organizing information efficiently
2. Arrays and lists - storing many things at once
3. NumPy - super-fast math on lots of numbers
4. Matrix operations - doing 30 calculations instantly
5. Smart target selection - who should we shoot?
6. Threat assessment - who's most dangerous?

## Part 1: The Problem - Too Many Enemies! 🤯

### Your Old Tank vs 30 Enemies

Let's look at what happens with your Week 6 tank:

```python
def on_scanned_robot(self, scanned_robot):
    # Calculate one enemy...
    distance = calculate_distance(self.x, self.y, scanned_robot.x, scanned_robot.y)
    angle = calculate_angle(...)
    # Aim at this one enemy...
    self.fire(2)
```

**Problems:**
- ❌ Only tracks ONE enemy at a time
- ❌ Forgets about enemies you scanned earlier
- ❌ Can't compare threats
- ❌ Might shoot at someone far away while someone close is about to hit you!
- ❌ Does the same math over and over

### What We Need

```
Enemy 1: x=100, y=200, vx=3, vy=2, last_seen=10
Enemy 2: x=300, y=400, vx=-2, vy=1, last_seen=12
Enemy 3: x=500, y=100, vx=0, vy=-3, last_seen=8
...
Enemy 30: x=200, y=600, vx=1, vy=0, last_seen=15

Calculate ALL distances at once!
Calculate ALL threats at once!
Pick the BEST target instantly!
```

## Part 2: Data Structures - Organizing Information 📦

### What's a Data Structure?

Think of organizing your toys:
- **One toy** = One variable (`enemy_x = 100`)
- **Toy box** = A list (`enemies = [toy1, toy2, toy3]`)
- **Toy shelf with labeled boxes** = A dictionary (`toys = {"cars": [...], "dolls": [...]}`)

### Lists - Your First Data Structure

```python
# Instead of:
enemy1_x = 100
enemy2_x = 200
enemy3_x = 300

# Use a list!
enemy_x_positions = [100, 200, 300]

# Easy to add more
enemy_x_positions.append(400)  # Now: [100, 200, 300, 400]

# Easy to loop through
for x in enemy_x_positions:
    print(f"Enemy at x={x}")
```

### Dictionaries - Labeled Storage

```python
# Store info about one enemy
enemy = {
    "x": 100,
    "y": 200,
    "velocity_x": 3,
    "velocity_y": 2,
    "last_seen": 10,
    "health": 100
}

# Access the info
print(f"Enemy is at ({enemy['x']}, {enemy['y']})")
print(f"Enemy health: {enemy['health']}")
```

### List of Dictionaries - Multiple Enemies

```python
# Track ALL enemies!
enemies = [
    {"x": 100, "y": 200, "vx": 3, "vy": 2, "health": 100},
    {"x": 300, "y": 400, "vx": -2, "vy": 1, "health": 80},
    {"x": 500, "y": 100, "vx": 0, "vy": -3, "health": 50}
]

# Find all enemies with low health
weak_enemies = [e for e in enemies if e["health"] < 60]
print(f"Found {len(weak_enemies)} weak enemies!")

# Find closest enemy
distances = [calculate_distance(my_x, my_y, e["x"], e["y"]) for e in enemies]
closest_index = distances.index(min(distances))
closest_enemy = enemies[closest_index]
```

## Part 3: NumPy - Supercharged Math! ⚡

### Why NumPy?

Regular Python loops are like walking:
```python
# Calculate 1000 distances one at a time
for i in range(1000):
    distance = math.sqrt(x[i]**2 + y[i]**2)  # One at a time...
```

NumPy is like a sports car:
```python
import numpy as np
# Calculate 1000 distances INSTANTLY
distances = np.sqrt(x**2 + y**2)  # ALL AT ONCE!
```

### Installing NumPy

```bash
pip install numpy
```

### Your First NumPy Arrays

```python
import numpy as np

# Regular Python list
regular_list = [1, 2, 3, 4, 5]

# NumPy array - supercharged!
numpy_array = np.array([1, 2, 3, 4, 5])

# Math on ALL numbers at once!
print(numpy_array * 2)  # [2, 4, 6, 8, 10]
print(numpy_array + 10)  # [11, 12, 13, 14, 15]
print(numpy_array ** 2)  # [1, 4, 9, 16, 25]
```

### NumPy for Tank Positions

```python
import numpy as np

# Store all enemy X positions
enemy_x = np.array([100, 200, 300, 400, 500])
# Store all enemy Y positions
enemy_y = np.array([150, 250, 350, 450, 550])

# Calculate ALL distances at once!
my_x = 250
my_y = 250

x_diff = enemy_x - my_x  # [−150, −50, 50, 150, 250]
y_diff = enemy_y - my_y  # [−100, 0, 100, 200, 300]

distances = np.sqrt(x_diff**2 + y_diff**2)
print(distances)  # All 5 distances calculated instantly!

# Find closest enemy
closest_index = np.argmin(distances)
print(f"Closest enemy is at index {closest_index}")
print(f"At position ({enemy_x[closest_index]}, {enemy_y[closest_index]})")
```

## Part 4: Building an Enemy Tracking System 🎯

### EnemyTracker Class

```python
import numpy as np
import time

class EnemyTracker:
    """
    Track multiple enemies efficiently using NumPy arrays
    
    Think of this like a sports scoreboard that tracks
    all players at once!
    """
    
    def __init__(self, max_enemies=50):
        """Initialize arrays to track enemies"""
        self.max_enemies = max_enemies
        
        # Arrays for each piece of information
        self.enemy_ids = []  # List of enemy names/IDs
        self.x = np.array([])  # X positions
        self.y = np.array([])  # Y positions
        self.velocity_x = np.array([])  # X velocities
        self.velocity_y = np.array([])  # Y velocities
        self.energy = np.array([])  # Enemy health
        self.last_seen = np.array([])  # When we last saw them (game tick)
    
    def update_enemy(self, enemy_id, x, y, vx, vy, energy, current_tick):
        """Add or update an enemy in our tracking system"""
        
        if enemy_id in self.enemy_ids:
            # Update existing enemy
            idx = self.enemy_ids.index(enemy_id)
            self.x[idx] = x
            self.y[idx] = y
            self.velocity_x[idx] = vx
            self.velocity_y[idx] = vy
            self.energy[idx] = energy
            self.last_seen[idx] = current_tick
        else:
            # Add new enemy
            self.enemy_ids.append(enemy_id)
            self.x = np.append(self.x, x)
            self.y = np.append(self.y, y)
            self.velocity_x = np.append(self.velocity_x, vx)
            self.velocity_y = np.append(self.velocity_y, vy)
            self.energy = np.append(self.energy, energy)
            self.last_seen = np.append(self.last_seen, current_tick)
    
    def remove_stale_enemies(self, current_tick, max_age=50):
        """Remove enemies we haven't seen in a while"""
        if len(self.enemy_ids) == 0:
            return
        
        # Find enemies we've seen recently
        age = current_tick - self.last_seen
        keep_mask = age < max_age
        
        # Keep only fresh data
        keep_indices = np.where(keep_mask)[0]
        self.enemy_ids = [self.enemy_ids[i] for i in keep_indices]
        self.x = self.x[keep_mask]
        self.y = self.y[keep_mask]
        self.velocity_x = self.velocity_x[keep_mask]
        self.velocity_y = self.velocity_y[keep_mask]
        self.energy = self.energy[keep_mask]
        self.last_seen = self.last_seen[keep_mask]
    
    def get_enemy_count(self):
        """How many enemies are we tracking?"""
        return len(self.enemy_ids)
    
    def get_all_positions(self):
        """Get arrays of all enemy positions"""
        return self.x, self.y
```

### Using the Tracker

```python
# Create tracker
tracker = EnemyTracker()

# When you scan enemies
tracker.update_enemy("Enemy1", x=100, y=200, vx=3, vy=2, energy=100, current_tick=10)
tracker.update_enemy("Enemy2", x=300, y=400, vx=-2, vy=1, energy=80, current_tick=10)
tracker.update_enemy("Enemy3", x=500, y=100, vx=0, vy=-3, energy=50, current_tick=10)

print(f"Tracking {tracker.get_enemy_count()} enemies")

# Get all positions at once
enemy_x, enemy_y = tracker.get_all_positions()
print(f"Enemy X positions: {enemy_x}")
print(f"Enemy Y positions: {enemy_y}")
```

## Part 5: Matrix Operations - Calculate Everything at Once! 🧮

### Calculating ALL Distances

```python
def calculate_all_distances(my_x, my_y, enemy_x, enemy_y):
    """
    Calculate distance to ALL enemies at once
    
    This is MUCH faster than a loop!
    """
    x_diff = enemy_x - my_x
    y_diff = enemy_y - my_y
    distances = np.sqrt(x_diff**2 + y_diff**2)
    return distances

# Example with 5 enemies
my_x, my_y = 250, 250
enemy_x = np.array([100, 200, 300, 400, 500])
enemy_y = np.array([150, 250, 350, 450, 550])

distances = calculate_all_distances(my_x, my_y, enemy_x, enemy_y)
print(f"Distances to all 5 enemies: {distances}")
# Output: [111.8  50.0  111.8  223.6  353.6]
```

### Calculating ALL Angles

```python
def calculate_all_angles(my_x, my_y, enemy_x, enemy_y):
    """Calculate angle to ALL enemies at once"""
    x_diff = enemy_x - my_x
    y_diff = enemy_y - my_y
    angles = np.degrees(np.arctan2(x_diff, y_diff))
    return angles

angles = calculate_all_angles(my_x, my_y, enemy_x, enemy_y)
print(f"Angles to all 5 enemies: {angles}")
```

### Predicting ALL Future Positions

```python
def predict_all_positions(enemy_x, enemy_y, velocity_x, velocity_y, time_ticks):
    """
    Predict where ALL enemies will be in the future
    
    Instead of predicting one at a time, do them ALL!
    """
    future_x = enemy_x + velocity_x * time_ticks
    future_y = enemy_y + velocity_y * time_ticks
    return future_x, future_y

# Enemy velocities
velocity_x = np.array([3, -2, 0, 1, -1])
velocity_y = np.array([2, 1, -3, 2, 0])

# Where will they be in 10 ticks?
future_x, future_y = predict_all_positions(enemy_x, enemy_y, velocity_x, velocity_y, 10)
print(f"Future X positions: {future_x}")
print(f"Future Y positions: {future_y}")
```

### Finding Best Targets

```python
def find_best_targets(tracker, my_x, my_y):
    """
    Analyze ALL enemies and find the best targets
    Returns indices sorted by priority
    """
    if tracker.get_enemy_count() == 0:
        return []
    
    enemy_x, enemy_y = tracker.get_all_positions()
    
    # Calculate distances to all enemies
    distances = calculate_all_distances(my_x, my_y, enemy_x, enemy_y)
    
    # Calculate threat score for each enemy
    # Closer = more dangerous, low energy = easier kill
    threat_score = (1.0 / (distances + 1)) * 100  # Closer = higher score
    threat_score += (100 - tracker.energy) / 10  # Weaker = higher score
    
    # Sort by threat score (highest first)
    sorted_indices = np.argsort(threat_score)[::-1]
    
    return sorted_indices
```

## Part 6: Target Selection Strategy 🎯

### Smart Target Selection

```python
class TargetSelector:
    """
    Choose the best enemy to shoot at from many options
    
    Think of this like choosing which opponent to tackle
    in a game of tag - you want the closest, slowest one!
    """
    
    def __init__(self):
        self.targeting_math = TargetingSystem()
    
    def calculate_hit_probability(self, distance, enemy_velocity):
        """
        Estimate chance of hitting this enemy
        
        Close + slow = easy hit
        Far + fast = hard hit
        """
        # Closer = easier
        distance_factor = 1.0 / (1.0 + distance / 100)
        
        # Slower = easier
        speed = np.sqrt(enemy_velocity[0]**2 + enemy_velocity[1]**2)
        speed_factor = 1.0 / (1.0 + speed / 5)
        
        return distance_factor * speed_factor
    
    def calculate_all_hit_probabilities(self, my_x, my_y, tracker):
        """Calculate hit probability for ALL enemies at once"""
        if tracker.get_enemy_count() == 0:
            return np.array([])
        
        enemy_x, enemy_y = tracker.get_all_positions()
        distances = calculate_all_distances(my_x, my_y, enemy_x, enemy_y)
        
        # Calculate speed for all enemies
        speeds = np.sqrt(tracker.velocity_x**2 + tracker.velocity_y**2)
        
        # Calculate probability for all
        distance_factor = 1.0 / (1.0 + distances / 100)
        speed_factor = 1.0 / (1.0 + speeds / 5)
        probabilities = distance_factor * speed_factor
        
        return probabilities
    
    def select_best_target(self, my_x, my_y, tracker):
        """
        Choose the single best enemy to shoot at
        
        Considers:
        - Distance (closer is better)
        - Energy (weaker is better)
        - Hit probability (easier targets are better)
        """
        if tracker.get_enemy_count() == 0:
            return None
        
        enemy_x, enemy_y = tracker.get_all_positions()
        
        # Calculate all factors
        distances = calculate_all_distances(my_x, my_y, enemy_x, enemy_y)
        hit_probs = self.calculate_all_hit_probabilities(my_x, my_y, tracker)
        
        # Score each enemy
        # Higher score = better target
        scores = np.zeros(tracker.get_enemy_count())
        
        # Prefer close targets
        scores += (1.0 / (distances + 1)) * 50
        
        # Prefer weak targets (easier to destroy)
        scores += (100 - tracker.energy) / 2
        
        # Prefer high hit probability
        scores += hit_probs * 100
        
        # Find best target
        best_index = np.argmax(scores)
        
        return {
            "index": best_index,
            "id": tracker.enemy_ids[best_index],
            "x": enemy_x[best_index],
            "y": enemy_y[best_index],
            "vx": tracker.velocity_x[best_index],
            "vy": tracker.velocity_y[best_index],
            "distance": distances[best_index],
            "hit_probability": hit_probs[best_index],
            "score": scores[best_index]
        }
```

## Part 7: Building the Skirmisher Tank! 🤖

Create `skirmisher_tank.py`:

```python
"""
Skirmisher Tank - Handles multiple enemies efficiently
Uses data structures and NumPy for speed!
"""
import numpy as np
import math


class TargetingSystem:
    """Fast math utilities using NumPy"""
    
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
    
    def predict_positions(self, x, y, vx, vy, time):
        """Predict future position of ALL enemies"""
        future_x = x + vx * time
        future_y = y + vy * time
        return future_x, future_y


class EnemyTracker:
    """Track multiple enemies efficiently"""
    
    def __init__(self):
        self.enemy_ids = []
        self.x = np.array([])
        self.y = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])
        self.energy = np.array([])
        self.last_seen = np.array([])
    
    def update(self, enemy_id, x, y, vx, vy, energy, tick):
        """Add or update enemy"""
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
        """Remove old enemy data"""
        if len(self.enemy_ids) == 0:
            return
        
        age = current_tick - self.last_seen
        keep = age < max_age
        
        if not np.any(keep):
            self.__init__()  # Reset if nothing to keep
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


class SkirmisherTank:
    """
    Advanced tank for multi-enemy battles
    
    Uses data structures and NumPy for efficient
    tracking and targeting of many enemies at once!
    """
    
    def __init__(self):
        self.name = "SkirmisherTank"
        
        # Track all enemies
        self.enemies = EnemyTracker()
        
        # Utilities
        self.targeting = TargetingSystem()
        
        # State
        self.tick = 0
        self.radar_direction = 1
    
    def run(self):
        """Main loop"""
        self.tick += 1
        
        # Clean up old enemy data
        if self.tick % 20 == 0:
            self.enemies.cleanup(self.tick)
        
        # Movement - stay away from walls
        margin = 80
        if (self.x < margin or self.x > self.battlefield_width - margin or
            self.y < margin or self.y > self.battlefield_height - margin):
            self.turn_right(90)
        
        self.ahead(20)
        
        # Radar - sweep back and forth
        self.turn_radar_right(self.radar_direction * 45)
        if self.tick % 8 == 0:
            self.radar_direction *= -1
    
    def on_scanned_robot(self, scanned):
        """Add scanned enemy to our tracking system"""
        # Calculate velocity components
        heading_rad = math.radians(scanned.heading)
        vx = scanned.velocity * math.sin(heading_rad)
        vy = scanned.velocity * math.cos(heading_rad)
        
        # Update tracker
        self.enemies.update(
            enemy_id=scanned.name,
            x=scanned.x,
            y=scanned.y,
            vx=vx,
            vy=vy,
            energy=scanned.energy,
            tick=self.tick
        )
        
        # Find best target among ALL enemies
        self.engage_best_target()
    
    def engage_best_target(self):
        """Choose and shoot at the best target"""
        if self.enemies.count() == 0:
            return
        
        # Calculate distances to ALL enemies
        distances = self.targeting.calculate_distances(
            self.x, self.y,
            self.enemies.x, self.enemies.y
        )
        
        # Calculate scores for ALL enemies
        # Close + weak = high score
        scores = (1000 / (distances + 1)) + (100 - self.enemies.energy)
        
        # Find best target
        best_idx = np.argmax(scores)
        
        # Get target info
        target_x = self.enemies.x[best_idx]
        target_y = self.enemies.y[best_idx]
        target_vx = self.enemies.vx[best_idx]
        target_vy = self.enemies.vy[best_idx]
        target_distance = distances[best_idx]
        
        # Predict where target will be
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power
        time_to_hit = target_distance / bullet_speed
        
        future_x, future_y = self.targeting.predict_positions(
            np.array([target_x]),
            np.array([target_y]),
            np.array([target_vx]),
            np.array([target_vy]),
            time_to_hit
        )
        
        # Aim at predicted position
        angle = self.targeting.calculate_angles(
            self.x, self.y,
            future_x, future_y
        )[0]
        
        self.turn_gun_to(angle)
        
        # Choose power based on distance
        if target_distance < 150:
            self.fire(3)
        elif target_distance < 350:
            self.fire(2)
        else:
            self.fire(1)
    
    def on_hit_by_bullet(self, event):
        """React to being hit"""
        # Quick dodge
        self.turn_right(90)
        self.ahead(50)
```

## Part 8: Performance Comparison 📊

### Regular Python vs NumPy

```python
import time
import numpy as np
import math

# Test with 100 enemies
num_enemies = 100

# Generate random enemy positions
enemy_x_list = [random.randint(0, 800) for _ in range(num_enemies)]
enemy_y_list = [random.randint(0, 600) for _ in range(num_enemies)]
my_x, my_y = 400, 300

# Method 1: Regular Python loop
start = time.time()
distances_loop = []
for i in range(num_enemies):
    x_diff = enemy_x_list[i] - my_x
    y_diff = enemy_y_list[i] - my_y
    dist = math.sqrt(x_diff**2 + y_diff**2)
    distances_loop.append(dist)
loop_time = time.time() - start

# Method 2: NumPy arrays
enemy_x_array = np.array(enemy_x_list)
enemy_y_array = np.array(enemy_y_list)

start = time.time()
x_diff = enemy_x_array - my_x
y_diff = enemy_y_array - my_y
distances_numpy = np.sqrt(x_diff**2 + y_diff**2)
numpy_time = time.time() - start

print(f"Loop time: {loop_time*1000:.3f}ms")
print(f"NumPy time: {numpy_time*1000:.3f}ms")
print(f"NumPy is {loop_time/numpy_time:.1f}x faster!")

# Typical result:
# Loop time: 0.043ms
# NumPy time: 0.009ms
# NumPy is 4.8x faster!
```

## Part 9: Advanced Strategies 🧠

### Threat Assessment

```python
def assess_all_threats(tracker, my_x, my_y, my_energy):
    """
    Calculate threat level of ALL enemies
    
    Threat = how dangerous they are to us
    Consider: distance, their energy, their aim
    """
    if tracker.count() == 0:
        return np.array([])
    
    distances = calculate_all_distances(my_x, my_y, tracker.x, tracker.y)
    
    # Closer = more threatening
    distance_threat = 1000 / (distances + 1)
    
    # Higher energy = more threatening
    energy_threat = tracker.energy / 10
    
    # Combined threat
    total_threat = distance_threat + energy_threat
    
    return total_threat


def prioritize_targets(tracker, my_x, my_y):
    """
    Decide who to shoot based on multiple factors
    
    Strategy: High threat + low health = PRIORITY
    """
    if tracker.count() == 0:
        return None
    
    threats = assess_all_threats(tracker, my_x, my_y, 100)
    
    # Opportunity score = threatening AND weak
    opportunity = threats * (100 - tracker.energy) / 100
    
    best_target_idx = np.argmax(opportunity)
    return best_target_idx
```

### Multi-Target Tracking

```python
def can_hit_multiple_targets(tracker, my_x, my_y, my_angle, bullet_power=2):
    """
    Check if we can hit multiple enemies with one shot
    
    Find enemies that are lined up!
    """
    if tracker.count() < 2:
        return []
    
    # Calculate angles to ALL enemies
    angles = calculate_all_angles(my_x, my_y, tracker.x, tracker.y)
    
    # Find enemies within 5 degrees of our gun
    angle_diff = np.abs(angles - my_angle)
    angle_diff = np.minimum(angle_diff, 360 - angle_diff)  # Handle wraparound
    
    within_firing_cone = angle_diff < 5
    
    # Get indices of lined-up enemies
    lined_up = np.where(within_firing_cone)[0]
    
    return lined_up
```

### Resource Management

```python
def should_fire(my_energy, target_distance, target_energy, hit_probability):
    """
    Decide if shooting is worth it
    
    Don't waste energy on bad shots!
    """
    # Don't shoot if we're low on energy
    if my_energy < 20:
        return False
    
    # Only shoot if we have a decent chance
    if hit_probability < 0.3:
        return False
    
    # Don't waste energy on targets that are almost dead
    # (someone else might finish them)
    if target_energy < 10 and target_distance > 300:
        return False
    
    # Shoot if target is close and we're healthy
    if target_distance < 150 and my_energy > 50:
        return True
    
    # Conservative shot for distant targets
    if target_distance > 400 and my_energy < 40:
        return False
    
    return True
```

## Part 10: Testing Your Skirmisher 🎮

### Battle Against Multiple Enemies

```bash
# Test against several sample tanks at once
# (You'll need a battle runner that supports multi-tank battles)
python battle_runner.py Tutorials/Week7_AdvancedSkirmisher/skirmisher_tank.py --all-samples
```

### Comparing Performance

```python
# Add this to your tank to track performance
class SkirmisherTank:
    def __init__(self):
        # ... other initialization ...
        self.shots_fired = 0
        self.shots_hit = 0
        self.enemies_destroyed = 0
    
    def on_bullet_hit(self, event):
        """Track successful hits"""
        self.shots_hit += 1
        print(f"Hit! Accuracy: {self.shots_hit/self.shots_fired*100:.1f}%")
    
    def on_robot_death(self, event):
        """Track kills"""
        self.enemies_destroyed += 1
        print(f"Destroyed {event.name}! Total kills: {self.enemies_destroyed}")
```

## Part 11: Challenges and Experiments 🚀

### Easy Challenges:
1. **Enemy Counter Display** - Print how many enemies you're tracking each tick
2. **Closest Enemy Indicator** - Always show the distance to the nearest threat
3. **Weak Target Finder** - Highlight enemies with less than 30 energy
4. **Distance Histogram** - Count how many enemies are in close/medium/far range

### Medium Challenges:
1. **Priority Queue** - Keep a sorted list of top 5 targets
2. **Staleness Indicator** - Show which enemy data is oldest
3. **Energy Efficiency Tracker** - Calculate damage dealt per energy spent
4. **Radar Optimization** - Spend more time scanning areas with enemies

### Hard Challenges:
1. **Threat History** - Track which enemies hit you most often
2. **Escape Vector Calculator** - Find the direction with fewest enemies
3. **Ammo Conservation Mode** - Only shoot when hit probability > 60%
4. **Multi-Target Lock** - Track when 2+ enemies are close together

### Expert Challenge - Preview for Next Week!
**Anti-Gravity Movement** - Move away from enemy clusters!

```python
def calculate_anti_gravity_movement(my_x, my_y, tracker):
    """
    Calculate movement direction away from all enemies
    
    Each enemy exerts a "repulsive force" - closer = stronger push
    Think of enemies like magnets pushing you away!
    """
    if tracker.count() == 0:
        return 0  # No enemies, no force
    
    # Calculate distance to ALL enemies
    distances = calculate_all_distances(my_x, my_y, tracker.x, tracker.y)
    
    # Calculate angles to ALL enemies
    angles = calculate_all_angles(my_x, my_y, tracker.x, tracker.y)
    
    # Calculate "repulsive force" from each enemy
    # Closer enemies push harder!
    forces = 1000 / (distances + 1)
    
    # Convert forces to X and Y components
    force_x = np.sum(forces * np.sin(np.radians(angles)))
    force_y = np.sum(forces * np.cos(np.radians(angles)))
    
    # Calculate escape angle (opposite of total force)
    escape_angle = np.degrees(np.arctan2(-force_x, -force_y))
    
    return escape_angle

# Use it in your tank:
# escape_direction = calculate_anti_gravity_movement(self.x, self.y, self.enemies)
# self.turn_to(escape_direction)
# self.ahead(50)
```

This sets the stage for Week 8 where we'll explore:
- Anti-gravity movement patterns
- Cluster detection (finding groups of enemies)
- Formation recognition (are they working together?)
- Swarm intelligence (coordinating with allies!)

## Part 12: Understanding the Data Structures 📚

### Why Arrays Are Faster

```python
# Regular Python: CPU does one thing at a time
for i in range(1000):
    result[i] = data[i] * 2  # 1000 separate operations

# NumPy: CPU can do many things at once (vectorization)
result = data * 2  # One operation on all 1000 items!
```

### Memory Efficiency

```python
# Inefficient: 30 separate variables
enemy1_x = 100
enemy2_x = 200
# ... 28 more ...
enemy30_x = 450

# Efficient: One array
enemy_x = np.array([100, 200, ..., 450])  # All in one place!
```

### When to Use What

| Data Structure | Use When | Example |
|----------------|----------|---------|
| **List** | Small amount of data, flexible size | `enemies = [e1, e2, e3]` |
| **Dictionary** | Named data, different types | `enemy = {"x": 100, "health": 80}` |
| **NumPy Array** | Many numbers, math operations | `distances = np.array([...])` |
| **List of Dicts** | Complex objects, flexibility | `enemies = [{"x":100}, {"x":200}]` |
| **Multiple Arrays** | Parallel data, fast math | `x = np.array([...])`, `y = np.array([...])` |

## Part 13: Key Concepts Review 📖

### Data Structures
- **Definition**: Ways to organize and store data
- **Purpose**: Make data easy to access and manipulate
- **Types**: Lists, dictionaries, arrays, tuples

### Arrays
- **Definition**: Ordered collection of items of the same type
- **Purpose**: Store many related values together
- **Benefit**: Process many items at once

### NumPy
- **Definition**: Python library for fast numerical operations
- **Purpose**: Do math on lots of numbers quickly
- **Key Feature**: Vectorization (operate on entire arrays at once)

### Matrix Operations
- **Definition**: Mathematical operations on entire arrays
- **Purpose**: Calculate many things simultaneously
- **Example**: Calculate distance to 30 enemies in one operation

### Vectorization
- **Definition**: Operating on entire arrays instead of loops
- **Purpose**: Speed! Let the computer use all its power
- **Result**: Often 10-100x faster than loops

## Part 14: Real-World Applications 🌍

These concepts aren't just for tanks - they're used everywhere!

### Video Games
- Track thousands of particles in explosions
- Calculate AI for hundreds of enemies
- Process physics for all objects at once

### Data Science
- Analyze millions of rows of data
- Train machine learning models
- Create graphs and visualizations

### Science
- Simulate weather patterns
- Model molecular interactions
- Process telescope images

### Finance
- Analyze stock prices
- Calculate risk across portfolios
- High-frequency trading

## Part 15: Submit Your Skirmisher! 🏆

Ready to dominate multi-enemy battles?

1. Test against at least 5 enemies at once
2. Verify your tracking system works
3. Ensure performance is good (no lag)
4. Copy to `Submissions/YourName/skirmisher_tank.py`
5. Create Pull Request: `[Submission] YourName's Skirmisher Tank`

In your PR description:
```
## Skirmisher Tank Submission

**Tank Name:** SkirmisherTank
**Week:** Week 7 - Advanced Skirmisher

**Features:**
- Tracks up to 50 enemies simultaneously
- Uses NumPy for fast calculations
- Smart target selection based on threat + opportunity
- Efficient memory usage with array operations

**Performance:**
- Can handle 30+ enemies without lag
- Processes all enemies in < 1ms
- Accuracy: XX% against multiple targets

Data structures and vectorization make this tank ready for battle royale!
```

## Homework

Before moving on:
1. ✅ Install NumPy and test basic array operations
2. ✅ Implement EnemyTracker class
3. ✅ Test with at least 10 enemies
4. ✅ Compare performance: loops vs NumPy
5. ✅ Implement smart target selection
6. ✅ Submit your skirmisher tank

**Bonus**: Visualize all enemy positions and threats!

## Quick Reference

### NumPy Basics
```python
import numpy as np

# Create array
arr = np.array([1, 2, 3, 4, 5])

# Math on all elements
arr * 2          # [2, 4, 6, 8, 10]
arr + 10         # [11, 12, 13, 14, 15]
np.sqrt(arr)     # [1.0, 1.41, 1.73, 2.0, 2.24]

# Find min/max
np.min(arr)      # 1
np.max(arr)      # 5
np.argmin(arr)   # 0 (index of minimum)
np.argmax(arr)   # 4 (index of maximum)

# Boolean operations
arr > 3          # [False, False, False, True, True]
np.where(arr > 3)  # (array([3, 4]),) indices where true

# Statistics
np.mean(arr)     # 3.0
np.sum(arr)      # 15
```

### Distance Calculation (vectorized)
```python
def calculate_all_distances(my_x, my_y, enemy_x, enemy_y):
    x_diff = enemy_x - my_x
    y_diff = enemy_y - my_y
    return np.sqrt(x_diff**2 + y_diff**2)
```

### Angle Calculation (vectorized)
```python
def calculate_all_angles(my_x, my_y, enemy_x, enemy_y):
    x_diff = enemy_x - my_x
    y_diff = enemy_y - my_y
    return np.degrees(np.arctan2(x_diff, y_diff))
```

## Help!

**"NumPy won't install!"**
- Try: `pip install numpy`
- Or: `pip3 install numpy`
- Or: `python -m pip install numpy`

**"My arrays have different sizes!"**
- Make sure you're updating all arrays together
- Check that you're adding/removing from all arrays at once
- Use `len()` to verify sizes match

**"It's not faster!"**
- NumPy is faster for large datasets (100+ items)
- Make sure you're using array operations, not loops
- Profile your code to find bottlenecks

**"I'm getting NaN or infinity!"**
- Check for division by zero: use `(distance + 1)` instead of `distance`
- Check for negative square roots
- Use `np.isnan()` and `np.isinf()` to find problems

**"Too many enemies to track!"**
- Set a maximum (50-100 is reasonable)
- Remove old/distant enemies
- Prioritize closer threats

---

Congratulations! You can now handle massive battles efficiently! 🎉

You've learned professional data processing techniques used in real-world applications. These skills will help you build faster, smarter programs for any purpose!
