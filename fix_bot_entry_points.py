#!/usr/bin/env python3
"""
Fix all bot entry points to properly load BotInfo from JSON files
"""
import re
from pathlib import Path

# Standard entry point template
ENTRY_POINT_TEMPLATE = '''

if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    
    # Load bot info from JSON file in same directory
    script_dir = Path(__file__).parent
    json_file = script_dir / "{json_name}"
    
    bot_info = None
    if json_file.exists():
        bot_info = BotInfo.from_file(str(json_file))
    
    # Create and start the bot
    bot = {class_name}(bot_info=bot_info)
    asyncio.run(bot.start())
'''

def fix_bot_file(bot_path, class_name):
    """Fix a single bot file's entry point"""
    bot_path = Path(bot_path)
    json_name = bot_path.with_suffix('.json').name
    
    # Read the file
    content = bot_path.read_text()
    
    # Find and remove old if __name__ block
    # Match from "if __name__" to the end of file, handling various formats
    pattern = r'\n\s*if __name__ == ["\']__main__["\']:\s*\n.*'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Add new entry point
    new_entry = ENTRY_POINT_TEMPLATE.format(
        json_name=json_name,
        class_name=class_name
    )
    
    content = content.rstrip() + new_entry
    
    # Write back
    bot_path.write_text(content)
    print(f"✓ Fixed {bot_path}")

# List of bots to fix
bots = [
    ("Samples/sitting_duck.py", "SittingDuck"),
    ("Samples/spin_bot.py", "SpinBot"),
    ("Samples/walls_bot.py", "WallsBot"),
    ("Samples/tracker_bot.py", "TrackerBot"),
    ("Samples/champion_bot.py", "ChampionBot"),
    ("Tutorials/Week1_MyFirstTank/my_first_tank.py", "MyFirstTank"),
    ("Tutorials/Week2_Trigonometry/predictor_bot.py", "PredictorBot"),
    ("Tutorials/Week3_BoundaryChecking/boundary_bot.py", "BoundaryBot"),
    ("Tutorials/Week4_Strategy/trickster_bot.py", "TricksterBot"),
    ("Tutorials/Week5_AdvancedTargeting/sniper_bot.py", "SniperBot"),
    ("Tutorials/Week6_AdvancedPython/professional_tank.py", "ProfessionalTank"),
    ("Tutorials/Week7_AdvancedSkirmisher/skirmisher_tank.py", "SkirmisherTank"),
    ("Tutorials/Week8_AntiGravitySwarms/anti_gravity_tank.py", "AntiGravityTank"),
    ("Submissions/ExampleSubmission/example_tank.py", "ExampleTank"),
    ("Submissions/ClaudeCode/final_boss_tank.py", "FinalBossTank"),
    ("Submissions/ClaudeCode/challenger_tank.py", "ChallengerTank"),
]

print("Fixing bot entry points...")
for bot_file, class_name in bots:
    fix_bot_file(bot_file, class_name)

print(f"\n✅ Fixed {len(bots)} bot files!")
