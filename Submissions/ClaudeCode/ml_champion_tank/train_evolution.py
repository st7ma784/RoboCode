"""
Training script for evolving ML Champion Tank parameters

This script runs a genetic algorithm to evolve the meta-parameters
that control the bot's Q-learning behavior and combat strategy.
"""
import json
import random
import numpy as np
from pathlib import Path
from dataclasses import asdict
from ml_champion_tank import EvolvableParameters


class EvolutionEngine:
    """Manages genetic algorithm evolution of parameters"""

    def __init__(self, population_size: int = 15):
        self.population_size = population_size
        self.population: list[EvolvableParameters] = []
        self.generation = 0
        self.best_params: EvolvableParameters = None
        self.best_fitness = float('-inf')

        # Evolution hyperparameters
        self.mutation_rate = 0.25
        self.elite_ratio = 0.2
        self.crossover_ratio = 0.6
        self.random_ratio = 0.2

    def initialize_population(self):
        """Create initial random population"""
        print(f"🧬 Initializing population of {self.population_size} individuals")

        # Start with some good defaults plus random variations
        base_params = EvolvableParameters()
        self.population = [base_params]

        for _ in range(self.population_size - 1):
            params = EvolvableParameters(
                learning_rate=random.uniform(0.05, 0.3),
                discount_factor=random.uniform(0.8, 0.98),
                epsilon_start=random.uniform(0.2, 0.5),
                epsilon_decay=random.uniform(0.99, 0.999),
                damage_dealt_weight=random.uniform(5.0, 15.0),
                damage_taken_weight=random.uniform(-8.0, -2.0),
                kill_reward=random.uniform(100.0, 200.0),
                death_penalty=random.uniform(-200.0, -100.0),
                close_range=random.uniform(150.0, 250.0),
                far_range=random.uniform(400.0, 600.0),
                low_health=random.uniform(20.0, 40.0),
                high_health=random.uniform(55.0, 75.0),
                aggressive_speed=random.uniform(7.0, 8.0),
                fire_power_close=random.uniform(2.5, 3.0),
                fire_power_medium=random.uniform(1.5, 2.5),
                fire_power_far=random.uniform(1.0, 1.5)
            )
            self.population.append(params)

    def evolve_generation(self):
        """Evolve to next generation"""
        # Sort by fitness
        self.population.sort(key=lambda p: p.fitness, reverse=True)

        # Track best
        if self.population[0].fitness > self.best_fitness:
            self.best_fitness = self.population[0].fitness
            self.best_params = self.population[0]
            print(f"✨ New best! Fitness: {self.best_fitness:.1f}")
            self.save_best()

        # Calculate group sizes
        elite_count = max(1, int(self.population_size * self.elite_ratio))
        crossover_count = int(self.population_size * self.crossover_ratio)
        random_count = self.population_size - elite_count - crossover_count

        next_gen = []

        # Elites
        next_gen.extend(self.population[:elite_count])

        # Crossover
        mating_pool = self.population[:self.population_size // 2]
        for _ in range(crossover_count):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            child = EvolvableParameters.crossover(parent1, parent2)
            child.mutate(self.mutation_rate)
            next_gen.append(child)

        # Random (diversity)
        for _ in range(random_count):
            params = EvolvableParameters()
            params.mutate(0.5)  # Heavy mutation for diversity
            next_gen.append(params)

        self.population = next_gen
        self.generation += 1

        # Stats
        avg_fitness = sum(p.fitness for p in self.population) / len(self.population)
        print(f"\n📊 Generation {self.generation}")
        print(f"   Best: {self.population[0].fitness:.1f}")
        print(f"   Average: {avg_fitness:.1f}")
        print(f"   All-time best: {self.best_fitness:.1f}")

    def save_best(self):
        """Save best parameters to file"""
        if self.best_params:
            with open("ml_champion_best_params.json", 'w') as f:
                json.dump(asdict(self.best_params), f, indent=2)
            print(f"💾 Saved best parameters")

    def save_population(self):
        """Save entire population"""
        data = {
            'generation': self.generation,
            'population': [asdict(p) for p in self.population],
            'best_fitness': self.best_fitness
        }
        with open("ml_champion_population.json", 'w') as f:
            json.dump(data, f, indent=2)

    def load_population(self) -> bool:
        """Load population from file"""
        if not Path("ml_champion_population.json").exists():
            return False

        with open("ml_champion_population.json", 'r') as f:
            data = json.load(f)

        self.generation = data['generation']
        self.population = [EvolvableParameters(**p) for p in data['population']]
        self.best_fitness = data['best_fitness']

        print(f"📂 Loaded population from generation {self.generation}")
        return True


def simulate_battle_fitness(params: EvolvableParameters) -> float:
    """
    Placeholder fitness function

    In a real implementation, this would:
    1. Create a bot with these parameters
    2. Run it in battles against various opponents
    3. Return fitness based on performance

    For now, we return a simulated fitness for demonstration
    """
    # Simulated fitness based on parameter balance
    fitness = 0.0

    # Reward balanced damage weights
    if 6 < params.damage_dealt_weight < 12:
        fitness += 50
    if -6 < params.damage_taken_weight < -3:
        fitness += 50

    # Reward reasonable ranges
    if 150 < params.close_range < 250:
        fitness += 30
    if 400 < params.far_range < 600:
        fitness += 30

    # Reward good learning parameters
    if 0.1 < params.learning_rate < 0.25:
        fitness += 40
    if 0.85 < params.discount_factor < 0.95:
        fitness += 40

    # Add randomness to simulate battle variance
    fitness += random.gauss(0, 30)

    return fitness


def train_evolution(generations: int = 20):
    """Run evolutionary training"""
    print("🚀 Starting Evolutionary Training")
    print(f"   Generations: {generations}")

    engine = EvolutionEngine(population_size=15)

    if not engine.load_population():
        engine.initialize_population()

    for gen in range(generations):
        print(f"\n{'='*60}")
        print(f"GENERATION {gen + 1}/{generations}")
        print(f"{'='*60}")

        # Evaluate fitness for each individual
        print("\n🎮 Running battles...")
        for i, params in enumerate(engine.population):
            # In real implementation, run actual battles here
            params.fitness = simulate_battle_fitness(params)
            print(f"  Individual {i+1}: fitness={params.fitness:.1f}")

        # Evolve
        engine.evolve_generation()

        # Save progress
        if (gen + 1) % 5 == 0:
            engine.save_population()

    print(f"\n✅ Training complete!")
    print(f"   Best fitness: {engine.best_fitness:.1f}")
    engine.save_population()
    engine.save_best()

    # Print best parameters
    print("\n🏆 Best Parameters:")
    best = engine.best_params
    print(f"   Learning rate: {best.learning_rate:.3f}")
    print(f"   Discount factor: {best.discount_factor:.3f}")
    print(f"   Damage dealt weight: {best.damage_dealt_weight:.1f}")
    print(f"   Damage taken weight: {best.damage_taken_weight:.1f}")
    print(f"   Close range: {best.close_range:.0f}")
    print(f"   Far range: {best.far_range:.0f}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Train ML Champion Tank via Evolution')
    parser.add_argument('--generations', type=int, default=20,
                       help='Number of generations to evolve')
    parser.add_argument('--mode', choices=['train', 'analyze'], default='train',
                       help='train: Run evolution, analyze: Show current best')

    args = parser.parse_args()

    if args.mode == 'analyze':
        # Show current best parameters
        if Path("ml_champion_best_params.json").exists():
            with open("ml_champion_best_params.json") as f:
                params = json.load(f)
            print("\n🏆 Current Best Parameters:")
            print(json.dumps(params, indent=2))
        else:
            print("❌ No trained parameters found")
    else:
        train_evolution(args.generations)
