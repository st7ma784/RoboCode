# Battle Strategies for Tank Commanders ⚔️

Master the art of tank warfare! This guide covers movement patterns, combat tactics, and winning strategies.

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Movement Patterns](#movement-patterns)
3. [Targeting Strategies](#targeting-strategies)
4. [Defensive Tactics](#defensive-tactics)
5. [Energy Management](#energy-management)
6. [Situational Strategy](#situational-strategy)
7. [Advanced Techniques](#advanced-techniques)

---

## Core Concepts

### The Three Pillars of Tank Combat

1. **Movement** - Don't be predictable
2. **Targeting** - Hit your opponent
3. **Energy** - Manage your resources

**Golden Rule:** The tank that hits more while getting hit less wins!

### Understanding the Battle

Every battle has three phases:

**Phase 1: Early Game (Energy > 70)**
- Explore and locate enemy
- Establish position
- Test enemy behavior

**Phase 2: Mid Game (Energy 30-70)**
- Active combat
- Tactical positioning
- Energy conservation

**Phase 3: End Game (Energy < 30)**
- Survival mode
- Careful shots only
- Defensive movement

---

## Movement Patterns

### Pattern 1: Circular Movement

**Use when:** General purpose, maintaining distance

```python
def circular_movement(self):
    """Move in a large circle"""
    self.ahead(50)
    self.turn_right(15)
```

**Pros:**
- Simple and reliable
- Good for scanning
- Maintains distance from walls

**Cons:**
- Predictable
- Easy to track

---

### Pattern 2: Zigzag Movement

**Use when:** Dodging bullets, unpredictable movement

```python
def zigzag_movement(self):
    """Zigzag pattern"""
    self.ahead(80)

    # Random direction
    if random.random() < 0.5:
        self.turn_right(30)
    else:
        self.turn_left(30)
```

**Pros:**
- Harder to predict
- Good for dodging
- Covers ground quickly

**Cons:**
- Can lead to walls
- Less smooth

---

### Pattern 3: Wall Following

**Use when:** Defensive play, protecting your back

```python
def follow_wall(self):
    """Stay near walls"""
    if self.too_far_from_wall():
        self.move_to_nearest_wall()
    else:
        self.ahead(50)
        if self.wall_ahead():
            self.turn_right(90)
```

**Pros:**
- Walls protect one side
- Limits enemy positions
- Good for corners

**Cons:**
- Predictable path
- Can be cornered
- Limited escape routes

---

### Pattern 4: Random Walk

**Use when:** Maximum unpredictability needed

```python
def random_walk(self):
    """Completely random movement"""
    distance = random.randint(30, 100)
    self.ahead(distance)

    angle = random.randint(-45, 45)
    if angle < 0:
        self.turn_left(abs(angle))
    else:
        self.turn_right(angle)
```

**Pros:**
- Very hard to predict
- Confuses pattern-learning opponents
- Flexible

**Cons:**
- May hit walls
- No tactical positioning
- Can be inefficient

---

### Pattern 5: Spiral Movement

**Use when:** Searching, interesting visual pattern

```python
def spiral_movement(self):
    """Expanding spiral"""
    time = self.time
    distance = 20 + (time % 100)
    self.ahead(distance)
    self.turn_right(20)
```

**Pros:**
- Covers area systematically
- Increasing radius
- Artistic!

**Cons:**
- Eventually hits walls
- Can be predicted
- Complex to manage

---

### Pattern 6: Stop and Go

**Use when:** Breaking enemy prediction

```python
def stop_and_go(self):
    """Unpredictable stops"""
    if random.random() < 0.2:
        # 20% chance to stop and spin
        self.turn_right(random.randint(90, 180))
    else:
        # Keep moving
        self.ahead(60)
        self.turn_right(10)
```

**Pros:**
- Breaks prediction
- Surprise factor
- Good for aiming

**Cons:**
- Being stationary is risky
- Less area coverage

---

## Targeting Strategies

### Strategy 1: Direct Fire

**When:** Enemy is stationary or very close

```python
def direct_fire(self, enemy_x, enemy_y):
    """Shoot at current position"""
    angle = self.calculate_angle(self.x, self.y, enemy_x, enemy_y)
    self.turn_gun_to(angle)
    self.fire(3)  # Max power for stationary target
```

**Best for:**
- Close range (< 100 pixels)
- Non-moving targets
- Guaranteed hits

---

### Strategy 2: Linear Prediction

**When:** Enemy moving in straight line

```python
def linear_prediction(self, enemy_x, enemy_y, velocity, heading, bullet_power):
    """Predict linear movement"""
    # Calculate bullet travel time
    distance = self.calculate_distance(self.x, self.y, enemy_x, enemy_y)
    bullet_speed = 20 - (3 * bullet_power)
    time_to_hit = distance / bullet_speed

    # Predict position
    future_x, future_y = self.predict_position(
        enemy_x, enemy_y, velocity, heading, time_to_hit
    )

    # Aim and fire
    angle = self.calculate_angle(self.x, self.y, future_x, future_y)
    self.turn_gun_to(angle)
    self.fire(bullet_power)
```

**Best for:**
- Medium range (100-400 pixels)
- Predictable enemies
- Standard combat

---

### Strategy 3: Statistical Targeting

**When:** Enemy has patterns

```python
def statistical_targeting(self):
    """Learn enemy patterns"""
    # Track enemy positions
    self.enemy_history.append((enemy_x, enemy_y, time))

    # Find most common positions
    # (Simplified example)
    if len(self.enemy_history) > 20:
        # Aim at most frequent position
        target = self.find_common_position()
        self.aim_at(target)
```

**Best for:**
- Long battles
- Pattern-based enemies
- Advanced play

---

## Defensive Tactics

### Tactic 1: Immediate Dodge

**When:** You get hit

```python
def on_hit_by_bullet(self, bullet):
    """Quick evasive action"""
    dodge_choice = random.randint(1, 3)

    if dodge_choice == 1:
        # Quick turn and advance
        self.turn_right(90)
        self.ahead(100)
    elif dodge_choice == 2:
        # Retreat
        self.back(80)
    else:
        # Spin and move
        self.turn_left(135)
        self.ahead(80)
```

---

### Tactic 2: Strafing

**When:** Maintaining distance while dodging

```python
def strafe(self, enemy_x, enemy_y):
    """Move perpendicular to enemy"""
    # Calculate angle to enemy
    angle_to_enemy = self.calculate_angle(
        self.x, self.y, enemy_x, enemy_y
    )

    # Turn perpendicular (90° offset)
    self.turn_to(angle_to_enemy + 90)

    # Move
    self.ahead(50)
```

---

### Tactic 3: Retreat Under Fire

**When:** Low energy or overwhelmed

```python
def retreat(self, enemy_x, enemy_y):
    """Run away from enemy"""
    # Calculate angle TO enemy
    angle_to_enemy = self.calculate_angle(
        self.x, self.y, enemy_x, enemy_y
    )

    # Turn opposite direction
    escape_angle = angle_to_enemy + 180

    self.turn_to(escape_angle)
    self.ahead(100)

    # Shoot while retreating (optional)
    self.fire(1)  # Low power to save energy
```

---

## Energy Management

### Energy Levels and Behavior

```python
def choose_behavior(self):
    """Adapt to energy level"""
    if self.energy > 80:
        return "aggressive"
    elif self.energy > 50:
        return "balanced"
    elif self.energy > 20:
        return "conservative"
    else:
        return "survival"
```

### Aggressive (Energy > 80)

```python
# High energy = take risks
if behavior == "aggressive":
    # Use max power
    self.fire(3)
    # Chase enemy
    self.move_toward_enemy()
    # Don't worry about hits
```

### Balanced (Energy 50-80)

```python
# Medium energy = smart play
if behavior == "balanced":
    # Power based on distance
    power = 2 if distance < 300 else 1
    self.fire(power)
    # Tactical positioning
    self.maintain_distance()
```

### Conservative (Energy 20-50)

```python
# Low energy = careful
if behavior == "conservative":
    # Only shoot good opportunities
    if hit_probability > 0.6:
        self.fire(2)
    # Focus on dodging
    self.defensive_movement()
```

### Survival (Energy < 20)

```python
# Critical energy = stay alive
if behavior == "survival":
    # Minimal shooting
    if distance < 100:  # Only point-blank
        self.fire(1)
    # Maximum evasion
    self.dodge()
    self.dodge()
    self.dodge()
```

---

## Situational Strategy

### Situation 1: Found Enemy Early

```python
if enemy_spotted and self.time < 100:
    # Early game - establish position
    # Don't rush in
    self.maintain_distance(optimal=250)
    # Conservative fire
    self.fire(2)
```

### Situation 2: Lost Enemy

```python
if not enemy_recently_seen:
    # Search pattern
    self.turn_radar_right(45)  # Faster scan
    # Move to center for better view
    self.move_to_center()
```

### Situation 3: Enemy Low on Energy

```python
if enemy_energy < 20 and self.energy > 50:
    # Finish them!
    # Aggressive pursuit
    self.chase_enemy()
    # Maximum firepower
    self.fire(3)
```

### Situation 4: You're Losing

```python
if self.energy < enemy_energy * 0.5:
    # Underdog tactics
    # Maximum unpredictability
    self.random_walk()
    # Only perfect shots
    if hit_probability > 0.8:
        self.fire(3)
```

### Situation 5: Corner Trap

```python
if self.in_corner():
    # Emergency corner escape
    # Turn toward center
    center_angle = self.angle_to_center()
    self.turn_to(center_angle)
    # Full speed escape
    self.ahead(150)
```

---

## Advanced Techniques

### Technique 1: Oscillation

Move side-to-side to dodge:

```python
def oscillate(self):
    """Wiggle movement"""
    if self.time % 20 < 10:
        self.turn_right(10)
    else:
        self.turn_left(10)
    self.ahead(30)
```

### Technique 2: Minimum Risk Point

Find safest position:

```python
def find_safe_position(self, enemy_x, enemy_y):
    """Calculate safest spot"""
    # Want to be:
    # - Far from enemy
    # - Not near walls
    # - Good firing angle

    # Simplified: opposite side from enemy
    safe_x = battlefield_width - enemy_x
    safe_y = battlefield_height - enemy_y

    return safe_x, safe_y
```

### Technique 3: Wave Surfing (Advanced)

Dodge predicted bullets:

```python
def wave_surfing(self, enemy_x, enemy_y, bullet_speed):
    """Predict and dodge bullet waves"""
    # Calculate when bullet will arrive
    distance = self.calculate_distance(self.x, self.y, enemy_x, enemy_y)
    time_to_hit = distance / bullet_speed

    # Move perpendicular to dodge
    if time_to_hit < 20:  # Bullet incoming!
        self.strafe(enemy_x, enemy_y)
```

### Technique 4: Radar Lock

Keep radar on enemy:

```python
def lock_radar(self, enemy_bearing):
    """Keep radar pointed at enemy"""
    # Bearing is relative angle to enemy
    # Small adjustments keep radar locked
    self.turn_radar_right(enemy_bearing)
```

---

## Putting It All Together

### Example: Complete Strategy

```python
class StrategicTank:
    def run(self):
        # Choose behavior based on energy
        behavior = self.choose_behavior()

        # Choose movement based on situation
        if self.is_too_close_to_wall(50):
            self.avoid_walls()
        elif behavior == "aggressive":
            self.zigzag_movement()
        elif behavior == "balanced":
            self.circular_movement()
        else:
            self.random_walk()

        # Always keep scanning
        self.turn_radar_right(45)

    def on_scanned_robot(self, enemy):
        # Choose targeting based on distance
        distance = enemy.distance

        if distance < 100:
            # Close combat - direct fire
            self.direct_fire(enemy.x, enemy.y)
        else:
            # Medium/long range - predict
            self.linear_prediction(
                enemy.x, enemy.y,
                enemy.velocity, enemy.heading,
                bullet_power=2
            )

    def on_hit_by_bullet(self, bullet):
        # Immediate dodge
        self.emergency_dodge()

        # Maybe retreat if low energy
        if self.energy < 30:
            self.retreat_mode = True
```

---

## Strategy Matrix

| Situation | Movement | Targeting | Power | Priority |
|-----------|----------|-----------|-------|----------|
| Early game, high energy | Circular | Linear prediction | 2 | Positioning |
| Mid game, even energy | Zigzag | Advanced prediction | 2 | Accuracy |
| Low energy | Random walk | High probability only | 1 | Survival |
| Enemy low energy | Chase | Direct fire | 3 | Finish |
| Near wall | Avoid | Opportunistic | 1-2 | Escape |
| Corner trap | Emergency escape | Don't shoot | 0 | Survival |

---

## Common Mistakes

### Mistake 1: Being Too Predictable
**Problem:** Always moving in circles
**Solution:** Change patterns every 30-50 ticks

### Mistake 2: Wasting Energy
**Problem:** Shooting when hit probability is low
**Solution:** Only shoot when probability > 40%

### Mistake 3: Ignoring Walls
**Problem:** Running into corners
**Solution:** Check boundaries before moving

### Mistake 4: Tunnel Vision
**Problem:** Focusing only on shooting
**Solution:** Balance shooting, movement, and dodging

### Mistake 5: Wrong Power Levels
**Problem:** Using power 3 at long range
**Solution:** Power 1 for long, 2 for medium, 3 for close

---

## Advanced: AI-Powered Strategy Learning

Once you've mastered hand-coded strategies, consider letting AI discover optimal tactics:

### Genetic Algorithms (Week 10)
- **Evolve** combat parameters over generations
- **Automatically find** optimal aggression, range preferences, dodge intensity
- **No manual tuning** - the algorithm discovers what works
- **Best for:** Finding global optimal parameter sets

### Q-Learning (Week 11)
- **Learn** from battle experience in real-time
- **Adapt** tactics based on opponent behavior
- **Discover** non-obvious state-action patterns
- **Best for:** Opponent-specific tactical adaptation

See **[AI & Machine Learning Guide](ai_learning_guide.md)** for details!

---

## Practice Drills

### Drill 1: Movement Mastery
Practice each movement pattern for 100 ticks without hitting walls.

### Drill 2: Target Practice
Shoot at SittingDuck - aim for 80%+ accuracy.

### Drill 3: Dodging
Let SpinBot shoot at you - minimize hits taken.

### Drill 4: Energy Management
Win a battle using minimum bullets (maximize efficiency).

### Drill 5: Adaptability
Change strategies mid-battle based on situation.

### Drill 6: AI Optimization (Advanced)
Use genetic algorithms to evolve your tank's parameters automatically.

---

## Final Tips

1. **Study Your Replays** - Watch battles to learn
2. **Test Against Different Opponents** - Each requires different strategy
3. **Iterate and Improve** - Keep refining your approach
4. **Balance All Three Pillars** - Movement, targeting, energy
5. **Consider AI Learning** - For advanced optimization
6. **Have Fun!** - The best strategy is one you enjoy

---

Remember: There's no single "best" strategy. The best tank adapts to its opponent!

Now go forth and dominate the arena! ⚔️
