"""
Q-Learning Tank - Reinforcement Learning for Combat AI
Week 11: Q-Learning - Real-Time Learning

This tank demonstrates:
- Q-Learning algorithm implementation
- State discretization for combat scenarios
- Epsilon-greedy exploration strategy
- Experience-based learning
- Persistent Q-table storage

The bot learns optimal combat tactics through trial and error,
updating its Q-values based on rewards from actions taken!
"""
from robocode_tank_royale.bot_api import Bot, BotInfo
import math
import random
import pickle
import os
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import argparse
import numpy as np


@dataclass
class CombatState:
    """
    Represents a discretized combat state
    
    We convert continuous values (position, energy, etc.) into
    discrete buckets to make the state space manageable for Q-learning.
    """
    my_health_bucket: int      # 0=low, 1=medium, 2=high
    enemy_health_bucket: int   # 0=low, 1=medium, 2=high
    distance_bucket: int       # 0=close, 1=medium, 2=far
    angle_bucket: int          # 0=front, 1=side, 2=back
    speed_bucket: int          # 0=stopped, 1=slow, 2=fast
    
    def to_tuple(self) -> Tuple:
        """Convert to hashable tuple for Q-table indexing"""
        return (
            self.my_health_bucket,
            self.enemy_health_bucket,
            self.distance_bucket,
            self.angle_bucket,
            self.speed_bucket
        )
    
    @staticmethod
    def from_combat_data(my_energy, enemy_energy, distance, angle, speed) -> 'CombatState':
        """
        Create state from continuous combat data
        
        This is where we discretize continuous values into buckets
        """
        # Health buckets: high (60+), medium (30-60), low (0-30)
        my_health = 2 if my_energy > 60 else (1 if my_energy > 30 else 0)
        enemy_health = 2 if enemy_energy > 60 else (1 if enemy_energy > 30 else 0)
        
        # Distance buckets: close (<200), medium (200-500), far (500+)
        dist = 0 if distance < 200 else (1 if distance < 500 else 2)
        
        # Angle buckets: front (±45°), side (45-135°), back (135-180°)
        abs_angle = abs(angle)
        ang = 0 if abs_angle < 45 else (1 if abs_angle < 135 else 2)
        
        # Speed buckets: stopped (<2), slow (2-5), fast (5+)
        spd = 0 if abs(speed) < 2 else (1 if abs(speed) < 5 else 2)
        
        return CombatState(my_health, enemy_health, dist, ang, spd)


class QLearningBrain:
    """
    Q-Learning algorithm implementation
    
    Manages:
    - Q-table: Maps (state, action) → expected reward
    - Learning: Updates Q-values based on experience
    - Exploration: Balances trying new vs known actions
    - Persistence: Saves/loads learned Q-table
    """
    
    # Define our action space
    ACTIONS = {
        0: "forward_shoot_heavy",
        1: "forward_shoot_light",
        2: "turn_left_shoot",
        3: "turn_right_shoot",
        4: "retreat_shoot",
        5: "circle_left_shoot",
        6: "circle_right_shoot",
        7: "stop_shoot_heavy"
    }
    
    def __init__(self, 
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.9,
                 epsilon: float = 0.1,
                 save_path: str = "qlearning_qtable.pkl"):
        """
        Initialize Q-Learning brain
        
        Args:
            learning_rate (α): How much to update Q-values (0.0-1.0)
            discount_factor (γ): Value of future rewards (0.0-1.0)
            epsilon (ε): Exploration rate (0.0-1.0)
            save_path: Where to save/load Q-table
        """
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.save_path = save_path
        
        # Q-table: maps (state, action) → Q-value
        # Use defaultdict so unseen states start at 0
        self.q_table: Dict[Tuple, np.ndarray] = defaultdict(lambda: np.zeros(len(self.ACTIONS)))
        
        # Statistics
        self.states_visited = set()
        self.total_updates = 0
        
        # Load existing Q-table if available
        self.load_qtable()
    
    def get_action(self, state: CombatState, explore: bool = True) -> int:
        """
        Choose action using epsilon-greedy strategy
        
        Args:
            state: Current combat state
            explore: If True, uses epsilon-greedy. If False, always exploits.
        
        Returns:
            action: Integer action ID (0-7)
        """
        state_tuple = state.to_tuple()
        self.states_visited.add(state_tuple)
        
        # Epsilon-greedy: explore vs exploit
        if explore and random.random() < self.epsilon:
            # Explore: random action
            return random.randint(0, len(self.ACTIONS) - 1)
        else:
            # Exploit: choose best known action
            q_values = self.q_table[state_tuple]
            return int(np.argmax(q_values))
    
    def update(self, 
               state: CombatState, 
               action: int, 
               reward: float, 
               next_state: CombatState,
               done: bool = False):
        """
        Update Q-value based on experience
        
        This is the core Q-Learning update rule:
        Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
        
        Args:
            state: State before action
            action: Action taken
            reward: Immediate reward received
            next_state: State after action
            done: True if episode ended (bot died)
        """
        state_tuple = state.to_tuple()
        next_state_tuple = next_state.to_tuple()
        
        # Current Q-value
        current_q = self.q_table[state_tuple][action]
        
        # Best future Q-value (or 0 if episode ended)
        if done:
            max_next_q = 0
        else:
            max_next_q = np.max(self.q_table[next_state_tuple])
        
        # TD target: r + γ·max Q(s',a')
        target = reward + self.gamma * max_next_q
        
        # TD error: target - current
        td_error = target - current_q
        
        # Update: Q(s,a) ← Q(s,a) + α·TD_error
        self.q_table[state_tuple][action] += self.alpha * td_error
        
        self.total_updates += 1
    
    def save_qtable(self):
        """Save Q-table to disk"""
        with open(self.save_path, 'wb') as f:
            # Convert defaultdict to regular dict for pickling
            q_dict = dict(self.q_table)
            pickle.dump({
                'q_table': q_dict,
                'states_visited': self.states_visited,
                'total_updates': self.total_updates
            }, f)
        print(f"💾 Saved Q-table with {len(self.q_table)} states, {self.total_updates} updates")
    
    def load_qtable(self):
        """Load Q-table from disk"""
        if not os.path.exists(self.save_path):
            print("📋 No existing Q-table found, starting fresh")
            return
        
        try:
            with open(self.save_path, 'rb') as f:
                data = pickle.load(f)
            
            # Convert back to defaultdict
            q_dict = data['q_table']
            self.q_table = defaultdict(lambda: np.zeros(len(self.ACTIONS)), q_dict)
            self.states_visited = data.get('states_visited', set())
            self.total_updates = data.get('total_updates', 0)
            
            print(f"📂 Loaded Q-table with {len(self.q_table)} states, {self.total_updates} updates")
        except Exception as e:
            print(f"⚠️  Failed to load Q-table: {e}")
    
    def print_statistics(self):
        """Print learning statistics"""
        print("\n" + "="*60)
        print("Q-LEARNING STATISTICS")
        print("="*60)
        print(f"Total states visited: {len(self.states_visited)}")
        print(f"Q-table entries: {len(self.q_table)}")
        print(f"Total updates: {self.total_updates}")
        print(f"Current epsilon: {self.epsilon:.3f}")
        print(f"Learning rate (α): {self.alpha:.3f}")
        print(f"Discount factor (γ): {self.gamma:.3f}")
        
        if len(self.q_table) > 0:
            # Show sample Q-values
            print("\nSample Q-values for random states:")
            for i, (state, q_values) in enumerate(list(self.q_table.items())[:3]):
                best_action = np.argmax(q_values)
                print(f"  State {state}:")
                print(f"    Best action: {self.ACTIONS[best_action]} (Q={q_values[best_action]:.2f})")
        print("="*60)


class QLearningTank(Bot):
    """
    A tank that learns combat tactics through Q-Learning
    
    The bot:
    1. Observes current state (health, distance, angle, etc.)
    2. Chooses action (explore or exploit)
    3. Executes action and observes outcome
    4. Receives reward based on outcome
    5. Updates Q-values to learn from experience
    """
    
    def __init__(self, bot_info: BotInfo, brain: Optional[QLearningBrain] = None):
        super().__init__(bot_info)
        
        # Q-Learning brain
        self.brain = brain if brain else QLearningBrain()
        
        # Combat tracking
        self.current_state: Optional[CombatState] = None
        self.current_action: Optional[int] = None
        self.last_energy = 100.0
        self.last_enemy_energy = 100.0
        self.episode_reward = 0.0
        self.episode_steps = 0
        
        # Enemy tracking
        self.scanned_enemies = {}
        self.current_target = None
        
        # Statistics
        self.damage_dealt = 0.0
        self.damage_taken = 0.0
        self.hits_landed = 0
        self.shots_fired = 0
        self.wall_hits = 0
    
    async def run(self):
        """
        Main Q-Learning loop
        
        This implements the classic RL loop:
        observe → act → observe → reward → learn → repeat
        """
        print("🤖 Q-Learning Tank activated!")
        print(f"   Exploration (ε): {self.brain.epsilon:.2f}")
        print(f"   Q-table size: {len(self.brain.q_table)} states")
        
        while self.is_running():
            self.episode_steps += 1
            
            # Always scan for enemies
            self.radar_turn_rate = 45
            
            if self.current_target and self.current_target in self.scanned_enemies:
                # We have a target - do Q-Learning!
                await self.qlearning_step()
            else:
                # No target - search
                self.target_speed = 5
                self.turn_rate = 10
            
            await self.go()
    
    async def qlearning_step(self):
        """
        Execute one Q-Learning step
        
        1. Get current state
        2. If we have previous state/action, update Q-value
        3. Choose next action
        4. Execute action
        """
        enemy = self.scanned_enemies[self.current_target]
        
        # Calculate state features
        distance = self.calculate_distance_to_enemy(enemy)
        angle = self.calculate_angle_to_enemy(enemy)
        
        # Create current state
        new_state = CombatState.from_combat_data(
            my_energy=self.get_energy(),
            enemy_energy=enemy['energy'],
            distance=distance,
            angle=angle,
            speed=self.speed
        )
        
        # If we have a previous state/action, update Q-value
        if self.current_state is not None and self.current_action is not None:
            reward = self.calculate_reward(enemy, distance)
            self.episode_reward += reward
            
            self.brain.update(
                state=self.current_state,
                action=self.current_action,
                reward=reward,
                next_state=new_state,
                done=False
            )
        
        # Choose next action using Q-Learning brain
        action = self.brain.get_action(new_state, explore=True)
        
        # Execute the chosen action
        await self.execute_action(action, enemy, distance)
        
        # Remember for next step
        self.current_state = new_state
        self.current_action = action
    
    def calculate_reward(self, enemy, distance) -> float:
        """
        Calculate reward based on recent outcomes
        
        This reward function shapes what the bot learns!
        Positive rewards for good outcomes, negative for bad.
        """
        reward = 0.0
        
        # Reward for damage dealt
        if enemy['energy'] < self.last_enemy_energy:
            damage = self.last_enemy_energy - enemy['energy']
            reward += damage * 10.0  # Major reward for hitting
        
        # Penalty for damage taken
        if self.get_energy() < self.last_energy:
            damage = self.last_energy - self.get_energy()
            reward -= damage * 5.0   # Penalty for getting hit
        
        # Positional rewards (context-dependent)
        if self.get_energy() > 50:
            # When healthy, reward getting closer (aggression)
            if distance < 300:
                reward += 2.0
        else:
            # When low health, reward keeping distance (defense)
            if distance > 400:
                reward += 2.0
        
        # Small survival reward
        reward += 0.1
        
        # Update tracking
        self.last_energy = self.get_energy()
        self.last_enemy_energy = enemy['energy']
        
        return reward
    
    async def execute_action(self, action: int, enemy: dict, distance: float):
        """
        Execute the chosen action
        
        Each action is a combination of movement and shooting
        """
        # Calculate angle to enemy for aiming
        dx = enemy['x'] - self.get_x()
        dy = enemy['y'] - self.get_y()
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        
        # Aim gun at enemy
        gun_turn = self.normalize_angle(angle_to_enemy - self.get_gun_direction())
        self.gun_turn_rate = gun_turn
        
        # Execute action
        if action == 0:  # forward_shoot_heavy
            self.target_speed = 8
            self.turn_rate = gun_turn * 0.3
            if abs(gun_turn) < 15 and self.gun_heat == 0:
                await self.fire(3.0)
                self.shots_fired += 1
        
        elif action == 1:  # forward_shoot_light
            self.target_speed = 8
            self.turn_rate = gun_turn * 0.3
            if abs(gun_turn) < 20 and self.gun_heat == 0:
                await self.fire(1.0)
                self.shots_fired += 1
        
        elif action == 2:  # turn_left_shoot
            self.target_speed = 5
            self.turn_rate = -30
            if abs(gun_turn) < 25 and self.gun_heat == 0:
                await self.fire(2.0)
                self.shots_fired += 1
        
        elif action == 3:  # turn_right_shoot
            self.target_speed = 5
            self.turn_rate = 30
            if abs(gun_turn) < 25 and self.gun_heat == 0:
                await self.fire(2.0)
                self.shots_fired += 1
        
        elif action == 4:  # retreat_shoot
            # Move away from enemy
            retreat_angle = angle_to_enemy + 180
            turn_needed = self.normalize_angle(retreat_angle - self.get_direction())
            self.target_speed = 8
            self.turn_rate = turn_needed * 0.4
            if abs(gun_turn) < 20 and self.gun_heat == 0:
                await self.fire(1.5)
                self.shots_fired += 1
        
        elif action == 5:  # circle_left_shoot
            # Strafe left around enemy
            circle_angle = angle_to_enemy + 90
            turn_needed = self.normalize_angle(circle_angle - self.get_direction())
            self.target_speed = 7
            self.turn_rate = turn_needed * 0.3
            if abs(gun_turn) < 20 and self.gun_heat == 0:
                await self.fire(2.0)
                self.shots_fired += 1
        
        elif action == 6:  # circle_right_shoot
            # Strafe right around enemy
            circle_angle = angle_to_enemy - 90
            turn_needed = self.normalize_angle(circle_angle - self.get_direction())
            self.target_speed = 7
            self.turn_rate = turn_needed * 0.3
            if abs(gun_turn) < 20 and self.gun_heat == 0:
                await self.fire(2.0)
                self.shots_fired += 1
        
        elif action == 7:  # stop_shoot_heavy
            self.target_speed = 0
            self.turn_rate = 0
            if abs(gun_turn) < 10 and self.gun_heat == 0:
                await self.fire(3.0)
                self.shots_fired += 1
    
    def calculate_distance_to_enemy(self, enemy: dict) -> float:
        """Calculate Euclidean distance to enemy"""
        dx = enemy['x'] - self.get_x()
        dy = enemy['y'] - self.get_y()
        return math.sqrt(dx*dx + dy*dy)
    
    def calculate_angle_to_enemy(self, enemy: dict) -> float:
        """Calculate angle to enemy relative to our direction"""
        dx = enemy['x'] - self.get_x()
        dy = enemy['y'] - self.get_y()
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        return self.normalize_angle(angle_to_enemy - self.get_direction())
    
    def normalize_angle(self, angle: float) -> float:
        """Normalize angle to [-180, 180]"""
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    async def on_scanned_bot(self, event):
        """Track scanned enemies"""
        self.scanned_enemies[event.scanned_bot_id] = {
            'x': event.x,
            'y': event.y,
            'energy': event.energy,
            'direction': event.direction,
            'speed': event.speed,
            'scan_time': self.time
        }
        
        if not self.current_target:
            self.current_target = event.scanned_bot_id
            self.last_enemy_energy = event.energy
    
    async def on_hit_by_bullet(self, event):
        """Track damage taken"""
        self.damage_taken += event.damage
    
    async def on_bullet_hit(self, event):
        """Track successful hit"""
        self.damage_dealt += event.damage
        self.hits_landed += 1
    
    async def on_hit_wall(self, event):
        """Penalty for hitting wall"""
        self.wall_hits += 1
        
        # Immediate negative reward for wall hit
        if self.current_state and self.current_action is not None:
            self.brain.update(
                state=self.current_state,
                action=self.current_action,
                reward=-10.0,  # Wall hit penalty
                next_state=self.current_state,
                done=False
            )
    
    async def on_bot_death(self, event):
        """Track enemy death"""
        if event.victim_id == self.current_target:
            # Huge reward for killing enemy!
            if self.current_state and self.current_action is not None:
                self.brain.update(
                    state=self.current_state,
                    action=self.current_action,
                    reward=100.0,
                    next_state=self.current_state,
                    done=False
                )
            self.current_target = None
    
    async def on_death(self, event):
        """Learn from death"""
        print(f"\n💀 Episode ended in death")
        
        # Large negative reward for dying
        if self.current_state and self.current_action is not None:
            self.brain.update(
                state=self.current_state,
                action=self.current_action,
                reward=-100.0,
                next_state=self.current_state,
                done=True
            )
        
        self.print_episode_stats()
    
    async def on_win(self, event):
        """Learn from victory"""
        print(f"\n🏆 Episode ended in victory!")
        
        # Bonus reward for winning
        if self.current_state and self.current_action is not None:
            self.brain.update(
                state=self.current_state,
                action=self.current_action,
                reward=200.0,
                next_state=self.current_state,
                done=True
            )
        
        self.print_episode_stats()
    
    def print_episode_stats(self):
        """Print statistics for this episode"""
        hit_rate = self.hits_landed / max(1, self.shots_fired)
        
        print(f"   Episode steps: {self.episode_steps}")
        print(f"   Total reward: {self.episode_reward:.1f}")
        print(f"   Damage dealt: {self.damage_dealt:.1f}")
        print(f"   Damage taken: {self.damage_taken:.1f}")
        print(f"   Hit rate: {self.hits_landed}/{self.shots_fired} ({hit_rate:.1%})")
        print(f"   Wall hits: {self.wall_hits}")
        print(f"   States visited this episode: {len(self.brain.states_visited)}")


# ============= MAIN =============

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Q-Learning Tank - Reinforcement Learning AI')
    parser.add_argument('--mode', choices=['battle', 'analyze'], default='battle',
                       help='battle: Run bot, analyze: Show Q-table stats')
    parser.add_argument('--epsilon', type=float, default=0.1,
                       help='Exploration rate (0.0-1.0)')
    parser.add_argument('--alpha', type=float, default=0.1,
                       help='Learning rate (0.0-1.0)')
    parser.add_argument('--gamma', type=float, default=0.9,
                       help='Discount factor (0.0-1.0)')
    
    args = parser.parse_args()
    
    if args.mode == 'analyze':
        # Just show Q-table statistics
        brain = QLearningBrain(epsilon=args.epsilon, learning_rate=args.alpha, discount_factor=args.gamma)
        brain.print_statistics()
    else:
        # Battle mode
        import asyncio
        import sys
        import json
        
        # Create Q-Learning brain
        brain = QLearningBrain(
            learning_rate=args.alpha,
            discount_factor=args.gamma,
            epsilon=args.epsilon
        )
        
        # Load bot info
        script_dir = Path(__file__).parent
        bot_info_path = script_dir / "qlearning_tank.json"
        
        if not bot_info_path.exists():
            print(f"❌ Bot info file not found: {bot_info_path}")
            print("   Create qlearning_tank.json with bot configuration")
            sys.exit(1)
        
        with open(bot_info_path) as f:
            bot_info_dict = json.load(f)
        
        bot_info = BotInfo.from_dict(bot_info_dict)
        bot = QLearningTank(bot_info=bot_info, brain=brain)
        
        print("🤖 Starting Q-Learning Tank...")
        print(f"   ε (exploration): {args.epsilon}")
        print(f"   α (learning rate): {args.alpha}")
        print(f"   γ (discount): {args.gamma}")
        
        try:
            asyncio.run(bot.start())
        finally:
            # Save Q-table when done
            brain.save_qtable()
            brain.print_statistics()
