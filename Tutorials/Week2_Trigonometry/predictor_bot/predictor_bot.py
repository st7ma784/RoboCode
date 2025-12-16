"""
PredictorBot - A tank that predicts enemy movement!

Week 2 Tutorial - Learning Trigonometry
This tank uses math to predict where enemies will be and shoots at their future position.
"""
import math
from robocode_tank_royale.bot_api import Bot, BotInfo

class PredictorBot(Bot):
    """Uses trigonometry to predict enemy movement and aim ahead"""

    def calc_gun_turn(self, target_angle):
        """Calculate gun turn needed to face target angle"""
        diff = target_angle - self.get_gun_direction()
        # Normalize to -180 to 180
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        return diff

    async def run(self):
        """Main loop - runs every game tick"""
        while self.is_running():
            # Spin radar to look for enemies
            self.radar_turn_rate = 45

            # Move in a circle to dodge bullets
            self.target_speed = 50
            self.turn_rate = 15
            
            await self.go()

    def calculate_angle(self, from_x, from_y, to_x, to_y):
        """
        Calculate angle from one point to another

        Returns: angle in degrees
        """
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))

    def calculate_distance(self, from_x, from_y, to_x, to_y):
        """
        Calculate distance between two points using Pythagorean theorem

        Returns: distance in pixels
        """
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)

    def predict_position(self, x, y, velocity, heading, time):
        """
        Predict future position of a moving tank

        x, y: current position
        velocity: speed of movement
        heading: direction of movement (degrees)
        time: how many game ticks in the future

        Returns: (future_x, future_y)
        """
        # Convert heading to radians for math functions
        heading_rad = math.radians(heading)

        # Calculate future position
        # sin for X movement, cos for Y movement
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)

        return future_x, future_y

    async def on_scanned_bot(self, event):
        """When we see an enemy - predict and shoot!"""
        # Bullet speed based on power (official formula)
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power

        # Enemy position is directly from event
        enemy_x = event.x
        enemy_y = event.y
        
        # Calculate distance from coordinates
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)
        
        # Time for bullet to reach current position
        time_to_hit = distance / bullet_speed

        # Predict where enemy will be
        future_x, future_y = self.predict_position(
            enemy_x,
            enemy_y,
            event.speed,
            event.direction,
            time_to_hit
        )

        # Calculate angle to future position
        angle = self.calculate_angle(self.get_x(), self.get_y(), future_x, future_y)

        # Aim and fire!
        self.gun_turn_rate = self.calc_gun_turn(angle)
        await self.fire(bullet_power)

        print(f"Enemy spotted at distance {distance:.1f}")
        print(f"Predicted future position: ({future_x:.1f}, {future_y:.1f})")

    async def on_hit_by_bullet(self, event):
        """React when hit - dodge!"""
        print("Ouch! Dodging!")
        # Turn perpendicular to the bullet to dodge better
        self.turn_rate = 90
        self.target_speed = 100

    async def on_hit_wall(self, event):
        """React when we hit a wall"""
        print("Hit a wall! Backing up...")
        # Back up and turn
        self.target_speed = -(50)
        self.turn_rate = 90

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "predictor_bot.json"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = PredictorBot(bot_info=bot_info)
    asyncio.run(bot.start())
