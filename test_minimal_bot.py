#!/usr/bin/env python3
"""Minimal test bot to verify API"""

import asyncio
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class MinimalBot(BaseBot):
    """Simplest possible moving bot"""

    async def run(self):
        """Main loop - just move forward and spin"""
        print("MinimalBot starting!")
        
        turn_count = 0
        while self.is_running():
            turn_count += 1
            print(f"Turn {turn_count}: Setting target_speed=50, turn_rate=10, radar_turn_rate=45")
            
            # Set movement
            self.target_speed = 50
            self.turn_rate = 10
            self.radar_turn_rate = 45
            
            # Execute
            await self.go()
            print(f"Turn {turn_count}: After go() - pos=({self.get_x():.1f}, {self.get_y():.1f}), speed={self.speed:.1f}, direction={self.get_direction():.1f}")

    async def on_scanned_bot(self, event):
        """Shoot when we see someone"""
        print(f"Scanned bot at distance {event.distance:.0f}!")
        await self.fire(1)

if __name__ == "__main__":
    bot_info = BotInfo(
        name="MinimalBot",
        version="1.0",
        authors=["Test"],
        description="Minimal test bot",
        homepage="",
        country_codes=["US"],
        game_types={"classic", "melee", "1v1"},
        platform="Python",
        programming_lang="Python",
    )
    
    bot = MinimalBot(bot_info=bot_info)
    asyncio.run(bot.start())
