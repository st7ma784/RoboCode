# AdaptiveBot

**Field-Based Adaptive Movement with Predictive Shooting**

## Strategy Overview

AdaptiveBot uses a sophisticated field-based movement system that evaluates the entire battlefield and chooses optimal positions to move toward.

### Movement System

**Field Evaluation:**
1. Creates a grid overlay of the entire arena (20-unit resolution)
2. Assigns values to each grid cell based on multiple factors
3. Evaluates all positions reachable within 3 turns
4. Moves toward the highest-value safe position

**Forces Applied to Field:**

1. **Anti-Gravity Field**: 
   - Enemies create repulsion forces
   - Strength scales with enemy energy (healthier enemies = stronger repulsion)
   - Uses inverse square law: force = (threat × 5000) / (distance² + 100)
   - Keeps bot away from dangerous enemies

2. **Wall Penalties**:
   - Positions near walls (< 50 units) receive heavy penalties
   - Penalty increases as distance to wall decreases
   - Prevents bot from getting trapped against boundaries

3. **Bullet Track Penalties**:
   - Detects enemy bullets by monitoring energy drops (0.1-3.0 energy)
   - Projects bullet trajectory 50 ticks into the future
   - Marks entire bullet path as danger zone
   - Penalty decreases over time (bullets further away are less threatening)
   - Also marks adjacent cells for safety margin

4. **Movement Bonuses**:
   - Rewards positions that require movement (encourages not sitting still)
   - Bonuses based on distance from current position
   - Balances safety with aggressive positioning

### Shooting System

**Predictive Targeting:**
- Tracks enemy position and velocity
- Predicts future position based on bullet travel time
- Validates predicted position is within arena bounds

**Hit Probability Calculation:**
- Factors in:
  - Target distance (closer = better)
  - Target velocity (slower = better)
  - Bullet speed (power-dependent)
  - Time to impact
- Only fires when probability > 40% or target < 150 units

**Power Selection:**
- Close range (< 200): Power 3
- Medium range (< 400): Power 2
- Long range: Power 1

**Target Selection:**
- Prioritizes enemies based on:
  - Distance (closer = higher priority)
  - Energy (weaker = higher priority)
- Focuses fire on most vulnerable target

## Key Features

✅ **Dynamic Field Analysis** - Evaluates entire battlefield every tick  
✅ **Multi-Factor Decision Making** - Considers enemies, walls, and bullets  
✅ **Bullet Dodging** - Detects and avoids incoming fire  
✅ **Predictive Shooting** - Leads moving targets  
✅ **Conservative Firing** - Only shoots when probability is good  
✅ **3-Turn Planning** - Looks ahead to find safe positions  

## Technical Details

**Grid Resolution**: 20 units per cell  
**Search Radius**: 24 units (8 speed × 3 turns)  
**Evaluation Angles**: Every 15° (24 directions)  
**Bullet Tracking**: 50 tick projection  
**Fire Threshold**: 40% hit probability  

## Strengths

- Excellent at avoiding multiple threats simultaneously
- Never gets trapped against walls
- Dodges bullets by avoiding their projected paths
- Conservative shooting reduces wasted energy
- Adapts to any number of enemies

## Weaknesses

- Field calculation is computationally intensive
- May be overly cautious in 1v1 situations
- Grid resolution limits precision
- Bullet detection relies on energy monitoring (doesn't see bullets directly)

## Running the Bot

```bash
cd Submissions/AdaptiveBot
python adaptive_bot.py
```

Then start a battle in the RoboCode Tank Royale GUI.

## Algorithm Complexity

- **Field Creation**: O(w × h) where w,h are grid dimensions
- **Enemy Repulsion**: O(w × h × n) where n is number of enemies
- **Wall Penalties**: O(w × h)
- **Bullet Penalties**: O(w × h × b) where b is number of bullets
- **Position Search**: O(k) where k is search positions (~72 positions)

Total per tick: O(w × h × (n + b) + k) ≈ O(3600 + k) with default settings

## Future Improvements

- Adaptive field resolution based on bot count
- Learning system to adjust field weights
- Cluster detection for team battles
- More sophisticated bullet trajectory prediction
- Energy management for power selection
