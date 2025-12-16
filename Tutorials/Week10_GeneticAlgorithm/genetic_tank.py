"""
Genetic Tank - Evolving Combat Parameters with Genetic Algorithms
Week 10: Genetic Algorithm - Parameter Optimization

This tank demonstrates:
- Genetic algorithm for parameter optimization
- Population-based search
- Fitness evaluation from combat outcomes
- Mutation and crossover operators
- Persistent learning across battles

The bot evolves parameters like aggression, range preferences,
and dodge intensity to maximize combat effectiveness!
"""
from robocode_tank_royale.bot_api import Bot, BotInfo
import math
import random
import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional
import argparse


@dataclass
class CombatGenome:
    """
    Represents a set of combat parameters (the "DNA" of our bot)
    
    Each parameter influences how the bot behaves in combat.
    The genetic algorithm will evolve these to find optimal values.
    """
    # Core behavior weights
    aggression: float = 0.5          # 0.0 (defensive) to 1.0 (aggressive)
    close_range_weight: float = 5.0  # Preference for close combat (0-10)
    medium_range_weight: float = 5.0 # Preference for medium distance (0-10)
    long_range_weight: float = 5.0   # Preference for long range (0-10)
    
    # Tactical thresholds
    energy_threshold: float = 30.0   # Health to switch defensive (0-100)
    close_range_dist: float = 150.0  # What counts as "close" (50-300)
    long_range_dist: float = 500.0   # What counts as "long" (300-800)
    
    # Combat parameters
    fire_power_min: float = 1.0      # Minimum bullet power (0.1-3.0)
    fire_power_max: float = 3.0      # Maximum bullet power (0.1-3.0)
    dodge_intensity: float = 0.7     # How hard to dodge (0.0-1.0)
    wall_avoidance: float = 0.8      # Wall avoidance strength (0.0-1.0)
    
    # Fitness tracking
    fitness: float = 0.0
    battles_fought: int = 0
    
    def mutate(self, mutation_rate: float = 0.1, mutation_strength: float = 0.2):
        """
        Apply random mutations to parameters
        
        Args:
            mutation_rate: Probability each gene mutates (0.0-1.0)
            mutation_strength: How much to change (0.0-1.0)
        """
        if random.random() < mutation_rate:
            self.aggression = max(0.0, min(1.0, 
                self.aggression + random.gauss(0, mutation_strength)))
        
        if random.random() < mutation_rate:
            self.close_range_weight = max(0.0, min(10.0,
                self.close_range_weight + random.gauss(0, mutation_strength * 5)))
        
        if random.random() < mutation_rate:
            self.medium_range_weight = max(0.0, min(10.0,
                self.medium_range_weight + random.gauss(0, mutation_strength * 5)))
        
        if random.random() < mutation_rate:
            self.long_range_weight = max(0.0, min(10.0,
                self.long_range_weight + random.gauss(0, mutation_strength * 5)))
        
        if random.random() < mutation_rate:
            self.energy_threshold = max(10.0, min(90.0,
                self.energy_threshold + random.gauss(0, mutation_strength * 20)))
        
        if random.random() < mutation_rate:
            self.close_range_dist = max(50.0, min(300.0,
                self.close_range_dist + random.gauss(0, mutation_strength * 50)))
        
        if random.random() < mutation_rate:
            self.long_range_dist = max(300.0, min(800.0,
                self.long_range_dist + random.gauss(0, mutation_strength * 100)))
        
        if random.random() < mutation_rate:
            self.fire_power_min = max(0.1, min(2.0,
                self.fire_power_min + random.gauss(0, mutation_strength)))
        
        if random.random() < mutation_rate:
            self.fire_power_max = max(self.fire_power_min, min(3.0,
                self.fire_power_max + random.gauss(0, mutation_strength)))
        
        if random.random() < mutation_rate:
            self.dodge_intensity = max(0.0, min(1.0,
                self.dodge_intensity + random.gauss(0, mutation_strength)))
        
        if random.random() < mutation_rate:
            self.wall_avoidance = max(0.0, min(1.0,
                self.wall_avoidance + random.gauss(0, mutation_strength)))
    
    @staticmethod
    def crossover(parent1: 'CombatGenome', parent2: 'CombatGenome') -> 'CombatGenome':
        """
        Create offspring by combining two parent genomes
        
        Uses uniform crossover: each gene randomly chosen from either parent
        """
        child = CombatGenome()
        
        # Randomly inherit each parameter from either parent
        child.aggression = random.choice([parent1.aggression, parent2.aggression])
        child.close_range_weight = random.choice([parent1.close_range_weight, parent2.close_range_weight])
        child.medium_range_weight = random.choice([parent1.medium_range_weight, parent2.medium_range_weight])
        child.long_range_weight = random.choice([parent1.long_range_weight, parent2.long_range_weight])
        child.energy_threshold = random.choice([parent1.energy_threshold, parent2.energy_threshold])
        child.close_range_dist = random.choice([parent1.close_range_dist, parent2.close_range_dist])
        child.long_range_dist = random.choice([parent1.long_range_dist, parent2.long_range_dist])
        child.fire_power_min = random.choice([parent1.fire_power_min, parent2.fire_power_min])
        child.fire_power_max = random.choice([parent1.fire_power_max, parent2.fire_power_max])
        child.dodge_intensity = random.choice([parent1.dodge_intensity, parent2.dodge_intensity])
        child.wall_avoidance = random.choice([parent1.wall_avoidance, parent2.wall_avoidance])
        
        return child
    
    @staticmethod
    def random_genome() -> 'CombatGenome':
        """Create a random genome for initial population"""
        return CombatGenome(
            aggression=random.uniform(0.0, 1.0),
            close_range_weight=random.uniform(0.0, 10.0),
            medium_range_weight=random.uniform(0.0, 10.0),
            long_range_weight=random.uniform(0.0, 10.0),
            energy_threshold=random.uniform(10.0, 90.0),
            close_range_dist=random.uniform(50.0, 300.0),
            long_range_dist=random.uniform(300.0, 800.0),
            fire_power_min=random.uniform(0.1, 2.0),
            fire_power_max=random.uniform(2.0, 3.0),
            dodge_intensity=random.uniform(0.0, 1.0),
            wall_avoidance=random.uniform(0.0, 1.0)
        )


class GeneticEvolutionEngine:
    """
    Manages the genetic algorithm process
    
    This class handles:
    - Population creation and management
    - Fitness evaluation
    - Selection of best performers
    - Crossover and mutation
    - Saving/loading genomes
    """
    
    def __init__(self, population_size: int = 20, save_path: str = "genetic_population.json"):
        self.population_size = population_size
        self.save_path = save_path
        self.population: List[CombatGenome] = []
        self.generation = 0
        self.best_genome: Optional[CombatGenome] = None
        self.best_fitness = float('-inf')
        
        # Evolution parameters
        self.mutation_rate = 0.15        # 15% chance each gene mutates
        self.mutation_strength = 0.2     # 20% variation
        self.elite_ratio = 0.2           # Keep top 20% unchanged
        self.crossover_ratio = 0.6       # 60% from crossover
        self.random_ratio = 0.2          # 20% completely random (diversity)
    
    def initialize_population(self):
        """Create initial random population"""
        self.population = [CombatGenome.random_genome() for _ in range(self.population_size)]
        print(f"🧬 Initialized population with {self.population_size} random genomes")
    
    def evolve_generation(self):
        """
        Create next generation through evolution
        
        Process:
        1. Sort by fitness
        2. Keep elite (top performers)
        3. Create offspring through crossover
        4. Add random individuals for diversity
        5. Apply mutations
        """
        # Sort population by fitness
        self.population.sort(key=lambda g: g.fitness, reverse=True)
        
        # Track best
        if self.population[0].fitness > self.best_fitness:
            self.best_fitness = self.population[0].fitness
            self.best_genome = self.population[0]
            print(f"✨ New best genome! Fitness: {self.best_fitness:.1f}")
        
        # Calculate sizes for each group
        elite_count = max(1, int(self.population_size * self.elite_ratio))
        crossover_count = int(self.population_size * self.crossover_ratio)
        random_count = self.population_size - elite_count - crossover_count
        
        # Build next generation
        next_generation = []
        
        # 1. Elite: Keep best performers
        next_generation.extend(self.population[:elite_count])
        
        # 2. Crossover: Breed from top 50%
        mating_pool = self.population[:self.population_size // 2]
        for _ in range(crossover_count):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            child = CombatGenome.crossover(parent1, parent2)
            child.mutate(self.mutation_rate, self.mutation_strength)
            next_generation.append(child)
        
        # 3. Random: Add diversity
        for _ in range(random_count):
            next_generation.append(CombatGenome.random_genome())
        
        self.population = next_generation
        self.generation += 1
        
        # Print generation stats
        avg_fitness = sum(g.fitness for g in self.population) / len(self.population)
        print(f"\n📊 Generation {self.generation}")
        print(f"   Best fitness: {self.population[0].fitness:.1f}")
        print(f"   Average fitness: {avg_fitness:.1f}")
        print(f"   All-time best: {self.best_fitness:.1f}")
    
    def save_population(self):
        """Save entire population to file"""
        data = {
            'generation': self.generation,
            'population': [asdict(genome) for genome in self.population],
            'best_genome': asdict(self.best_genome) if self.best_genome else None,
            'best_fitness': self.best_fitness
        }
        with open(self.save_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved population to {self.save_path}")
    
    def load_population(self):
        """Load population from file"""
        if not os.path.exists(self.save_path):
            return False
        
        with open(self.save_path, 'r') as f:
            data = json.load(f)
        
        self.generation = data['generation']
        self.population = [CombatGenome(**g) for g in data['population']]
        if data['best_genome']:
            self.best_genome = CombatGenome(**data['best_genome'])
        self.best_fitness = data['best_fitness']
        
        print(f"📂 Loaded population from generation {self.generation}")
        return True


class GeneticTank(Bot):
    """
    A tank that uses evolved parameters for combat decisions
    
    The bot's behavior is controlled by a genome (set of parameters).
    In training mode, it evaluates multiple genomes and evolves them.
    In battle mode, it uses the best evolved genome.
    """
    
    def __init__(self, bot_info: BotInfo, genome: Optional[CombatGenome] = None):
        super().__init__(bot_info)
        
        # Use provided genome or load best one
        if genome:
            self.genome = genome
        else:
            self.genome = self.load_best_genome()
        
        # Combat tracking for fitness
        self.start_energy = 100.0
        self.damage_dealt = 0.0
        self.damage_taken = 0.0
        self.hits_landed = 0
        self.shots_fired = 0
        self.survival_time = 0
        self.wall_hits = 0
        self.enemies_killed = 0
        
        # Radar tracking
        self.scanned_enemies = {}
        self.current_target = None
    
    def load_best_genome(self) -> CombatGenome:
        """Load the best evolved genome, or use default"""
        best_path = "genetic_best.json"
        if os.path.exists(best_path):
            with open(best_path, 'r') as f:
                data = json.load(f)
            print(f"🧬 Loaded best genome (fitness: {data.get('fitness', 0):.1f})")
            return CombatGenome(**data)
        else:
            print("⚠️  No evolved genome found, using default parameters")
            return CombatGenome()
    
    def calculate_fitness(self) -> float:
        """
        Calculate fitness score based on combat performance
        
        Rewards:
        - Damage dealt (offensive effectiveness)
        - Survival time (defensive effectiveness)
        - Hit accuracy (shooting skill)
        - Kills (ultimate goal)
        
        Penalties:
        - Damage taken (poor defense)
        - Wall hits (poor navigation)
        """
        hit_rate = self.hits_landed / max(1, self.shots_fired)
        
        fitness = (
            self.damage_dealt * 2.0 +           # Offense
            -self.damage_taken * 1.0 +          # Defense
            self.survival_time * 0.1 +          # Longevity
            hit_rate * 50.0 +                   # Accuracy
            -self.wall_hits * 10.0 +            # Navigation
            self.enemies_killed * 100.0         # Victory
        )
        
        return fitness
    
    async def run(self):
        """
        Main combat loop using evolved parameters
        
        The genome determines:
        - How aggressive to be
        - Preferred fighting distance
        - When to dodge vs attack
        - Fire power decisions
        """
        while self.is_running():
            self.survival_time += 1
            
            # Scan for enemies
            self.radar_turn_rate = 45
            
            if self.current_target:
                await self.execute_tactics()
            else:
                # No target, search
                self.target_speed = 5
                self.turn_rate = 5
            
            await self.go()
    
    async def execute_tactics(self):
        """
        Execute combat tactics based on genome parameters
        
        This is where the evolved parameters influence behavior!
        """
        enemy = self.scanned_enemies.get(self.current_target)
        if not enemy:
            return
        
        # Calculate distance to enemy
        dx = enemy['x'] - self.get_x()
        dy = enemy['y'] - self.get_y()
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Determine range category using genome parameters
        if distance < self.genome.close_range_dist:
            range_pref = self.genome.close_range_weight
            range_type = "close"
        elif distance < self.genome.long_range_dist:
            range_pref = self.genome.medium_range_weight
            range_type = "medium"
        else:
            range_pref = self.genome.long_range_weight
            range_type = "long"
        
        # Decide: Attack or Retreat?
        low_health = self.get_energy() < self.genome.energy_threshold
        
        if low_health:
            # Defensive mode: retreat
            await self.retreat_from_enemy(dx, dy, distance)
        else:
            # Offensive mode: use evolved aggression
            if random.random() < self.genome.aggression * (range_pref / 10.0):
                await self.approach_enemy(dx, dy, distance)
            else:
                await self.maintain_distance(dx, dy, distance)
        
        # Fire based on distance
        await self.fire_at_enemy(enemy, distance)
        
        # Dodge if needed
        if random.random() < self.genome.dodge_intensity:
            await self.execute_dodge()
        
        # Wall avoidance using genome parameter
        await self.avoid_walls()
    
    async def approach_enemy(self, dx, dy, distance):
        """Move toward enemy"""
        angle_to_enemy = math.atan2(dy, dx)
        angle_diff = self.normalize_angle(math.degrees(angle_to_enemy) - self.get_direction())
        
        self.turn_rate = angle_diff * 0.5
        self.target_speed = 8
    
    async def retreat_from_enemy(self, dx, dy, distance):
        """Move away from enemy"""
        angle_to_enemy = math.atan2(dy, dx)
        # Turn opposite direction
        retreat_angle = math.degrees(angle_to_enemy) + 180
        angle_diff = self.normalize_angle(retreat_angle - self.get_direction())
        
        self.turn_rate = angle_diff * 0.5
        self.target_speed = 8
    
    async def maintain_distance(self, dx, dy, distance):
        """Circle around enemy"""
        angle_to_enemy = math.atan2(dy, dx)
        # Perpendicular movement
        circle_angle = math.degrees(angle_to_enemy) + 90
        angle_diff = self.normalize_angle(circle_angle - self.get_direction())
        
        self.turn_rate = angle_diff * 0.3
        self.target_speed = 6
    
    async def fire_at_enemy(self, enemy, distance):
        """
        Fire at enemy with power based on distance and genome
        
        Evolved parameters determine fire power strategy
        """
        # Scale fire power based on distance
        if distance < self.genome.close_range_dist:
            fire_power = self.genome.fire_power_max
        elif distance < self.genome.long_range_dist:
            fire_power = (self.genome.fire_power_min + self.genome.fire_power_max) / 2
        else:
            fire_power = self.genome.fire_power_min
        
        # Aim at enemy
        dx = enemy['x'] - self.get_x()
        dy = enemy['y'] - self.get_y()
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        gun_turn = self.normalize_angle(angle_to_enemy - self.get_gun_direction())
        
        self.gun_turn_rate = gun_turn
        
        # Fire if roughly aimed
        if abs(gun_turn) < 10 and self.gun_heat == 0:
            await self.fire(fire_power)
            self.shots_fired += 1
    
    async def execute_dodge(self):
        """Quick dodge movement based on genome dodge_intensity"""
        dodge_turn = random.choice([-45, 45]) * self.genome.dodge_intensity
        self.turn_rate = dodge_turn
    
    async def avoid_walls(self):
        """
        Avoid arena walls using genome wall_avoidance parameter
        
        Higher wall_avoidance = stronger repulsion from walls
        """
        arena_width = self.get_arena_width()
        arena_height = self.get_arena_height()
        margin = 100
        
        # Calculate repulsion from each wall
        repulsion = 0
        
        if self.get_x() < margin:
            repulsion = (margin - self.get_x()) * self.genome.wall_avoidance
            self.turn_rate += repulsion * 0.1
        elif self.get_x() > arena_width - margin:
            repulsion = (self.get_x() - (arena_width - margin)) * self.genome.wall_avoidance
            self.turn_rate -= repulsion * 0.1
        
        if self.get_y() < margin:
            repulsion = (margin - self.get_y()) * self.genome.wall_avoidance
            self.turn_rate += repulsion * 0.1
        elif self.get_y() > arena_height - margin:
            repulsion = (self.get_y() - (arena_height - margin)) * self.genome.wall_avoidance
            self.turn_rate -= repulsion * 0.1
    
    def normalize_angle(self, angle):
        """Normalize angle to [-180, 180]"""
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    async def on_scanned_bot(self, event):
        """Track scanned enemy"""
        self.scanned_enemies[event.scanned_bot_id] = {
            'x': event.x,
            'y': event.y,
            'energy': event.energy,
            'direction': event.direction,
            'speed': event.speed,
            'scan_time': self.time
        }
        self.current_target = event.scanned_bot_id
    
    async def on_hit_bot(self, event):
        """Track collision with bot"""
        pass
    
    async def on_hit_by_bullet(self, event):
        """Track damage taken"""
        self.damage_taken += event.damage
    
    async def on_bullet_hit(self, event):
        """Track successful hit"""
        self.damage_dealt += event.damage
        self.hits_landed += 1
    
    async def on_bullet_missed(self, event):
        """Track missed shot"""
        pass
    
    async def on_hit_wall(self, event):
        """Track wall collision"""
        self.wall_hits += 1
    
    async def on_bot_death(self, event):
        """Track kill"""
        if event.victim_id in self.scanned_enemies:
            self.enemies_killed += 1
    
    async def on_death(self, event):
        """Calculate final fitness when we die"""
        fitness = self.calculate_fitness()
        print(f"\n💀 Battle ended. Fitness: {fitness:.1f}")
        print(f"   Damage dealt: {self.damage_dealt:.1f}")
        print(f"   Damage taken: {self.damage_taken:.1f}")
        print(f"   Hit rate: {self.hits_landed}/{self.shots_fired}")
        print(f"   Survival time: {self.survival_time}")
        
        # Update genome fitness
        self.genome.fitness = fitness
        self.genome.battles_fought += 1
    
    async def on_win(self, event):
        """Calculate final fitness when we win"""
        fitness = self.calculate_fitness()
        fitness += 500  # Bonus for winning!
        print(f"\n🏆 Victory! Fitness: {fitness:.1f}")
        
        self.genome.fitness = fitness
        self.genome.battles_fought += 1


# ============= TRAINING MODE =============

def train_genetic_algorithm(generations: int = 50, population_size: int = 20):
    """
    Train the genetic algorithm over multiple generations
    
    This would typically run many battles, but requires integration
    with the battle system. For now, this is a template.
    """
    print("🧬 Starting Genetic Algorithm Training")
    print(f"   Generations: {generations}")
    print(f"   Population size: {population_size}")
    
    engine = GeneticEvolutionEngine(population_size)
    
    # Try to load existing population or create new
    if not engine.load_population():
        engine.initialize_population()
    
    for gen in range(generations):
        print(f"\n{'='*60}")
        print(f"Generation {gen + 1}/{generations}")
        print(f"{'='*60}")
        
        # In a real implementation, you would:
        # 1. For each genome in population:
        #    - Create a GeneticTank with that genome
        #    - Run battles against various opponents
        #    - Update genome.fitness based on results
        # 2. Call engine.evolve_generation()
        # 3. Save progress
        
        # Placeholder: Random fitness for demonstration
        for genome in engine.population:
            # This should be replaced with actual battle results
            genome.fitness = random.uniform(-100, 500)
        
        # Evolve to next generation
        engine.evolve_generation()
        
        # Save progress every 5 generations
        if (gen + 1) % 5 == 0:
            engine.save_population()
            
            # Save best genome separately
            if engine.best_genome:
                with open("genetic_best.json", 'w') as f:
                    json.dump(asdict(engine.best_genome), f, indent=2)
    
    print(f"\n✅ Training complete!")
    print(f"   Best fitness achieved: {engine.best_fitness:.1f}")
    engine.save_population()


# ============= MAIN =============

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genetic Tank - Evolutionary Combat AI')
    parser.add_argument('--mode', choices=['battle', 'train'], default='battle',
                       help='battle: Use best evolved params, train: Run genetic algorithm')
    parser.add_argument('--generations', type=int, default=50,
                       help='Number of generations for training')
    parser.add_argument('--population', type=int, default=20,
                       help='Population size for training')
    
    args = parser.parse_args()
    
    if args.mode == 'train':
        train_genetic_algorithm(args.generations, args.population)
    else:
        # Battle mode: Create bot and connect
        import asyncio
        import sys
        
        # Load bot info from file
        script_dir = Path(__file__).parent
        bot_info_path = script_dir / "genetic_tank.json"
        
        if not bot_info_path.exists():
            print(f"❌ Bot info file not found: {bot_info_path}")
            print("   Create genetic_tank.json with bot configuration")
            sys.exit(1)
        
        with open(bot_info_path) as f:
            bot_info_dict = json.load(f)
        
        bot_info = BotInfo.from_dict(bot_info_dict)
        bot = GeneticTank(bot_info=bot_info)
        
        print("🚀 Starting Genetic Tank with evolved parameters...")
        print(f"   Aggression: {bot.genome.aggression:.2f}")
        print(f"   Close/Med/Long weights: {bot.genome.close_range_weight:.1f}/"
              f"{bot.genome.medium_range_weight:.1f}/{bot.genome.long_range_weight:.1f}")
        
        asyncio.run(bot.start())
