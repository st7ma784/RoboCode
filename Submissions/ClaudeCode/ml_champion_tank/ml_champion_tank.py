"""
ML Champion Tank - Working Q-Learning Bot
Based on tutorial pattern with evolved parameters
"""
from robocode_tank_royale.bot_api import Bot, BotInfo
import math
import random
import pickle
import json
import os
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class EvolvableParameters:
    """Evolved parameters"""
    learning_rate: float = 0.15
    discount_factor: float = 0.9
    epsilon_start: float = 0.2
    epsilon_decay: float = 0.995
    epsilon_min: float = 0.05
    damage_dealt_weight: float = 10.0
    damage_taken_weight: float = -5.0
    close_range: float = 200.0
    far_range: float = 500.0


@dataclass
class CombatState:
    my_health: int
    enemy_health: int
    distance: int

    def to_tuple(self):
        return (self.my_health, self.enemy_health, self.distance)

    @staticmethod
    def from_data(my_energy, enemy_energy, distance, params):
        my_h = 2 if my_energy > 60 else (1 if my_energy > 30 else 0)
        enemy_h = 2 if enemy_energy > 60 else (1 if enemy_energy > 30 else 0)
        dist = 0 if distance < params.close_range else (1 if distance < params.far_range else 2)
        return CombatState(my_h, enemy_h, dist)


class QLearningBrain:
    ACTIONS = {
        0: "aggressive_charge",
        1: "defensive_retreat",
        2: "circle_left",
        3: "circle_right",
        4: "strafe_shoot"
    }

    def __init__(self, params):
        self.params = params
        self.q_table = defaultdict(lambda: np.zeros(len(self.ACTIONS)))
        self.epsilon = params.epsilon_start
        self.load_qtable()

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, len(self.ACTIONS) - 1)
        return int(np.argmax(self.q_table[state.to_tuple()]))

    def update(self, state, action, reward, next_state, done=False):
        s, ns = state.to_tuple(), next_state.to_tuple()
        current_q = self.q_table[s][action]
        max_next_q = 0 if done else np.max(self.q_table[ns])
        self.q_table[s][action] += self.params.learning_rate * (reward + self.params.discount_factor * max_next_q - current_q)

    def decay_epsilon(self):
        self.epsilon = max(self.params.epsilon_min, self.epsilon * self.params.epsilon_decay)

    def save_qtable(self):
        with open("ml_champion_qtable.pkl", 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def load_qtable(self):
        if os.path.exists("ml_champion_qtable.pkl"):
            with open("ml_champion_qtable.pkl", 'rb') as f:
                self.q_table = defaultdict(lambda: np.zeros(len(self.ACTIONS)), pickle.load(f))


class MLChampionTank(Bot):
    def __init__(self, bot_info=None):
        super().__init__(bot_info)
        self.params = self.load_params()
        self.brain = QLearningBrain(self.params)

        self.current_state = None
        self.current_action = None
        self.last_my_energy = 100.0
        self.last_enemy_energy = 100.0
        self.episode_reward = 0.0

        self.enemy = None
        self.tick = 0
        self.shots = 0
        self.hits = 0
        self.damage_dealt = 0.0
        self.damage_taken = 0.0

    def load_params(self):
        if os.path.exists("ml_champion_best_params.json"):
            with open("ml_champion_best_params.json") as f:
                data = json.load(f)
            return EvolvableParameters(**{k: v for k, v in data.items() if k in EvolvableParameters.__annotations__})
        return EvolvableParameters()

    async def run(self):
        # Reduced console output for performance
        while self.is_running():
            self.tick += 1

            # Periodic status update
            if self.tick % 100 == 0:
                print(f"🚀 ML Champion! Epsilon: {self.brain.epsilon:.3f}")

            # Keep scanning if no enemy
            if not self.enemy:
                self.radar_turn_rate = 45
                self.target_speed = 6
                self.turn_rate = 10
            else:
                # Lock radar on enemy
                dx = self.enemy['x'] - self.get_x()
                dy = self.enemy['y'] - self.get_y()
                angle_to_enemy = math.degrees(math.atan2(dy, dx))
                radar_turn = self.normalize_angle(angle_to_enemy - self.get_radar_direction())
                self.radar_turn_rate = radar_turn * 2

                await self.execute_qlearning_action()

            await self.go()

    async def execute_qlearning_action(self):
        """Execute action using Q-learning"""
        # Calculate distance
        dx = self.enemy['x'] - self.get_x()
        dy = self.enemy['y'] - self.get_y()
        distance = math.sqrt(dx*dx + dy*dy)

        # Create state
        new_state = CombatState.from_data(
            self.get_energy(), self.enemy['energy'], distance, self.params
        )

        # Update Q-value
        if self.current_state and self.current_action is not None:
            reward = self.calculate_reward()
            self.episode_reward += reward
            self.brain.update(self.current_state, self.current_action, reward, new_state)

        # Choose action
        action = self.brain.get_action(new_state)

        # Execute action (INCLUDES FIRING)
        await self.execute_action(action, dx, dy, distance)

        # Remember
        self.current_state = new_state
        self.current_action = action

    async def execute_action(self, action, dx, dy, distance):
        """Execute action - movement AND firing"""
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        gun_turn = self.normalize_angle(angle_to_enemy - self.get_gun_direction())
        self.gun_turn_rate = gun_turn

        # Choose power
        if distance < self.params.close_range:
            power = 2.5
        elif distance < self.params.far_range:
            power = 2.0
        else:
            power = 1.5

        if self.get_energy() < 20:
            power = 1.0

        # ACTION 0: Aggressive charge
        if action == 0:
            turn_needed = self.normalize_angle(angle_to_enemy - self.get_direction())
            self.turn_rate = turn_needed * 0.5
            self.target_speed = 8

        # ACTION 1: Defensive retreat
        elif action == 1:
            retreat_angle = angle_to_enemy + 180
            turn_needed = self.normalize_angle(retreat_angle - self.get_direction())
            self.turn_rate = turn_needed * 0.5
            self.target_speed = 8

        # ACTION 2: Circle left
        elif action == 2:
            circle_angle = angle_to_enemy + 80
            turn_needed = self.normalize_angle(circle_angle - self.get_direction())
            self.turn_rate = turn_needed * 0.4
            self.target_speed = 7

        # ACTION 3: Circle right
        elif action == 3:
            circle_angle = angle_to_enemy - 80
            turn_needed = self.normalize_angle(circle_angle - self.get_direction())
            self.turn_rate = turn_needed * 0.4
            self.target_speed = 7

        # ACTION 4: Strafe
        else:
            strafe_angle = angle_to_enemy + random.choice([-60, 60])
            turn_needed = self.normalize_angle(strafe_angle - self.get_direction())
            self.turn_rate = turn_needed * 0.4
            self.target_speed = 7

        # Fire after setting movement - VERY AGGRESSIVE!
        # Fire even if gun isn't perfectly aimed to encourage shooting
        if abs(gun_turn) < 60:  # Much more lenient - fire if roughly aimed
            await self.fire(power)
            self.shots += 1

        # Wall avoidance
        margin = 70
        x, y = self.get_x(), self.get_y()
        if x < margin or x > self.get_arena_width() - margin or y < margin or y > self.get_arena_height() - margin:
            center_x, center_y = self.get_arena_width() / 2, self.get_arena_height() / 2
            to_center = math.degrees(math.atan2(center_y - y, center_x - x))
            self.turn_rate = self.normalize_angle(to_center - self.get_direction()) * 0.6

    def calculate_reward(self):
        reward = 0.0

        # Reward for damaging enemy
        if self.enemy['energy'] < self.last_enemy_energy:
            damage = self.last_enemy_energy - self.enemy['energy']
            reward += damage * self.params.damage_dealt_weight

        # Penalty for taking damage
        if self.get_energy() < self.last_my_energy:
            damage = self.last_my_energy - self.get_energy()
            reward += damage * self.params.damage_taken_weight

        # Small reward for being close (encourages aggression)
        dx = self.enemy['x'] - self.get_x()
        dy = self.enemy['y'] - self.get_y()
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < 200:
            reward += 1.0  # Reward for closing distance

        self.last_my_energy = self.get_energy()
        self.last_enemy_energy = self.enemy['energy']
        return reward

    def normalize_angle(self, angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle

    async def on_scanned_bot(self, event):
        self.enemy = {
            'x': event.x,
            'y': event.y,
            'energy': event.energy,
        }
        if self.last_enemy_energy is None or self.last_enemy_energy == 100.0:
            self.last_enemy_energy = event.energy

    async def on_bullet_hit(self, event):
        self.hits += 1
        self.damage_dealt += event.damage

    async def on_hit_by_bullet(self, event):
        self.damage_taken += event.damage

    async def on_death(self, event):
        if self.current_state and self.current_action is not None:
            self.brain.update(self.current_state, self.current_action, -200, self.current_state, True)
        self.print_stats()
        self.brain.save_qtable()
        self.brain.decay_epsilon()

    async def on_win(self, event):
        if self.current_state and self.current_action is not None:
            self.brain.update(self.current_state, self.current_action, 300, self.current_state, True)
        self.print_stats()
        self.brain.save_qtable()
        self.brain.decay_epsilon()

    def print_stats(self):
        hit_rate = self.hits / max(1, self.shots)
        print(f"\n📊 Battle Complete! Accuracy: {hit_rate:.1%}")
        print(f"   Dmg: {self.damage_dealt:.0f} dealt/{self.damage_taken:.0f} taken")
        print(f"   ε: {self.brain.epsilon:.3f} | Q-size: {len(self.brain.q_table)}")


if __name__ == '__main__':
    import asyncio
    bot_info = BotInfo.from_file(str(Path(__file__).parent / "ml_champion_tank.json"))
    bot = MLChampionTank(bot_info=bot_info)
    asyncio.run(bot.start())
