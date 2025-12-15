"""
PredictorBot - A tank that predicts enemy movement!

Week 2 Tutorial - Learning Trigonometry
This tank uses math to predict where enemies will be and shoots at their future position.
"""
import math
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class PredictorBot(BaseBot):
    """Uses trigonometry to predict enemy movement and aim ahead"""

    async def run(self):
        """Main loop - runs every game tick"""
        while True:
            # Spin radar to look for enemies
            self.turn_radar_right(45)

            # Move in a circle to dodge bullets
            self.forward(50)
            self.turn_right(15)
            
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

    def on_scanned_bot(self, event):
        """When we see an enemy - predict and shoot!"""
        # Bullet speed based on power (official formula)
        bullet_power = 2
        bullet_speed = 20 - 3 * bullet_power

        # Time for bullet to reach current position
        time_to_hit = event.distance / bullet_speed

        # Calculate enemy position from bearing
        bearing_rad = math.radians(event.bearing)
        enemy_x = self.x + event.distance * math.sin(bearing_rad)
        enemy_y = self.y + event.distance * math.cos(bearing_rad)

        # Predict where enemy will be
        future_x, future_y = self.predict_position(
            enemy_x,
            enemy_y,
            event.speed,
            event.direction,
            time_to_hit
        )

        # Calculate angle to future position
        angle = self.calculate_angle(self.x, self.y, future_x, future_y)

        # Aim and fire!
        self.turn_gun_to(angle)
        self.fire(bullet_power)

        print(f"Enemy spotted at distance {event.distance:.1f}")
        print(f"Predicted future position: ({future_x:.1f}, {future_y:.1f})")

    def on_hit_by_bullet(self, event):
        """React when hit - dodge!"""
        print("Ouch! Dodging!")
        # Turn perpendicular to the bullet to dodge better
        self.turn_right(90)
        self.forward(100)

    def on_hit_wall(self, event):
        """React when we hit a wall"""
        print("Hit a wall! Backing up...")
        # Back up and turn
        self.back(50)
        self.turn_right(90)


if __name__ == "__main__":
    bot = PredictorBot()
    bot.start()
