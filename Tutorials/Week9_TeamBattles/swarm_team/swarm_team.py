"""
Swarm Team - Coordinated Pack Hunting Strategy

This team demonstrates coordinated pack behavior where bots work together
to surround and overwhelm enemies with focused fire.

Strategy:
- Leader: Main target acquisition and attack coordination
- Followers: Maintain formation around leader, provide flanking fire
- All bots: Share target priority, focus fire on weakest enemy

Roles:
- SwarmLeader: Coordinates attacks, tracks primary target
- SwarmFollower1: Flanks left, secondary damage
- SwarmFollower2: Flanks right, secondary damage
"""

import asyncio
import math
from robocode_tank_royale.bot_api import Bot, BotInfo
from robocode_tank_royale.bot_api.events import ScannedBotEvent


class SwarmBot(Bot):
    """Base class for swarm team members"""
    
    def __init__(self, bot_info: BotInfo):
        super().__init__(bot_info=bot_info)
        self.role = self.get_role()
        self.target_x = None
        self.target_y = None
        self.target_energy = None
        self.teammates = {}  # Track teammate positions
        self.formation_angle = 0  # Angle for formation positioning
        
    def get_role(self):
        """Determine role based on bot name"""
        name_lower = self.name.lower()
        if "leader" in name_lower:
            return "LEADER"
        elif "follower1" in name_lower or "swarm1" in name_lower:
            return "FOLLOWER1"
        elif "follower2" in name_lower or "swarm2" in name_lower:
            return "FOLLOWER2"
        return "FOLLOWER"
    
    async def run(self):
        """Main bot loop"""
        # Set colors based on role
        if self.role == "LEADER":
            self.body_color = "#FF0000"  # Red leader
            self.turret_color = "#FF4444"
            self.radar_color = "#FF8888"
        else:
            self.body_color = "#0000FF"  # Blue followers
            self.turret_color = "#4444FF"
            self.radar_color = "#8888FF"
        
        while self.is_running():
            # Spin radar to detect bots
            self.radar_turn_rate = 30
            
            if self.role == "LEADER":
                await self.leader_behavior()
            else:
                await self.follower_behavior()
            
            await self.go()
    
    async def leader_behavior(self):
        """Leader coordinates the attack"""
        if self.target_x is not None and self.target_y is not None:
            # Calculate angle to target
            angle_to_target = math.degrees(math.atan2(
                self.target_x - self.x,
                self.target_y - self.y
            ))
            
            # Turn toward target
            turn_amount = (angle_to_target - self.direction + 360) % 360
            if turn_amount > 180:
                turn_amount -= 360
            self.turn_rate = turn_amount * 0.3
            
            # Move toward target but maintain distance
            distance = math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
            if distance > 200:
                self.target_speed = 100
            elif distance < 100:
                self.target_speed = -50
            else:
                self.target_speed = 20
            
            # Aim turret at target
            turret_angle = (angle_to_target - self.gun_direction + 360) % 360
            if turret_angle > 180:
                turret_angle -= 360
            self.gun_turn_rate = turret_angle
            
            # Fire if aimed
            if abs(turret_angle) < 10 and self.gun_heat == 0:
                power = min(3, self.energy / 10)  # Scale power with energy
                self.fire = power
        else:
            # No target, patrol
            self.target_speed = 50
            if self.x < 100 or self.x > self.arena_width - 100:
                self.turn_rate = 90
            if self.y < 100 or self.y > self.arena_height - 100:
                self.turn_rate = 90
    
    async def follower_behavior(self):
        """Followers maintain formation and support leader"""
        if self.target_x is not None and self.target_y is not None:
            # Calculate formation position
            # Follower1 flanks at +120°, Follower2 at -120°
            if self.role == "FOLLOWER1":
                self.formation_angle = 120
            else:
                self.formation_angle = -120
            
            # Calculate desired position (flanking the target)
            angle_to_target = math.degrees(math.atan2(
                self.target_x - self.x,
                self.target_y - self.y
            ))
            
            # Flank position
            flank_angle = (angle_to_target + self.formation_angle) % 360
            turn_amount = (flank_angle - self.direction + 360) % 360
            if turn_amount > 180:
                turn_amount -= 360
            self.turn_rate = turn_amount * 0.3
            
            # Maintain optimal distance
            distance = math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
            if distance > 250:
                self.target_speed = 100
            elif distance < 150:
                self.target_speed = -30
            else:
                self.target_speed = 30
            
            # Aim and fire at target
            turret_angle = (angle_to_target - self.gun_direction + 360) % 360
            if turret_angle > 180:
                turret_angle -= 360
            self.gun_turn_rate = turret_angle
            
            if abs(turret_angle) < 15 and self.gun_heat == 0:
                power = min(2.5, self.energy / 10)
                self.fire = power
        else:
            # No target, stay mobile
            self.target_speed = 50
            self.turn_rate = 5
    
    async def on_scanned_bot(self, event: ScannedBotEvent):
        """Track enemies and teammates"""
        # Enemy position is directly from event
        scanned_x = event.x
        scanned_y = event.y
        
        if event.is_teammate:
            # Track teammate position
            self.teammates[event.scanned_bot_id] = {
                'x': scanned_x,
                'y': scanned_y,
                'energy': event.energy
            }
        else:
            # Track enemy (prioritize weakest or closest)
            if self.target_energy is None or event.energy < self.target_energy:
                self.target_x = scanned_x
                self.target_y = scanned_y
                self.target_energy = event.energy
    
    async def on_hit_by_bullet(self, event):
        """Evasive maneuver when hit"""
        self.turn_rate = 90
        self.target_speed = -100


# Create the three swarm team members
class SwarmLeader(SwarmBot):
    """Leader bot for swarm team"""
    pass


class SwarmFollower1(SwarmBot):
    """First follower bot"""
    pass


class SwarmFollower2(SwarmBot):
    """Second follower bot"""
    pass


# Entry points for each bot
if __name__ == "__main__":
    import sys
    
    bot_info = BotInfo.from_file("swarm_team.json")
    
    # Determine which bot to run based on command line or bot name
    if len(sys.argv) > 1:
        role = sys.argv[1].lower()
    else:
        role = "leader"
    
    if role == "leader":
        bot = SwarmLeader(bot_info=bot_info)
    elif role == "follower1":
        bot = SwarmFollower1(bot_info=bot_info)
    else:
        bot = SwarmFollower2(bot_info=bot_info)
    
    asyncio.run(bot.start())
