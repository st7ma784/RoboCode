"""
Tank Utilities - Shared Helper Functions
=========================================

This module contains common helper functions used across multiple tank tutorials.
Instead of copying the same code into every tank, we can import these functions!

Think of this like a toolbox - you don't need to build a hammer for every project,
you just grab the hammer from your toolbox when you need it!
"""

import math


class TankMath:
    """Mathematical helper functions for tank combat"""
    
    @staticmethod
    def calculate_distance(from_x, from_y, to_x, to_y):
        """
        Calculate distance between two points using the Pythagorean theorem.
        
        Remember from geometry: distance = √((x₂-x₁)² + (y₂-y₁)²)
        
        Args:
            from_x, from_y: Starting point coordinates
            to_x, to_y: Ending point coordinates
            
        Returns:
            float: Distance in pixels
            
        Example:
            >>> TankMath.calculate_distance(0, 0, 3, 4)
            5.0  # The famous 3-4-5 triangle!
        """
        x_diff = to_x - from_x
        y_diff = to_y - from_y
        return math.sqrt(x_diff**2 + y_diff**2)
    
    @staticmethod
    def calculate_angle(from_x, from_y, to_x, to_y):
        """
        Calculate angle from one point to another.
        
        Uses atan2 (arctangent with two arguments) which handles all 4 quadrants correctly!
        
        Args:
            from_x, from_y: Starting point
            to_x, to_y: Target point
            
        Returns:
            float: Angle in degrees (0° = North, 90° = East, 180° = South, 270° = West)
            
        Example:
            >>> TankMath.calculate_angle(0, 0, 1, 0)  # Point directly east
            90.0
        """
        return math.degrees(math.atan2(to_x - from_x, to_y - from_y))
    
    @staticmethod
    def predict_position(x, y, velocity, heading, time):
        """
        Predict where a moving target will be in the future.
        
        This is linear prediction - assumes the target keeps moving in a straight line
        at constant speed. Works great for simple bots, less accurate against smart ones!
        
        Args:
            x, y: Current position
            velocity: Speed of movement (pixels per tick)
            heading: Direction of movement (degrees)
            time: How many ticks into the future to predict
            
        Returns:
            tuple: (future_x, future_y) coordinates
            
        Example:
            >>> TankMath.predict_position(100, 100, 5, 0, 10)
            (100.0, 150.0)  # Moved 50 pixels north (5 * 10 ticks)
        """
        heading_rad = math.radians(heading)
        future_x = x + velocity * time * math.sin(heading_rad)
        future_y = y + velocity * time * math.cos(heading_rad)
        return future_x, future_y
    
    @staticmethod
    def normalize_angle(angle):
        """
        Normalize an angle to be between -180 and 180 degrees.
        
        Sometimes angles can be 450° (same as 90°) or -270° (same as 90°).
        This function "wraps" them to the standard -180 to 180 range.
        
        Args:
            angle: Any angle in degrees
            
        Returns:
            float: Equivalent angle between -180 and 180
            
        Example:
            >>> TankMath.normalize_angle(450)
            90.0
            >>> TankMath.normalize_angle(-270)
            90.0
        """
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    @staticmethod
    def bullet_speed(power):
        """
        Calculate bullet speed based on fire power.
        
        RoboCode formula: bullet_speed = 20 - 3 * power
        Higher power = slower bullet but more damage!
        
        Args:
            power: Fire power (0.1 to 3.0)
            
        Returns:
            float: Bullet speed in pixels per tick
            
        Example:
            >>> TankMath.bullet_speed(1)
            17  # Fast bullet, low damage
            >>> TankMath.bullet_speed(3)
            11  # Slow bullet, high damage
        """
        return 20 - 3 * power


class TankTargeting:
    """Helper functions for aiming and targeting"""
    
    @staticmethod
    def aim_at_target(bot, target_x, target_y):
        """
        Calculate the angle the gun needs to turn to aim at a target.
        
        Args:
            bot: The bot instance (needs get_x(), get_y(), get_gun_direction() methods)
            target_x, target_y: Target coordinates
            
        Returns:
            float: Angle to turn the gun (degrees)
        """
        # Calculate absolute angle to target
        angle_to_target = TankMath.calculate_angle(
            bot.get_x(), bot.get_y(),
            target_x, target_y
        )
        
        # Calculate how much to turn from current gun direction
        current_gun_angle = bot.get_gun_direction()
        turn_angle = TankMath.normalize_angle(angle_to_target - current_gun_angle)
        
        return turn_angle
    
    @staticmethod
    def lead_shot(bot, enemy_x, enemy_y, enemy_velocity, enemy_heading, fire_power=2):
        """
        Calculate where to aim to hit a moving target (lead the shot).
        
        This does "predictive targeting" - aims at where the enemy WILL BE,
        not where they ARE now!
        
        Args:
            bot: The bot instance
            enemy_x, enemy_y: Current enemy position
            enemy_velocity: Enemy's speed
            enemy_heading: Enemy's direction
            fire_power: How hard we're shooting (affects bullet speed)
            
        Returns:
            tuple: (aim_angle, predicted_x, predicted_y)
        """
        # Calculate distance to enemy
        distance = TankMath.calculate_distance(
            bot.get_x(), bot.get_y(),
            enemy_x, enemy_y
        )
        
        # Calculate bullet travel time
        bullet_speed = TankMath.bullet_speed(fire_power)
        time_to_hit = distance / bullet_speed
        
        # Predict where enemy will be
        future_x, future_y = TankMath.predict_position(
            enemy_x, enemy_y,
            enemy_velocity, enemy_heading,
            time_to_hit
        )
        
        # Calculate aim angle
        aim_angle = TankTargeting.aim_at_target(bot, future_x, future_y)
        
        return aim_angle, future_x, future_y


class TankMovement:
    """Helper functions for smart movement"""
    
    @staticmethod
    def is_near_wall(bot, margin=50):
        """
        Check if the bot is too close to any wall.
        
        Args:
            bot: The bot instance
            margin: How many pixels from wall is "too close"
            
        Returns:
            bool: True if near any wall
        """
        x = bot.get_x()
        y = bot.get_y()
        arena_width = bot.get_arena_width()
        arena_height = bot.get_arena_height()
        
        too_close_left = x < margin
        too_close_right = x > (arena_width - margin)
        too_close_top = y < margin
        too_close_bottom = y > (arena_height - margin)
        
        return too_close_left or too_close_right or too_close_top or too_close_bottom
    
    @staticmethod
    def find_nearest_wall(bot):
        """
        Find which wall is closest to the bot.
        
        Args:
            bot: The bot instance
            
        Returns:
            str: "left", "right", "top", or "bottom"
        """
        x = bot.get_x()
        y = bot.get_y()
        arena_width = bot.get_arena_width()
        arena_height = bot.get_arena_height()
        
        distances = {
            "left": x,
            "right": arena_width - x,
            "top": y,
            "bottom": arena_height - y
        }
        
        return min(distances, key=distances.get)
    
    @staticmethod
    def is_valid_target(bot, target_x, target_y, margin=20):
        """
        Check if a target position is inside the arena boundaries.
        
        Useful for validating predicted positions before shooting!
        
        Args:
            bot: The bot instance
            target_x, target_y: Target coordinates to check
            margin: Safety margin from walls
            
        Returns:
            bool: True if target is valid
        """
        arena_width = bot.get_arena_width()
        arena_height = bot.get_arena_height()
        
        x_ok = margin < target_x < (arena_width - margin)
        y_ok = margin < target_y < (arena_height - margin)
        
        return x_ok and y_ok


# Convenience function for quick imports
def quick_aim(bot, event, fire_power=2):
    """
    One-line function to aim and return fire angle with prediction.
    
    Args:
        bot: Your bot instance
        event: Scanned event from on_scanned_bot
        fire_power: How hard to shoot
        
    Returns:
        float: Angle to turn gun
        
    Example in your bot:
        >>> from tank_utils import quick_aim
        >>> def on_scanned_bot(self, event):
        ...     turn_angle = quick_aim(self, event, fire_power=2)
        ...     self.turn_gun_right(turn_angle)
        ...     self.fire(2)
    """
    aim_angle, _, _ = TankTargeting.lead_shot(
        bot,
        event.x, event.y,
        event.speed, event.direction,
        fire_power
    )
    return aim_angle


if __name__ == "__main__":
    # Run some tests!
    print("🧪 Testing TankMath...")
    print(f"Distance (3,4,5 triangle): {TankMath.calculate_distance(0, 0, 3, 4)}")
    print(f"Angle to (1,0): {TankMath.calculate_angle(0, 0, 1, 0)}°")
    print(f"Bullet speed (power=2): {TankMath.bullet_speed(2)} px/tick")
    print(f"Normalize 450°: {TankMath.normalize_angle(450)}°")
    print("\n✅ Tank utilities loaded and ready to use!")
