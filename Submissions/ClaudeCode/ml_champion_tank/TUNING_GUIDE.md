# ML Champion Tank - Tuning Guide

## Quick Fixes Applied

**Just made the bot MORE AGGRESSIVE:**
- ✅ Full turn rate (was 0.5x, now 1.0x) - turns faster
- ✅ Higher speeds (all actions now 7-8 speed)
- ✅ Debug output every 50 ticks to see what it's doing
- ✅ Tighter action angles (85° instead of 90° for circling)
- ✅ More aggressive search mode (turn_rate 15 instead of 10)

## Debug Output

Watch the console for:
- `🔍 Searching for enemies...` - Bot hasn't found anyone yet
- `🎯 Combat: distance=X, enemy_energy=Y, my_energy=Z` - Bot is fighting

## Tuning Parameters

### 1. Movement Aggressiveness

**File:** `ml_champion_tank.py`, lines 213-227

```python
if action == 0:  # aggressive
    turn_angle = angle_to_enemy
    speed = 8  # ← TUNE: Increase for faster aggression (max 8)

elif action == 1:  # defensive
    turn_angle = angle_to_enemy + 180  # ← TUNE: Change angle
    speed = 8  # ← TUNE: Increase to retreat faster

elif action == 2:  # circle_left
    turn_angle = angle_to_enemy + 85  # ← TUNE: 90 = pure circle, 60 = diagonal
    speed = 8  # ← TUNE: Speed while circling
```

**Recommendations:**
- **Too passive?** Increase all speeds to 8
- **Circles too much?** Reduce circle angles to 60-70°
- **Not aggressive enough?** Make action 0 more likely by tuning epsilon or rewards

### 2. Q-Learning Exploration

**File:** `ml_champion_tank.py`, line 82 (in QLearningBrain)

```python
self.epsilon = params.epsilon_start  # Currently 0.392 (39% random)
```

**To make bot less random:**
```bash
# Edit ml_champion_best_params.json
{
  "epsilon_start": 0.1,  # ← Change to 0.1 for only 10% random actions
  ...
}
```

**Recommendations:**
- **Too random?** Set `epsilon_start: 0.1` (10% exploration)
- **Too predictable?** Set `epsilon_start: 0.5` (50% exploration)
- **For competition:** Set `epsilon_start: 0.05` (5% exploration, mostly learned)

### 3. Reward Tuning (What the bot learns to maximize)

**File:** `ml_champion_best_params.json`

```json
{
  "damage_dealt_weight": 8.0,     // ← Reward for hitting enemy
  "damage_taken_weight": -4.0,    // ← Penalty for getting hit
  "survival_reward": 0.15,        // ← Reward per tick alive
  ...
}
```

**To encourage aggression:**
```json
{
  "damage_dealt_weight": 15.0,    // ← HIGHER = more aggressive
  "damage_taken_weight": -2.0,    // ← LESS NEGATIVE = less cautious
  "survival_reward": 0.05         // ← LOWER = cares less about living long
}
```

**To encourage defense:**
```json
{
  "damage_dealt_weight": 5.0,
  "damage_taken_weight": -10.0,   // ← MORE NEGATIVE = avoid damage
  "survival_reward": 0.5          // ← HIGHER = values survival
}
```

**Then re-run evolution:**
```bash
python train_evolution.py --generations 10
```

### 4. Fire Power (How hard to shoot)

**File:** `ml_champion_best_params.json`

```json
{
  "fire_power_close": 2.8,   // ← Power when close (< 200)
  "fire_power_medium": 2.0,  // ← Power at medium range
  "fire_power_far": 1.2      // ← Power when far (> 500)
}
```

**Recommendations:**
- **More damage?** Increase all to 3.0 (but uses more energy!)
- **Energy conservation?** Reduce to 1.5-2.0
- **Sniper build?** Use `fire_power_far: 2.5` for long-range power

### 5. Range Thresholds

**File:** `ml_champion_best_params.json`

```json
{
  "close_range": 200.0,   // ← Anything < 200 is "close"
  "far_range": 500.0      // ← Anything > 500 is "far"
}
```

**For aggressive bot:**
```json
{
  "close_range": 300.0,   // ← Larger close range
  "far_range": 600.0
}
```

## Quick Tuning Recipes

### Recipe 1: "Berserker" (Maximum Aggression)

```json
{
  "epsilon_start": 0.1,
  "damage_dealt_weight": 20.0,
  "damage_taken_weight": -1.0,
  "fire_power_close": 3.0,
  "fire_power_medium": 2.5,
  "fire_power_far": 2.0
}
```

### Recipe 2: "Tank" (Defensive Survivor)

```json
{
  "epsilon_start": 0.05,
  "damage_dealt_weight": 5.0,
  "damage_taken_weight": -15.0,
  "survival_reward": 0.5,
  "fire_power_close": 2.0,
  "fire_power_medium": 1.5
}
```

### Recipe 3: "Sniper" (Long Range)

```json
{
  "epsilon_start": 0.05,
  "close_range": 150.0,
  "far_range": 400.0,
  "fire_power_close": 1.5,
  "fire_power_medium": 2.5,
  "fire_power_far": 3.0
}
```

## Testing Your Changes

1. **Edit parameters** in `ml_champion_best_params.json`
2. **Restart the bot** in RoboCode
3. **Watch debug output** to see if behavior changed
4. **Run 5-10 battles** to evaluate
5. **Check stats** at end of battle (damage dealt/taken, accuracy)

## What to Watch For

### Bot is too passive/circles too much
- ✅ Increase `damage_dealt_weight` to 15-20
- ✅ Reduce `epsilon_start` to 0.05 (less random)
- ✅ Check if circle actions dominate - may need to retrain Q-table

### Bot gets hit too often
- ✅ Increase `damage_taken_weight` (more negative, like -10)
- ✅ Ensure wall avoidance is working (check margin = 70)

### Bot doesn't shoot enough
- ✅ Check fire threshold (line 287): `if abs(gun_turn) < 20`
- ✅ Increase to `< 30` for more shots (less accurate)
- ✅ Reduce to `< 10` for fewer shots (more accurate)

### Bot runs out of energy
- ✅ Reduce fire powers to 1.5-2.0
- ✅ Add energy conservation in rewards

## Advanced: Reset Q-Table

If the bot learned bad behaviors:

```bash
rm ml_champion_qtable.pkl
# Bot will start learning from scratch with new parameters
```

## Evolution-Based Tuning

For systematic optimization:

```bash
# Run evolution with more generations
python train_evolution.py --generations 30

# This will optimize all parameters automatically
# But note: current evolution uses simulated fitness
# For best results, modify train_evolution.py to run actual battles
```

## Monitoring Learning

After battles, check:
```
📊 Battle Stats:
   Reward: 234.5          ← Higher = better (should increase over battles)
   Damage: 45 dealt, 23 taken  ← Want high dealt, low taken
   Accuracy: 12/25 (48%)  ← Shot accuracy
   Epsilon: 0.387         ← Decreases each battle
```

- Reward should trend upward over 20-30 battles
- Epsilon decays from ~0.39 to ~0.05
- Q-table grows to ~20-27 states

Good luck tuning! 🎯
