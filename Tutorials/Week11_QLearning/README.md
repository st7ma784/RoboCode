# Week 11: Q-Learning - Real-Time Reinforcement Learning

## 🤖 Learning Objectives

- Understand reinforcement learning fundamentals
- Learn Q-Learning algorithm
- Implement state representation for combat
- Build Q-table for action values
- Enable real-time learning during battles

## 📚 Concepts Covered

### Reinforcement Learning Basics

Reinforcement Learning (RL) is learning through interaction:
- **Agent**: Our tank making decisions
- **Environment**: The battle arena and opponents
- **State**: Current situation (position, enemies, health)
- **Action**: What to do (move, shoot, turn)
- **Reward**: Feedback on action quality (+/- points)
- **Policy**: Strategy for choosing actions

### Q-Learning Algorithm

Q-Learning learns an **action-value function** Q(s, a):
- **Q(s, a)**: Expected reward for taking action `a` in state `s`
- **Goal**: Learn which actions are best in each situation
- **Method**: Update Q-values based on experience

**Update Rule**:
```
Q(s, a) ← Q(s, a) + α[r + γ·max Q(s', a') - Q(s, a)]

Where:
  α (alpha) = learning rate (how fast to learn)
  γ (gamma) = discount factor (value future rewards)
  r = immediate reward
  s' = next state
  max Q(s', a') = best future value
```

### State Representation

We discretize continuous combat into discrete states:

```
State = (my_health, enemy_health, distance, angle, my_speed)

Discretized:
- my_health: [high, medium, low]          (3 values)
- enemy_health: [high, medium, low]       (3 values)
- distance: [close, medium, far]          (3 values)
- angle: [front, side, back]              (3 values)
- my_speed: [stopped, slow, fast]         (3 values)

Total states: 3 × 3 × 3 × 3 × 3 = 243 states
```

### Action Space

Our bot can take discrete actions:
```
Actions:
  0: Move forward + shoot heavy
  1: Move forward + shoot light
  2: Turn left + shoot
  3: Turn right + shoot
  4: Retreat + shoot
  5: Circle left + shoot
  6: Circle right + shoot
  7: Stop + shoot heavy
```

### Reward Function

We give immediate feedback after each action:
```
Reward = 
  + 10.0 per damage dealt to enemy
  - 5.0 per damage taken from enemy
  + 2.0 if got closer to enemy (when healthy)
  + 2.0 if got farther from enemy (when low health)
  - 1.0 per wall hit
  + 100.0 for killing enemy
  - 100.0 for dying
  + 0.1 per tick survived
```

## 🎮 The Q-Learning Tank

**`qlearning_tank.py`** - A tank that learns optimal tactics through experience

### Key Features:
1. **State Discretization**: Converts continuous values to discrete states
2. **Q-Table**: Stores learned values for (state, action) pairs
3. **Epsilon-Greedy**: Balances exploration vs exploitation
4. **Experience Replay**: Learns from past experiences
5. **Persistent Memory**: Saves/loads Q-table across battles

### How It Works:

```
Initial battles: Random exploration
  ├─ Try action → Get reward
  ├─ Update Q(state, action)
  └─ Gradually learn which actions work

After 50 battles: Exploitation
  ├─ Use learned Q-values
  ├─ Choose best known actions
  └─ Still occasionally explore (ε=0.1)

After 200 battles: Expert
  └─ Near-optimal policy learned!
```

### Learning Process:

```python
# Pseudo-code for Q-Learning loop
while in_battle:
    state = get_current_state()
    
    # Choose action (explore or exploit)
    if random() < epsilon:
        action = random_action()      # Explore
    else:
        action = best_action(state)   # Exploit
    
    # Execute action
    execute_action(action)
    
    # Observe result
    next_state = get_current_state()
    reward = calculate_reward()
    
    # Update Q-value
    Q[state][action] += α * (
        reward + γ * max(Q[next_state]) - Q[state][action]
    )
```

## 🚀 Running the Tutorial

### Step 1: Initial Training (Exploration)
```bash
# Start with high exploration (90% random)
python qlearning_tank.py --epsilon 0.9 --battles 50
```

The bot will:
- Try random actions frequently
- Build initial Q-table
- Learn basic patterns
- Save Q-table to `qlearning_qtable.pkl`

### Step 2: Continued Training (Refinement)
```bash
# Reduce exploration (30% random)
python qlearning_tank.py --epsilon 0.3 --battles 100
```

The bot will:
- Load existing Q-table
- Mostly use learned actions
- Explore occasionally
- Refine Q-values

### Step 3: Expert Mode (Exploitation)
```bash
# Minimal exploration (10% random)
python qlearning_tank.py --epsilon 0.1
```

The bot will:
- Use learned optimal policy
- Rarely explore
- Demonstrate learned skills

### Step 4: Visualize Learning
```bash
# Show Q-table statistics
python qlearning_tank.py --mode analyze
```

## 📊 Understanding the Output

During training:
```
Battle 1/50
  Episode steps: 245
  Total reward: -45.3
  Epsilon: 0.90 (exploring)
  Q-table size: 127 states learned

Battle 10/50
  Episode steps: 412
  Total reward: 125.7
  Epsilon: 0.90 (exploring)
  Q-table size: 189 states learned

Battle 50/50
  Episode steps: 623
  Total reward: 387.4
  Epsilon: 0.30 (mostly exploiting)
  Q-table size: 243 states learned
  
💾 Q-table saved with 243 states
📈 Average reward over last 10 battles: 298.5
```

Watch how:
- Total reward increases (better performance)
- Episode length increases (survives longer)
- Q-table fills up (explores all states)
- Average reward trends upward

## 🧪 Experiments to Try

### 1. Different Learning Rates (α)
```python
# Fast learning (might be unstable)
alpha = 0.5

# Slow learning (more stable)
alpha = 0.1

# Adaptive learning (decrease over time)
alpha = 0.5 / (1 + episode_number * 0.01)
```

### 2. Discount Factor (γ)
```python
# Short-term focus (immediate rewards)
gamma = 0.5

# Long-term planning (future rewards valued)
gamma = 0.95

# Balanced
gamma = 0.8
```

### 3. Exploration Schedule
```python
# Aggressive decay (quick convergence)
epsilon = max(0.01, 0.9 * 0.95 ** episode)

# Conservative decay (thorough exploration)
epsilon = max(0.1, 0.9 * 0.99 ** episode)

# Fixed exploration (always 20% random)
epsilon = 0.2
```

### 4. Reward Shaping
Try emphasizing different behaviors:
```python
# Aggressive fighter
reward += damage_dealt * 15.0 - damage_taken * 3.0

# Defensive survivor
reward += survival_time * 0.5 - damage_taken * 10.0

# Accuracy-focused
reward += (hits / shots) * 20.0
```

### 5. State Space Variations

**Simpler state (faster learning)**:
```python
state = (my_health_bucket, distance_bucket)
# Only 3 × 3 = 9 states
```

**Richer state (better decisions)**:
```python
state = (my_health, enemy_health, distance, angle, 
         my_speed, enemy_speed, gun_heat, bullets_left)
# Many more states, slower learning
```

## 🎯 Key Takeaways

1. **Q-Learning learns from experience** - No manual tuning needed!
2. **Exploration vs Exploitation tradeoff** - Must explore to find good actions
3. **Reward design is critical** - Shapes what the agent learns
4. **State representation matters** - Too simple misses info, too complex slows learning
5. **Learning takes time** - Expect 50-200+ battles for good performance
6. **Generalization is limited** - Q-table only remembers visited states

## 📈 Comparing to Genetic Algorithm

| Aspect | Genetic Algorithm | Q-Learning |
|--------|------------------|------------|
| **Learning** | Offline (between battles) | Online (during battle) |
| **Adaptation** | Slow (generations) | Fast (seconds) |
| **Memory** | Parameters only | Full Q-table |
| **Exploration** | Mutation | Epsilon-greedy |
| **Opponent-specific** | No | Yes (can adapt mid-battle) |
| **Convergence** | 20-100 generations | 50-200 battles |

## 🚀 Advanced Extensions

### 1. Deep Q-Learning (DQN)
Replace Q-table with neural network:
- Handle continuous states directly
- Generalize to unseen situations
- Learn complex patterns

### 2. Policy Gradient Methods
Learn policy directly instead of Q-values:
- Better for continuous actions
- More stable in some cases
- Can learn stochastic policies

### 3. Multi-Agent RL
Learn in team battles:
- Coordinate with teammates
- Learn emergent strategies
- Handle opponent adaptation

### 4. Transfer Learning
Use knowledge from one opponent against others:
- Faster learning on new opponents
- Build general combat skills
- Meta-learning

## 🔗 What's Next?

Congratulations! You've learned both:
- **Genetic Algorithms** (evolutionary optimization)
- **Q-Learning** (reinforcement learning)

These techniques can be combined:
- Use GA to find good reward function parameters
- Use Q-Learning with evolved state representation
- Multi-objective optimization with RL policies

## 📖 Further Reading

- Sutton & Barto's RL Book: http://incompleteideas.net/book/
- Q-Learning Tutorial: https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/
- Deep RL Course: https://huggingface.co/learn/deep-rl-course/
- OpenAI Spinning Up: https://spinningup.openai.com/
