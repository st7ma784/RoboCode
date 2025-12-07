# Week 5: Master Targeting! 🎯

Welcome to the final week! You'll become a targeting master by learning:
1. How to choose the right bullet power
2. Calculating hit probability
3. Simulating shots before firing
4. Energy management and strategy

## Part 1: Understanding Bullet Power (15 minutes)

### The Three Powers

RoboCode bullets can have power from 1 to 3:

| Power | Speed | Damage to Enemy | Energy Cost | Damage to You if Enemy Hits You |
|-------|-------|-----------------|-------------|----------------------------------|
| 1     | 17    | 4              | 1           | 4                                |
| 2     | 14    | 8              | 2           | 8                                |
| 3     | 11    | 12             | 3           | 12                               |

**Formula:**
```python
bullet_speed = 20 - (3 * power)
damage_dealt = 4 * power
energy_cost = power
```

### When to Use Each Power?

**Power 1 (Fast & Weak):**
- Long distance shots
- Fast-moving enemies
- When you're low on energy
- When hit probability is low

**Power 2 (Balanced):**
- Medium range
- Most general situations
- Good balance of speed and damage
- Your default choice

**Power 3 (Slow & Strong):**
- Very close range
- Stationary or slow targets
- When you have lots of energy
- Finishing blow to destroy enemy

## Part 2: Calculating Hit Probability (25 minutes)

### What Affects Hit Probability?

Several factors determine if you'll hit:

1. **Distance** - Farther = harder to hit
2. **Enemy Speed** - Faster = harder to hit
3. **Bullet Speed** - Slower bullets give enemy more time to dodge
4. **Prediction Accuracy** - Are they moving predictably?

### Simple Probability Formula

```python
def calculate_hit_probability(distance, enemy_velocity, bullet_power):
    """
    Estimate probability of hitting target (0.0 to 1.0)

    distance: how far away enemy is
    enemy_velocity: how fast enemy is moving
    bullet_power: power of bullet (1-3)
    """
    # Calculate bullet speed
    bullet_speed = 20 - (3 * bullet_power)

    # Time for bullet to reach target
    time_to_hit = distance / bullet_speed

    # How far will enemy move in that time?
    enemy_movement = enemy_velocity * time_to_hit

    # If enemy moves less than their width (36 pixels), likely hit!
    # More movement = lower probability
    if enemy_movement < 36:
        probability = 1.0  # 100% chance
    elif enemy_movement > 200:
        probability = 0.1  # 10% chance
    else:
        # Linear scale between 36 and 200
        probability = 1.0 - ((enemy_movement - 36) / 164)

    # Distance penalty
    if distance > 400:
        probability *= 0.7  # 30% penalty for long distance
    elif distance > 600:
        probability *= 0.5  # 50% penalty for very long distance

    # Clamp between 0 and 1
    return max(0.0, min(1.0, probability))
```

### Using Hit Probability

```python
def on_scanned_robot(self, scanned_robot):
    """Smart shooting based on probability"""
    distance = scanned_robot.distance
    velocity = scanned_robot.velocity

    # Try each power level
    prob_power1 = calculate_hit_probability(distance, velocity, 1)
    prob_power2 = calculate_hit_probability(distance, velocity, 2)
    prob_power3 = calculate_hit_probability(distance, velocity, 3)

    print(f"Hit probabilities - P1: {prob_power1:.1%}, P2: {prob_power2:.1%}, P3: {prob_power3:.1%}")

    # Choose power with best expected damage
    # Expected damage = probability × damage
    expected_dmg_1 = prob_power1 * 4
    expected_dmg_2 = prob_power2 * 8
    expected_dmg_3 = prob_power3 * 12

    # Pick the best one
    if expected_dmg_3 > expected_dmg_2 and expected_dmg_3 > expected_dmg_1:
        power = 3
    elif expected_dmg_2 > expected_dmg_1:
        power = 2
    else:
        power = 1

    print(f"Choosing power {power}")
    self.fire(power)
```

## Part 3: Simulating Shots (25 minutes)

### Why Simulate?

Before wasting energy, check if the shot will:
- Hit the target
- Hit a wall instead
- Be worth the energy cost

### Shot Simulation

```python
def simulate_shot(self, target_x, target_y, bullet_power):
    """
    Simulate a bullet traveling to target

    Returns: (will_hit, hit_x, hit_y)
    """
    # Calculate angle to target
    angle = self.calculate_angle(self.x, self.y, target_x, target_y)
    angle_rad = math.radians(angle)

    # Bullet speed
    bullet_speed = 20 - (3 * bullet_power)

    # Simulate bullet path
    bullet_x = self.x
    bullet_y = self.y

    # Step through bullet trajectory
    for step in range(100):  # Max 100 steps
        # Move bullet
        bullet_x += bullet_speed * math.sin(angle_rad)
        bullet_y += bullet_speed * math.cos(angle_rad)

        # Check if hit wall
        if (bullet_x < 0 or bullet_x > self.battlefield_width or
            bullet_y < 0 or bullet_y > self.battlefield_height):
            return (False, bullet_x, bullet_y)  # Hit wall

        # Check if reached target area
        distance_to_target = math.sqrt(
            (bullet_x - target_x)**2 +
            (bullet_y - target_y)**2
        )

        if distance_to_target < 20:  # Within hit range
            return (True, bullet_x, bullet_y)  # Will hit!

    return (False, bullet_x, bullet_y)  # Went too far
```

### Using Simulation

```python
def on_scanned_robot(self, scanned_robot):
    """Only shoot if simulation shows we'll hit"""
    # Predict where enemy will be
    future_x, future_y = self.predict_position(
        scanned_robot.x,
        scanned_robot.y,
        scanned_robot.velocity,
        scanned_robot.heading,
        time_to_hit
    )

    # Simulate shot
    will_hit, hit_x, hit_y = self.simulate_shot(future_x, future_y, 2)

    if will_hit:
        print("✓ Simulation passed - taking shot!")
        angle = self.calculate_angle(self.x, self.y, future_x, future_y)
        self.turn_gun_to(angle)
        self.fire(2)
    else:
        print("✗ Simulation failed - would miss")
        # Don't waste energy!
```

## Part 4: Energy Management (20 minutes)

### Tracking Energy

```python
def __init__(self):
    self.name = "SniperBot"
    self.energy = 100
    self.enemy_energy = None  # Track enemy energy

def on_scanned_robot(self, scanned_robot):
    """Track enemy energy changes"""
    if self.enemy_energy is not None:
        # Did enemy lose energy?
        energy_drop = self.enemy_energy - scanned_robot.energy

        if energy_drop > 0 and energy_drop <= 3:
            print(f"Enemy fired! Power ~{energy_drop}")
            # They just shot - might be good time to move!

        if energy_drop >= 4:
            print(f"Enemy took damage: {energy_drop}")

    # Update tracked energy
    self.enemy_energy = scanned_robot.energy
```

### Energy-Based Strategy

```python
def choose_strategy(self):
    """Adapt strategy based on energy levels"""
    if self.energy > 80:
        return "aggressive"  # We can afford to take risks
    elif self.energy > 50:
        return "balanced"    # Play it smart
    elif self.energy > 20:
        return "defensive"   # Be careful!
    else:
        return "survival"    # Just stay alive!

def on_scanned_robot(self, scanned_robot):
    """Energy-aware shooting"""
    strategy = self.choose_strategy()
    distance = scanned_robot.distance

    if strategy == "aggressive":
        # Shoot often, high power
        if distance < 200:
            self.fire(3)
        else:
            self.fire(2)

    elif strategy == "balanced":
        # Smart power choices
        if distance < 150 and scanned_robot.velocity < 4:
            self.fire(3)  # Good opportunity
        else:
            self.fire(2)  # Safe choice

    elif strategy == "defensive":
        # Only shoot when probability is high
        prob = self.calculate_hit_probability(distance, scanned_robot.velocity, 2)
        if prob > 0.6:  # 60% chance or better
            self.fire(2)

    else:  # survival
        # Only shoot at close, easy targets
        if distance < 100 and scanned_robot.velocity < 3:
            self.fire(1)  # Save energy
```

## Part 5: Your Master Tank - "SniperBot"

Create `sniper_bot.py` - combining everything you've learned!

```python
"""
SniperBot - The ultimate targeting machine!

Combines:
- Smart power selection
- Hit probability calculation
- Shot simulation
- Energy management
- All previous week's skills
"""
import math
import random

class SniperBot:
    def __init__(self):
        self.name = "SniperBot"
        # Position
        self.x = 0
        self.y = 0
        self.heading = 0
        self.energy = 100
        self.battlefield_width = 800
        self.battlefield_height = 600

        # Statistics
        self.shots_fired = 0
        self.shots_hit = 0
        self.enemy_energy = None

    def run(self):
        """Main loop"""
        # Safe movement (from Week 3)
        if not self.is_too_close_to_wall(50):
            self.ahead(40)
            self.turn_right(15)
        else:
            self.avoid_walls()

        # Radar sweep
        self.turn_radar_right(45)

    def on_scanned_robot(self, scanned_robot):
        """Advanced targeting system"""
        distance = scanned_robot.distance
        velocity = scanned_robot.velocity

        # Calculate best power based on probability
        power = self.choose_optimal_power(distance, velocity)

        # Predict enemy position
        bullet_speed = 20 - (3 * power)
        time_to_hit = distance / bullet_speed

        future_x, future_y = self.predict_position(
            scanned_robot.x,
            scanned_robot.y,
            velocity,
            scanned_robot.heading,
            time_to_hit
        )

        # Validate prediction
        if not self.is_valid_target(future_x, future_y):
            # Use current position instead
            future_x, future_y = scanned_robot.x, scanned_robot.y

        # Simulate shot
        will_hit, _, _ = self.simulate_shot(future_x, future_y, power)

        # Only shoot if simulation looks good
        if will_hit or distance < 100:  # Always shoot at close range
            angle = self.calculate_angle(self.x, self.y, future_x, future_y)
            self.turn_gun_to(angle)
            self.fire(power)
            self.shots_fired += 1

            hit_prob = self.calculate_hit_probability(distance, velocity, power)
            print(f"🎯 Shot #{self.shots_fired}: Power {power}, Prob {hit_prob:.1%}")
        else:
            print("⏸️  Holding fire - low hit probability")

        # Track enemy energy
        if self.enemy_energy is not None:
            energy_drop = self.enemy_energy - scanned_robot.energy
            if 0 < energy_drop <= 3:
                print(f"⚠️  Enemy fired! Dodging...")
                self.dodge()
        self.enemy_energy = scanned_robot.energy

    def choose_optimal_power(self, distance, velocity):
        """Choose power that maximizes expected damage"""
        # Consider our energy
        if self.energy < 20:
            max_power = 1
        elif self.energy < 50:
            max_power = 2
        else:
            max_power = 3

        # Calculate expected damage for each power
        best_power = 1
        best_expected_dmg = 0

        for power in range(1, max_power + 1):
            prob = self.calculate_hit_probability(distance, velocity, power)
            damage = 4 * power
            expected = prob * damage

            if expected > best_expected_dmg:
                best_expected_dmg = expected
                best_power = power

        return best_power

    def calculate_hit_probability(self, distance, velocity, power):
        """Estimate hit probability"""
        bullet_speed = 20 - (3 * power)
        time_to_hit = distance / bullet_speed
        enemy_movement = velocity * time_to_hit

        # Base probability from movement
        if enemy_movement < 36:
            prob = 1.0
        elif enemy_movement > 200:
            prob = 0.1
        else:
            prob = 1.0 - ((enemy_movement - 36) / 164)

        # Distance penalty
        if distance > 400:
            prob *= 0.7
        elif distance > 600:
            prob *= 0.5

        return max(0.0, min(1.0, prob))

    def simulate_shot(self, target_x, target_y, power):
        """Simulate bullet path"""
        angle = self.calculate_angle(self.x, self.y, target_x, target_y)
        angle_rad = math.radians(angle)
        bullet_speed = 20 - (3 * power)

        bullet_x = self.x
        bullet_y = self.y

        for _ in range(100):
            bullet_x += bullet_speed * math.sin(angle_rad)
            bullet_y += bullet_speed * math.cos(angle_rad)

            # Hit wall?
            if (bullet_x < 0 or bullet_x > self.battlefield_width or
                bullet_y < 0 or bullet_y > self.battlefield_height):
                return (False, bullet_x, bullet_y)

            # Hit target?
            dist = math.sqrt((bullet_x - target_x)**2 + (bullet_y - target_y)**2)
            if dist < 25:
                return (True, bullet_x, bullet_y)

        return (False, bullet_x, bullet_y)

    def predict_position(self, x, y, velocity, heading, time):
        """Predict future position"""
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y

    def dodge(self):
        """Quick evasive maneuver"""
        if random.random() < 0.5:
            self.turn_right(90)
        else:
            self.turn_left(90)
        self.ahead(80)

    def is_too_close_to_wall(self, margin):
        """From Week 3"""
        return (self.x < margin or
                self.x > self.battlefield_width - margin or
                self.y < margin or
                self.y > self.battlefield_height - margin)

    def avoid_walls(self):
        """From Week 3"""
        self.back(50)
        self.turn_right(90)

    def is_valid_target(self, x, y):
        """From Week 3"""
        margin = 20
        return (margin < x < self.battlefield_width - margin and
                margin < y < self.battlefield_height - margin)

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """From Week 2"""
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    def on_hit_by_bullet(self, bullet):
        """Track accuracy"""
        print(f"💥 Hit! Energy: {self.energy}")
        self.dodge()

    def on_bullet_hit(self, bullet_hit):
        """Track our hits"""
        self.shots_hit += 1
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"✓ HIT! Accuracy: {accuracy:.1f}%")

    def on_win(self, event):
        """Victory!"""
        accuracy = (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0
        print(f"🏆 VICTORY! Final accuracy: {accuracy:.1f}%")

    # Game engine methods
    def ahead(self, distance):
        pass
    def back(self, distance):
        pass
    def turn_right(self, degrees):
        pass
    def turn_left(self, degrees):
        pass
    def turn_radar_right(self, degrees):
        pass
    def turn_gun_to(self, angle):
        pass
    def fire(self, power):
        pass
```

## Part 6: Challenges

### Easy:
1. **Accuracy Tracker**: Display hit percentage after each shot
2. **Power Logger**: Track how often you use each power level
3. **Energy Display**: Print energy levels every 50 ticks

### Medium:
1. **Adaptive Probability**: Adjust probability calculation based on actual hit rate
2. **Energy Prediction**: Predict when enemy will run out of energy
3. **Multi-Target**: Handle multiple enemies with priority system

### Hard:
1. **Machine Learning**: Learn enemy movement patterns and improve predictions
2. **Probability Map**: Create a 2D grid of hit probabilities
3. **Perfect Shot**: Combine all techniques for maximum accuracy

## Final Project

Create your ultimate tank combining ALL 5 weeks:
- Week 1: Basic movement and shooting
- Week 2: Trigonometry and prediction
- Week 3: Boundary checking
- Week 4: Unpredictable movement
- Week 5: Advanced targeting

## You Did It! 🎉

Congratulations! You've completed all 5 weeks and learned:
- Python programming basics
- Trigonometry and geometry
- Decision-making with if-statements
- Random numbers and strategy
- Probability and simulation

## What's Next?

1. **Test your tanks** in the Submissions folder
2. **Study the samples** to learn new tricks
3. **Read the guides** for deeper understanding
4. **Join competitions** with other students
5. **Invent new strategies** and share them!

---

You're now a RoboCode master! 🏆

Sources:
- [Robocode.py](https://github.com/scilicet64/robocode.py)
- [Robocode Tank Royale](https://github.com/robocode-dev/tank-royale)
- [Robocode Tank Royale Docs](https://robocode-dev.github.io/tank-royale/)
