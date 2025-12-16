# Week 10: Genetic Algorithm - Evolving Combat Tactics

## 🧬 Learning Objectives

- Understand genetic algorithms for parameter optimization
- Learn how to represent tactics as genes (parameters)
- Implement mutation and crossover operations
- Evaluate fitness based on combat outcomes
- Evolve better combat strategies over generations

## 📚 Concepts Covered

### Genetic Algorithms
Genetic algorithms are optimization techniques inspired by natural evolution:
1. **Population**: Multiple candidate solutions (parameter sets)
2. **Fitness**: How well each solution performs (battle results)
3. **Selection**: Choose the best performers to "breed"
4. **Crossover**: Combine parameters from two parents
5. **Mutation**: Random changes to explore new strategies
6. **Evolution**: Repeat for many generations

### Combat Parameters to Optimize

Our bot will optimize a weighted policy with parameters like:
- **Aggression level** (0.0 - 1.0): How much to chase vs retreat
- **Close range weight** (0-10): Preference for close combat
- **Medium range weight** (0-10): Preference for medium distance
- **Long range weight** (0-10): Preference for staying far
- **Energy threshold** (0-100): Health level to switch to defensive
- **Fire power multiplier** (0.5 - 3.0): How hard to shoot at different ranges
- **Dodge intensity** (0.0 - 1.0): How aggressively to dodge
- **Wall avoidance** (0.0 - 1.0): How much to avoid arena edges

### Episode-Based Learning

Each tactical exchange is an **episode** with:
- **Initial state**: Distance, enemies, health, position
- **Actions taken**: Movement, shooting, dodging
- **Outcome**: Health gained/lost, hits/misses, survival
- **Fitness score**: Calculated from the episode results

### Fitness Function

We evaluate each parameter set based on:
```
fitness = (damage_dealt * 2.0) - (damage_taken * 1.0) + 
          (survival_time * 0.1) + (hit_rate * 50.0) - 
          (wall_hits * 10.0) + (kills * 100.0)
```

## 🎮 The Genetic Tank

**`genetic_tank.py`** - A tank that evolves its combat parameters

### Key Features:
1. **Parameter Genome**: 8+ float values representing combat tactics
2. **Population Management**: Tracks multiple parameter sets
3. **Fitness Tracking**: Records performance of each genome
4. **Evolution Engine**: Mutation, crossover, and selection
5. **Persistent Learning**: Saves best genomes to file

### How It Works:

```
Generation 1: Random parameters
  ├─ Battle 1-10: Test each genome
  ├─ Fitness calculation
  └─ Select top 30% performers

Generation 2: Evolve from best
  ├─ Crossover: Combine parent genes
  ├─ Mutation: Add random noise
  ├─ Battle 11-20: Test new genomes
  └─ Repeat...

After 100 generations: 
  └─ Optimal parameters discovered!
```

## 🚀 Running the Tutorial

### Step 1: Train the Genetic Tank
```bash
# Run training mode (many battles)
python genetic_tank.py --mode train --generations 50
```

This will:
- Create a population of 20 random parameter sets
- Battle against various opponents
- Evolve parameters over 50 generations
- Save the best genome to `genetic_best.json`

### Step 2: Test the Evolved Bot
```bash
# Run with best evolved parameters
python genetic_tank.py --mode battle
```

### Step 3: Watch Your Bot Evolve in the Arena!

```bash
# Start the RoboCode GUI, then run:
python Tutorials/Week10_GeneticAlgorithm/genetic_tank.py --mode battle
```

Add some opponents and start the battle to see your evolved parameters in action!

You can also check your GitHub Actions tab - the automated battles will show you how well your evolved bot performs against various opponents!

## 📊 Understanding the Output

During training, you'll see:
```
Generation 1
  Genome 0: fitness=-150.5 (aggression=0.45, close_range=3.2, ...)
  Genome 1: fitness=210.3 (aggression=0.72, close_range=1.8, ...)
  ...
  Best fitness: 210.3
  Average fitness: 45.2

Generation 2 (evolved from gen 1)
  Genome 0: fitness=198.7 (child of genomes 1 & 4)
  Genome 1: fitness=245.8 (child of genomes 1 & 3, mutated)
  ...
  Best fitness: 245.8 (improvement!)
  Average fitness: 112.6
```

Watch how:
- Average fitness increases over time
- Best fitness finds better solutions
- Parameters converge to effective values

## 🧪 Experiments to Try

### 1. Different Mutation Rates
- High mutation (0.3): More exploration, slower convergence
- Low mutation (0.05): Faster convergence, might get stuck

### 2. Population Size
- Small (10): Faster generations, less diversity
- Large (50): Slower but more thorough search

### 3. Fitness Function Tuning
Try emphasizing different aspects:
```python
# Aggressive fighter
fitness = damage_dealt * 3.0 - damage_taken * 0.5

# Survivalist
fitness = survival_time * 1.0 + damage_dealt * 0.5 - damage_taken * 2.0

# Sniper
fitness = hit_rate * 100.0 + long_range_kills * 50.0
```

### 4. Multi-Objective Optimization
Optimize for multiple goals:
- Win rate AND survival time
- Damage dealt AND energy efficiency
- Hit rate AND movement efficiency

## 🎯 Key Takeaways

1. **Genetic algorithms find good solutions without manual tuning**
2. **Fitness function design is crucial** - it defines what "good" means
3. **Mutation provides exploration**, crossover exploits known good solutions
4. **Evolution takes time** - expect 20-100+ generations
5. **Parameters discovered often surprise us** - the algorithm finds non-obvious solutions

## 🔗 What's Next?

The genetic algorithm finds good parameters through trial and error. But what if we want the bot to **learn during combat**?

→ **Week 11: Q-Learning** - Real-time reinforcement learning that adapts to opponents!

## 📖 Further Reading

- Genetic Algorithms in Python: https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
- Evolution Strategies: https://blog.otoro.net/2017/10/29/visual-evolution-strategies/
- Hyperparameter Optimization: https://en.wikipedia.org/wiki/Hyperparameter_optimization
