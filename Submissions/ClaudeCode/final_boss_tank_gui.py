"""
FinalBossTank - GUI Version
Adapted for Robocode Tank Royale visual battles

Run with:
    python Submissions/ClaudeCode/final_boss_tank_gui.py
"""
import asyncio
import os
from pathlib import Path
from robocode_tank_royale.bot_api import BaseBot, BotInfo


class FinalBossTankGUI(BaseBot):
    """
    GUI-compatible version of FinalBossTank

    This is a simplified demo version that works with the Tank Royale GUI.
    For full features, see final_boss_tank.py
    """

    async def run(self):
        """Main bot loop"""
        # Simple strategy: move forward and scan
        while True:
            # Move forward
            self.forward(100)

            # Turn radar to scan
            self.turn_radar_right(30)

            # Turn gun independently
            self.turn_gun_right(15)

            # Execute the turn
            await self.go()

    def on_scanned_bot(self, event):
        """Fire when we see an enemy"""
        # Aim at the scanned bot
        self.turn_gun_to(event.angle)

        # Fire!
        self.fire(2)

    def on_hit_by_bullet(self, event):
        """React when hit"""
        # Turn perpendicular to dodge
        self.turn_right(90)
        self.forward(100)

    def on_hit_wall(self, event):
        """React to wall collision"""
        # Back up and turn
        self.back(100)
        self.turn_right(90)


if __name__ == "__main__":
    # Load bot info from JSON file in same directory as this script
    script_dir = Path(__file__).parent
    json_file = script_dir / "final_boss_tank_gui.json"

    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))

    # Start the bot
    bot = FinalBossTankGUI(bot_info=bot_info)
    asyncio.run(bot.start())
