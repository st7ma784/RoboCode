# AI & Machine Learning for RoboCode

## 🧠 Introduction to AI in Combat

Traditional tank programming uses **hand-coded rules**:
```python
if enemy_distance < 200:
    # Attack!
elif my_health < 30:
    # Retreat!
```

But what if your tank could **learn** what works? That's where AI comes in!

## 🎯 Two Approaches to Learning

### 1. Genetic Algorithms (Week 10)
**Evolutionary optimization** - Simulate natural selection

**Best for:**
- Finding optimal parameter values
- Offline learning (between battles)
- Global optimization of tank behavior
- When you can't easily define rewards

**How it works:**
```
Generation 1: Try 20 random parameter sets
  ├─ aggression=0.3, range_pref=close → loses badly
  ├─ aggression=0.8, range_pref=medium → does OK
  └─ aggression=0.5, range_pref=far → wins!

Generation 2: Evolve from best performers
  ├─ Combine good traits (crossover)
  ├─ Add random changes (mutation)
  └─ Test new combinations

After 50 generations → Optimal parameters discovered!
```

### 2. Q-Learning (Week 11)
**Reinforcement learning** - Learn from experience

**Best for:**
- Learning during combat
- Adapting to specific opponents
- State-action decision making
- When you can define clear rewards

**How it works:**
```
Battle starts: Q-table empty

Tick 1: In state "close, low health"
  ├─ Try action "retreat" → Get +15 reward (good!)
  └─ Update Q(close-low, retreat) = 15

Tick 2: In state "medium, high health"
  ├─ Try action "attack" → Get +25 reward (great!)
  └─ Update Q(medium-high, attack) = 25

After 100 battles:
  └─ Q-table knows best action for each state!
```

## 📊 Comparison

| Feature | Genetic Algorithm | Q-Learning |
|---------|------------------|------------|
| **Learning Speed** | Slow (generations) | Fast (during battle) |
| **When** | Offline training | Real-time online |
| **What it learns** | Parameters | Action policy |
| **Adaptation** | Between battles | During battle |
| **Memory** | Small (params) | Large (Q-table) |
| **Opponent-specific** | No | Yes |
| **Best for** | Global strategy | Tactical decisions |

## 🎮 When to Use Each

### Use Genetic Algorithms When:
- You want to tune many parameters at once
- You have time for offline training
- You want one tank that works well generally
- Your strategy has many tunable numbers

**Example:** Evolving fire power, dodge intensity, range preferences, wall avoidance

### Use Q-Learning When:
- You want to adapt to specific opponents
- You need real-time decision making
- Your problem is about choosing actions
- You can define good reward signals

**Example:** Learning when to attack vs retreat based on health and distance

## 🔥 Combining Both!

The most powerful approach uses **both techniques together**:

### Level 1: Genetic Algorithm for Parameters
```python
# Evolve optimal parameters
aggression = 0.73  # Learned via GA
close_range = 4.2  # Learned via GA
energy_threshold = 35  # Learned via GA
```

### Level 2: Q-Learning for Tactics
```python
# Use Q-Learning to choose actions with those parameters
state = (health, distance, angle)
action = q_table[state].argmax()  # Learned via RL
```

**Result:** Parameters optimized offline, tactics adapted online!

## 🧪 Advanced Concepts

### 1. Fitness Function Design (GA)
Your fitness function determines what the bot learns:

```python
# Aggressive fighter
fitness = damage_dealt * 3.0 - damage_taken * 0.5 + kills * 100

# Defensive survivor  
fitness = survival_time * 2.0 - damage_taken * 2.0 + damage_dealt * 0.5

# Balanced warrior
fitness = damage_dealt * 2.0 - damage_taken * 1.0 + survival_time * 0.1
```

### 2. Reward Shaping (Q-Learning)
Your rewards shape the learned behavior:

```python
# Teaches aggressive close combat
reward = +10 * damage_dealt - 5 * damage_taken + 2 * got_closer

# Teaches cautious sniping
reward = +15 * damage_dealt - 10 * damage_taken + 2 * kept_distance

# Teaches hit accuracy
reward = +20 * hit_landed - 5 * shot_missed
```

### 3. Exploration vs Exploitation

Both techniques balance trying new things (explore) vs using known good strategies (exploit):

**Genetic Algorithm:**
- Mutation = exploration (try random changes)
- Elite selection = exploitation (keep best)
- Random individuals = exploration (maintain diversity)

**Q-Learning:**
- Epsilon-greedy = exploration/exploitation balance
- High ε (0.9) = explore (90% random actions)
- Low ε (0.1) = exploit (90% best actions)

### 4. State Representation (Q-Learning)

How you represent state hugely impacts learning:

**Too simple** - Loses important information:
```python
state = (distance_bucket,)  # Only distance, ignores health!
```

**Too complex** - Takes forever to learn:
```python
state = (x, y, direction, speed, gun_heat, health, 
         enemy_x, enemy_y, enemy_dir, enemy_speed, ...)
# Millions of possible states!
```

**Just right** - Captures key factors:
```python
state = (health_bucket, distance_bucket, angle_bucket)
# 3 × 3 × 3 = 27 manageable states
```

## 📚 Learning Path

### Beginner Path
1. **Start with Week 10 (Genetic Algorithm)**
   - Easier to understand
   - See evolution happen
   - Less math required

2. **Then Week 11 (Q-Learning)**
   - Builds on GA concepts
   - More sophisticated
   - Real-time learning is cooler!

### Advanced Path
1. **Master both separately**
2. **Combine them** - GA for params, QL for actions
3. **Try Deep Q-Learning** - Neural networks instead of Q-table
4. **Explore policy gradient methods** - Direct policy learning

## 🎯 Key Takeaways

1. **AI discovers solutions humans might miss** - Don't hand-code everything!
2. **Different problems need different AI** - GA for optimization, RL for decisions
3. **Learning takes time** - Expect 50-200+ battles
4. **Design matters** - Fitness functions and rewards shape behavior
5. **Experiment and iterate** - Try different approaches and learn

## 🚀 Next Steps

Ready to build learning tanks?

- **[Week 10: Genetic Algorithm Tutorial](../Tutorials/Week10_GeneticAlgorithm/README.md)**
- **[Week 11: Q-Learning Tutorial](../Tutorials/Week11_QLearning/README.md)**

Have fun teaching your tanks to learn! 🤖🎓
