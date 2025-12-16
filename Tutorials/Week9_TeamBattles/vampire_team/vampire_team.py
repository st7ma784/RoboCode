"""
Vampire Team - Energy Farming Strategy

This team uses a unique energy farming mechanic where servant bots
sacrifice themselves to heal the master vampire when needed.

Strategy:
- Master: Powerful combat bot that farms servants for energy
- Servants: Stay near master, allow themselves to be shot for energy transfer
- Master gains +3 energy per hit on servant (minus bullet cost)
- Servants respawn after death, repeat cycle

Roles:
- VampireMaster: Main combat bot with high firepower
- VampireServant1: Energy source, defensive positioning
- VampireServant2: Energy source, defensive positioning

Mechanics:
- When Master HP < 50: Farm nearest servant
- When Master HP > 70: Full combat mode against enemies
- Servants avoid enemies, prioritize survival to feed master
- Servants position near master but not too close (avoid splash)
"""

import asyncio
import math
from robocode_tank_royale.bot_api import Bot, BotInfo
from robocode_tank_royale.bot_api.events import ScannedBotEvent, HitBotEvent


class VampireBot(Bot):
    """Base class for vampire team members"""
    
    def __init__(self, bot_info: BotInfo):
        super().__init__(bot_info=bot_info)
        self.role = self.get_role()
        self.master_position = None
        self.servants = {}
        self.enemies = {}
        self.farming_mode = False
        self.target_servant = None
        
    def get_role(self):
        """Determine role based on bot name"""
        name_lower = self.name.lower()
        if "master" in name_lower:
            return "MASTER"
        elif "servant1" in name_lower or "vampire1" in name_lower:
            return "SERVANT1"
        elif "servant2" in name_lower or "vampire2" in name_lower:
            return "SERVANT2"
        return "SERVANT"
    
    async def run(self):
        """Main bot loop"""
        # Set colors based on role
        if self.role == "MASTER":
            self.body_color = "#8B0000"  # Dark red master
            self.turret_color = "#FF0000"
            self.radar_color = "#FF4444"
            self.scan_color = "#8B0000"
        else:
            self.body_color = "#4B0082"  # Indigo servants
            self.turret_color = "#6A5ACD"
            self.radar_color = "#9370DB"
            self.scan_color = "#4B0082"
        
        while self.is_running():
            # Constant radar sweep
            self.radar_turn_rate = 45
            
            if self.role == "MASTER":
                await self.master_behavior()
            else:
                await self.servant_behavior()
            
            await self.go()
    
    async def master_behavior(self):
        """Vampire master farms servants and fights enemies"""
        # Decide whether to farm or fight
        energy_threshold_low = 50
        energy_threshold_high = 70
        
        if self.energy < energy_threshold_low and self.servants:
            # Low energy - farm a servant
            self.farming_mode = True
            
            # Find closest servant
            closest_servant = None
            min_distance = float('inf')
            
            for servant_id, servant in self.servants.items():
                distance = math.sqrt((servant['x'] - self.x)**2 + (servant['y'] - self.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_servant = servant
                    self.target_servant = servant_id
            
            if closest_servant:
                # Move toward servant
                angle = math.degrees(math.atan2(
                    closest_servant['x'] - self.x,
                    closest_servant['y'] - self.y
                ))
                
                turn = (angle - self.direction + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.4
                
                # Maintain farming distance (100-150 pixels)
                if min_distance > 150:
                    self.target_speed = 60
                elif min_distance < 100:
                    self.target_speed = -30
                else:
                    self.target_speed = 20
                
                # Aim at servant
                turret_angle = (angle - self.gun_direction + 360) % 360
                if turret_angle > 180:
                    turret_angle -= 360
                self.gun_turn_rate = turret_angle
                
                # Fire weak shots to farm energy efficiently
                if abs(turret_angle) < 5 and self.gun_heat == 0:
                    self.fire = 1.0  # 1.0 power = costs 1, gains 3 = +2 net
        
        elif self.energy > energy_threshold_high or not self.servants:
            # Good energy or no servants - combat mode
            self.farming_mode = False
            
            if self.enemies:
                # Find best target (closest or weakest)
                target = min(self.enemies.values(), 
                           key=lambda e: e['distance'] if e['energy'] > 20 else e['energy'])
                
                # Calculate angle to target
                angle = math.degrees(math.atan2(
                    target['x'] - self.x,
                    target['y'] - self.y
                ))
                
                # Advanced movement - stay at optimal range
                distance = target['distance']
                if distance > 300:
                    # Close in
                    turn = (angle - self.direction + 360) % 360
                    if turn > 180:
                        turn -= 360
                    self.turn_rate = turn * 0.4
                    self.target_speed = 100
                elif distance < 150:
                    # Back off
                    turn = (angle - self.direction + 180 + 360) % 360
                    if turn > 180:
                        turn -= 360
                    self.turn_rate = turn * 0.3
                    self.target_speed = -50
                else:
                    # Optimal range - strafe
                    turn = (angle - self.direction + 90 + 360) % 360
                    if turn > 180:
                        turn -= 360
                    self.turn_rate = turn * 0.2
                    self.target_speed = 50
                
                # Aim and fire
                turret_angle = (angle - self.gun_direction + 360) % 360
                if turret_angle > 180:
                    turret_angle -= 360
                self.gun_turn_rate = turret_angle
                
                if abs(turret_angle) < 10 and self.gun_heat == 0:
                    # Variable power based on distance and energy
                    if distance < 150:
                        power = 3.0
                    elif distance < 300:
                        power = 2.5
                    else:
                        power = 2.0
                    
                    power = min(power, self.energy / 5)  # Don't use too much energy
                    self.fire = power
            else:
                # No enemies, patrol
                self.target_speed = 50
                self.turn_rate = 10
        else:
            # Mid-range energy - cautious combat
            self.farming_mode = False
            
            # Stay defensive, conserve energy
            if self.enemies:
                target = min(self.enemies.values(), key=lambda e: e['distance'])
                
                # Maintain distance
                angle = math.degrees(math.atan2(
                    target['x'] - self.x,
                    target['y'] - self.y
                ))
                
                # Keep distance
                if target['distance'] < 250:
                    turn = (angle - self.direction + 180 + 360) % 360
                    if turn > 180:
                        turn -= 360
                    self.turn_rate = turn * 0.3
                    self.target_speed = 70
                else:
                    self.target_speed = 30
                    self.turn_rate = 5
                
                # Fire conservatively
                turret_angle = (angle - self.gun_direction + 360) % 360
                if turret_angle > 180:
                    turret_angle -= 360
                self.gun_turn_rate = turret_angle
                
                if abs(turret_angle) < 10 and self.gun_heat == 0:
                    self.fire = 1.5
    
    async def servant_behavior(self):
        """Servants stay near master and avoid enemies"""
        if self.master_position:
            master_x, master_y = self.master_position
            
            # Calculate distance to master
            distance_to_master = math.sqrt((master_x - self.x)**2 + (master_y - self.y)**2)
            
            # Stay near master but not too close
            optimal_distance = 120
            
            if distance_to_master > optimal_distance + 50:
                # Too far, move toward master
                angle = math.degrees(math.atan2(master_x - self.x, master_y - self.y))
                turn = (angle - self.direction + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.5
                self.target_speed = 80
            elif distance_to_master < optimal_distance - 30:
                # Too close, move away
                angle = math.degrees(math.atan2(master_x - self.x, master_y - self.y))
                turn = (angle - self.direction + 180 + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.4
                self.target_speed = 50
            else:
                # Good distance, orbit master
                angle = math.degrees(math.atan2(master_x - self.x, master_y - self.y))
                # Orbit clockwise for servant1, counter-clockwise for servant2
                orbit_direction = 90 if self.role == "SERVANT1" else -90
                turn = (angle - self.direction + orbit_direction + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.3
                self.target_speed = 40
            
            # If enemies nearby, evade!
            if self.enemies:
                closest_enemy = min(self.enemies.values(), key=lambda e: e['distance'])
                if closest_enemy['distance'] < 200:
                    # Run away from enemy
                    angle = math.degrees(math.atan2(
                        closest_enemy['x'] - self.x,
                        closest_enemy['y'] - self.y
                    ))
                    turn = (angle - self.direction + 180 + 360) % 360
                    if turn > 180:
                        turn -= 360
                    self.turn_rate = turn * 0.6
                    self.target_speed = 100
        else:
            # Don't know where master is, search center
            center_x = self.arena_width / 2
            center_y = self.arena_height / 2
            
            angle = math.degrees(math.atan2(center_x - self.x, center_y - self.y))
            turn = (angle - self.direction + 360) % 360
            if turn > 180:
                turn -= 360
            self.turn_rate = turn * 0.3
            self.target_speed = 60
    
    async def on_scanned_bot(self, event: ScannedBotEvent):
        """Track all bots"""
        # Enemy position is directly from event
        scanned_x = event.x
        scanned_y = event.y
        
        # Calculate distance from coordinates
        dx = event.x - self.x
        dy = event.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        bot_data = {
            'x': scanned_x,
            'y': scanned_y,
            'energy': event.energy,
            'distance': distance
        }
        
        if event.is_teammate:
            # Check if master or servant
            # This is a simplification - in real implementation, 
            # you'd need to identify which teammate
            if self.role == "MASTER":
                self.servants[event.scanned_bot_id] = bot_data
            else:
                # Servant tracking master
                self.master_position = (scanned_x, scanned_y)
        else:
            # Enemy
            self.enemies[event.scanned_bot_id] = bot_data
    
    async def on_hit_by_bullet(self, event):
        """React to being hit"""
        if self.role == "MASTER":
            # Master dodges
            self.turn_rate = 60
        else:
            # Servant evades aggressively
            self.turn_rate = 90
            self.target_speed = -100
    
    async def on_hit_bot(self, event: HitBotEvent):
        """React to collision"""
        self.target_speed = -100
        self.turn_rate = 90


# Create the three team members
class VampireMaster(VampireBot):
    """Master vampire bot"""
    pass


class VampireServant1(VampireBot):
    """First servant bot"""
    pass


class VampireServant2(VampireBot):
    """Second servant bot"""
    pass


# Entry points
if __name__ == "__main__":
    import sys
    
    bot_info = BotInfo.from_file("vampire_team.json")
    
    if len(sys.argv) > 1:
        role = sys.argv[1].lower()
    else:
        role = "master"
    
    if role == "master":
        bot = VampireMaster(bot_info=bot_info)
    elif role == "servant1":
        bot = VampireServant1(bot_info=bot_info)
    else:
        bot = VampireServant2(bot_info=bot_info)
    
    asyncio.run(bot.start())
