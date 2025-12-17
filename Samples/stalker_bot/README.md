# StalkerBot - Patient Sniper 👻

**Difficulty:** ★★★★☆ (Level 4)

## Overview

StalkerBot is a patient, calculating sniper that demonstrates advanced tactical concepts:
- **Target locking** - Picks one enemy and focuses on them
- **Kiting mechanics** - Maintains optimal sniping distance
- **Pattern recognition** - Detects when enemies move predictably
- **Selective firing** - Only shoots at easy targets

## Key Features

### 1. Linear Movement Detection

The bot tracks enemy positions over multiple scans and calculates if they're moving in a straight line:

```python
def detect_linear_movement(self):
    """Returns True if enemy's recent positions form a straight line"""
    # Compares movement vectors between positions
    # If all angles are within 20 degrees - it's linear!
```

**Why this matters:** Enemies moving linearly are easy to hit with prediction. Erratic enemies are harder.

### 2. Kiting Distance Management

Maintains optimal sniping range (350 pixels):

- **Too close (< 250):** Kite away while staying mobile
- **Optimal (250-500):** Strafe perpendicular to maintain range
- **Too far (> 500):** Close distance to get in range

```python
if distance < self.min_distance:
    retreat_angle = angle_to_target + 180  # Move away
elif distance > self.max_distance:
    self.turn_to(angle_to_target)  # Move closer
else:
    strafe_angle = angle_to_target + 90  # Circle
```

### 3. Selective Firing

Only fires when **both** conditions are met:
1. Enemy has moved linearly for 3+ consecutive scans
2. Gun is aimed within 15 degrees

```python
if self.consecutive_linear_scans >= 3 and abs(gun_turn) < 15:
    await self.fire(power)
```

## Strategy

1. **Lock onto first enemy** - Sticky targeting for consistency
2. **Track movement patterns** - Store last 5 positions
3. **Maintain distance** - Kite to optimal sniping range
4. **Wait for pattern** - Don't fire until enemy is predictable
5. **Snipe accurately** - Use prediction with tight aim tolerance

## Strengths

- ✓ Very accurate against predictable opponents
- ✓ Excellent energy efficiency (wastes no shots)
- ✓ Strong survivability through kiting
- ✓ Patient - doesn't panic
- ✓ Great wall avoidance while maneuvering

## Weaknesses

- ❌ May miss opportunities being too selective
- ❌ Struggles against erratic movement
- ❌ Sticky targeting (won't switch to better targets)
- ❌ Requires time to detect patterns
- ❌ Can be rushed by aggressive bots

## Good Matchups

**Beats:**
- WallsBot (very linear movement)
- SpinBot (predictable circular pattern)
- Sitting Duck (stationary = perfectly linear)

**Struggles against:**
- TrackerBot (ramming - no time to analyze)
- ChampionBot (unpredictable patterns)

## What You'll Learn

1. **Pattern Recognition** - How to detect predictable behavior
2. **Kiting Mechanics** - Maintaining distance while mobile
3. **Patience vs Aggression** - When to hold fire
4. **Distance Management** - Finding your optimal combat range
5. **Data Collection** - Using history to make decisions

## Testing

```bash
# Against predictable enemy (should dominate)
python stalker_bot.py Samples/walls_bot.py

# Against unpredictable enemy (challenging)
python stalker_bot.py Samples/champion_bot.py

# Test patience vs aggression
python stalker_bot.py Samples/tracker_bot.py
```

## Customization Ideas

1. **Adjust patience** - Lower `linear_threshold` from 3 to 2 for more aggression
2. **Change range** - Modify `optimal_distance` for different tactics
3. **Multi-targeting** - Remove sticky targeting to switch targets
4. **Improve detection** - Use velocity changes instead of just position
5. **Add circling** - Circle at optimal distance instead of strafing

## Advanced Concepts

### Why Linear Detection Matters

Linear movement = predictable! If an enemy moves in a straight line, simple linear prediction works perfectly:

```python
future_x = current_x + velocity_x * time
future_y = current_y + velocity_y * time
```

But if they're turning, changing speed, or dodging, this prediction fails!

### The Kiting Trade-off

- **Closer** = Higher damage but more danger
- **Farther** = Safer but bullets take longer (enemy can dodge)
- **Optimal** = Balance between safety and effectiveness

StalkerBot chooses **350 pixels** as its sweet spot - far enough to be safe, close enough to hit reliably.

---

**Pro Tip:** This bot teaches you that sometimes the best strategy is *not* to shoot. Wasting energy on low-probability shots makes you weaker!
