"""
Hunter-Killer Team - Specialized Tracking and Elimination

This team uses role specialization: Hunters scout and relay information,
while the Killer eliminates tagged targets with maximum firepower.

Strategy:
- Hunters: Scout different quadrants, use weak shots to tag enemies
- Killer: Receives target info, moves to intercept, eliminates with power shots
- Hunters retreat when Killer engages

Roles:
- Hunter1: Covers upper quadrant, tracks and tags
- Hunter2: Covers lower quadrant, tracks and tags  
- Killer: Heavy firepower bot, eliminates confirmed targets
"""

import asyncio
import math
from robocode_tank_royale.bot_api import Bot, BotInfo
from robocode_tank_royale.bot_api.events import ScannedBotEvent


class HunterKillerBot(Bot):
    """Base class for hunter-killer team members"""
    
    def __init__(self, bot_info: BotInfo):
        super().__init__(bot_info=bot_info)
        self.role = self.get_role()
        self.shared_targets = {}  # Shared enemy tracking
        self.primary_target = None
        self.killer_engaging = False
        
    def get_role(self):
        """Determine role based on bot name"""
        name_lower = self.name.lower()
        if "killer" in name_lower:
            return "KILLER"
        elif "hunter1" in name_lower:
            return "HUNTER1"
        elif "hunter2" in name_lower:
            return "HUNTER2"
        return "HUNTER"
    
    async def run(self):
        """Main bot loop"""
        # Set colors based on role
        if self.role == "KILLER":
            self.body_color = "#FF0000"  # Red killer
            self.turret_color = "#CC0000"
            self.radar_color = "#990000"
            self.scan_color = "#FF0000"
        else:
            self.body_color = "#00FF00"  # Green hunters
            self.turret_color = "#00CC00"
            self.radar_color = "#009900"
            self.scan_color = "#00FF00"
        
        while self.is_running():
            # Constant radar sweep
            self.radar_turn_rate = 45
            
            if self.role == "KILLER":
                await self.killer_behavior()
            else:
                await self.hunter_behavior()
            
            await self.go()
    
    async def hunter_behavior(self):
        """Hunters scout and tag enemies"""
        # Assign patrol quadrants
        if self.role == "HUNTER1":
            # Upper quadrant
            target_x = self.arena_width * 0.5
            target_y = self.arena_height * 0.75
        else:
            # Lower quadrant
            target_x = self.arena_width * 0.5
            target_y = self.arena_height * 0.25
        
        # Check if killer is engaging
        if self.killer_engaging and self.primary_target:
            # Retreat to give killer room
            retreat_x = self.arena_width * 0.1 if self.x < self.arena_width / 2 else self.arena_width * 0.9
            retreat_y = target_y
            
            angle = math.degrees(math.atan2(retreat_x - self.x, retreat_y - self.y))
            turn = (angle - self.direction + 360) % 360
            if turn > 180:
                turn -= 360
            self.turn_rate = turn * 0.5
            self.target_speed = 80
        else:
            # Patrol quadrant
            distance_to_patrol = math.sqrt((target_x - self.x)**2 + (target_y - self.y)**2)
            
            if distance_to_patrol > 50:
                angle = math.degrees(math.atan2(target_x - self.x, target_y - self.y))
                turn = (angle - self.direction + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.3
                self.target_speed = 60
            else:
                # At patrol point, circle
                self.turn_rate = 15
                self.target_speed = 30
        
        # Track and tag enemies with weak shots
        if self.primary_target:
            target = self.shared_targets[self.primary_target]
            
            # Aim at target
            angle_to_target = math.degrees(math.atan2(
                target['x'] - self.x,
                target['y'] - self.y
            ))
            turret_angle = (angle_to_target - self.gun_direction + 360) % 360
            if turret_angle > 180:
                turret_angle -= 360
            self.gun_turn_rate = turret_angle
            
            # Tag with weak shot (conserve energy)
            if abs(turret_angle) < 10 and self.gun_heat == 0 and not self.killer_engaging:
                self.fire = 0.5  # Weak tagging shot
    
    async def killer_behavior(self):
        """Killer eliminates high-priority targets"""
        if self.primary_target and self.primary_target in self.shared_targets:
            target = self.shared_targets[self.primary_target]
            
            # Calculate intercept course
            angle_to_target = math.degrees(math.atan2(
                target['x'] - self.x,
                target['y'] - self.y
            ))
            
            distance = math.sqrt((target['x'] - self.x)**2 + (target['y'] - self.y)**2)
            
            # Movement strategy
            if distance > 300:
                # Close distance quickly
                turn = (angle_to_target - self.direction + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.5
                self.target_speed = 100
                self.killer_engaging = False
            elif distance < 150:
                # Too close, maintain distance
                turn = (angle_to_target - self.direction + 180 + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.3
                self.target_speed = -50
                self.killer_engaging = True
            else:
                # Optimal range - engage!
                self.killer_engaging = True
                # Strafe movement
                turn = (angle_to_target - self.direction + 90 + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.2
                self.target_speed = 40
            
            # Aim and fire with maximum power
            turret_angle = (angle_to_target - self.gun_direction + 360) % 360
            if turret_angle > 180:
                turret_angle -= 360
            self.gun_turn_rate = turret_angle
            
            # Fire heavy shots when aimed
            if abs(turret_angle) < 8 and self.gun_heat == 0:
                # Calculate bullet speed for lead
                power = 3.0
                bullet_speed = 20 - 3 * power
                
                # Lead target (simple prediction)
                lead_angle = 0
                if distance > 0:
                    travel_time = distance / bullet_speed
                    # Assume target moving perpendicular at speed 8
                    lead_distance = 8 * travel_time
                    lead_angle = math.degrees(math.atan2(lead_distance, distance))
                
                self.gun_turn_rate = lead_angle
                self.fire = power
        else:
            # No target, center position
            center_x = self.arena_width / 2
            center_y = self.arena_height / 2
            
            distance_to_center = math.sqrt((center_x - self.x)**2 + (center_y - self.y)**2)
            
            if distance_to_center > 100:
                angle = math.degrees(math.atan2(center_x - self.x, center_y - self.y))
                turn = (angle - self.direction + 360) % 360
                if turn > 180:
                    turn -= 360
                self.turn_rate = turn * 0.3
                self.target_speed = 50
            else:
                # At center, rotate in place
                self.turn_rate = 10
                self.target_speed = 0
    
    async def on_scanned_bot(self, event: ScannedBotEvent):
        """Track all bots and prioritize targets"""
        # Enemy position is directly from event
        scanned_x = event.x
        scanned_y = event.y
        
        # Calculate distance from coordinates
        dx = event.x - self.x
        dy = event.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if not event.is_teammate:
            # Track enemy
            self.shared_targets[event.scanned_bot_id] = {
                'x': scanned_x,
                'y': scanned_y,
                'energy': event.energy,
                'distance': distance
            }
            
            # Prioritize closest or weakest target
            if self.primary_target is None:
                self.primary_target = event.scanned_bot_id
            else:
                current = self.shared_targets.get(self.primary_target)
                if current is None or event.energy < current['energy']:
                    self.primary_target = event.scanned_bot_id
    
    async def on_hit_by_bullet(self, event):
        """Evasive action when hit"""
        if self.role != "KILLER":
            # Hunters dodge aggressively
            self.turn_rate = 90
            self.target_speed = -80
        else:
            # Killer maintains position, just adjusts
            self.turn_rate = 30


# Create the three team members
class Hunter1(HunterKillerBot):
    """First hunter bot"""
    pass


class Hunter2(HunterKillerBot):
    """Second hunter bot"""
    pass


class Killer(HunterKillerBot):
    """Killer bot"""
    pass


# Entry points
if __name__ == "__main__":
    import sys
    
    bot_info = BotInfo.from_file("hunter_killer_team.json")
    
    if len(sys.argv) > 1:
        role = sys.argv[1].lower()
    else:
        role = "hunter1"
    
    if role == "killer":
        bot = Killer(bot_info=bot_info)
    elif role == "hunter1":
        bot = Hunter1(bot_info=bot_info)
    else:
        bot = Hunter2(bot_info=bot_info)
    
    asyncio.run(bot.start())
