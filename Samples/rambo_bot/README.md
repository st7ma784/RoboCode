# Rambo - The Perimeter Sharpshooter

## Strategy Overview

Rambo implements an innovative firing strategy that inverts the traditional aim-then-shoot approach:

### Traditional Bot Strategy
1. Detect enemy
2. Calculate where enemy will be
3. Aim gun at predicted position
4. Choose power and fire

### Rambo's Strategy
1. Patrol the walls, firing inward
2. Keep gun pointing toward center with minimal movement
3. Detect enemy
4. Calculate when enemy will **cross the current firing line**
5. **Vary bullet power** so bullet arrives exactly when enemy crosses
6. Fire with calculated power

## How It Works

### Movement
- Patrols around the arena perimeter (wall-following)
- Maintains consistent distance from walls
- Reverses direction when hitting corners or obstacles

### Gun Control
- Points generally toward arena center
- Minimal gun movement (slow 15-degree sweep)
- Gun aim is treated as a **fixed firing line**, not actively tracking

### Firing Algorithm

When an enemy is detected, Rambo:

1. **Ray Intersection Calculation**
   - Gun firing line: Ray from bot position in gun direction
   - Enemy trajectory: Ray from enemy position in enemy's movement direction
   - Calculates intersection point of these two rays

2. **Timing Calculation**
   - Time for enemy to reach intersection = distance / enemy_speed
   - Distance bullet must travel = distance to intersection point
   - Required bullet speed = bullet_distance / enemy_time

3. **Power Selection**
   - Bullet speed formula: `speed = 20 - 3 * power`
   - Solve for power: `power = (20 - required_speed) / 3`
   - Validate power is in range [0.1, 3.0]

4. **Fire Decision**
   - Only fires if:
     - Valid intersection exists in the future
     - Enemy is moving (speed > 2)
     - Intersection distance is reasonable (< 800 pixels)
     - Required power is within valid range

## Mathematical Approach

The core innovation is solving for trajectory intersection using parametric line equations:

```
Gun ray:   P = (bx, by) + t1 * (sin(gun_angle), cos(gun_angle))
Enemy ray: Q = (ex, ey) + t2 * enemy_speed * (sin(enemy_angle), cos(enemy_angle))
```

Setting P = Q gives a 2x2 linear system solved using Cramer's rule:
- `t1` = distance bullet must travel
- `t2` = time until enemy reaches intersection

## Strengths

- **Efficient gun movement**: Minimal energy wasted on gun turning
- **Interception specialist**: Deadly against fast-moving targets crossing your firing zone
- **Predictable positioning**: Wall patrol pattern is consistent and defensive
- **Power optimization**: Each shot uses exactly the right power needed

## Weaknesses

- **Stationary targets**: Doesn't aim at slow/stopped enemies (falls back to not firing)
- **Direct pursuit**: Less effective against targets moving directly toward/away
- **Corner coverage**: Limited firing angles in corners
- **Parallel trajectories**: Cannot hit targets moving parallel to firing line

## When Rambo Dominates

- Large, open arenas where enemies cross paths frequently
- Against aggressive bots that move quickly
- Multi-bot melees with lots of crossing traffic
- Mid to late game when enemies are moving unpredictably

## Usage

### Run with RoboCode Tank Royale:
```bash
./rambo.sh
```

### Or directly:
```bash
python3 rambo.py
```

## Configuration

- **Wall margin**: 80 pixels (distance from walls during patrol)
- **Gun sweep**: ±15 degrees around center angle
- **Maximum intercept distance**: 800 pixels
- **Minimum enemy speed**: 2 pixels/tick (ignores stationary targets)

## Level Classification

**Level: 4** (Advanced)

Rambo uses sophisticated trajectory intersection mathematics and innovative power-based aiming, placing it among the advanced tactical bots.

## Color Scheme

- Body: Dark Olive Green (85, 107, 47)
- Turret: Olive Drab (107, 142, 35)
- Radar: Yellow Green (154, 205, 50)

## Future Enhancements

Potential improvements:
- Hybrid mode: Switch to traditional aiming for stationary targets
- Wall-hugging optimization: Better corner handling
- Multi-target tracking: Track multiple crossing trajectories
- Energy management: Vary power based on available energy
- Evasive maneuvers: Add dodging when energy is low
