#!/usr/bin/env python3
"""
Fix all bot __init__ methods to accept bot_info parameter
"""
import re
from pathlib import Path

def fix_bot_init(bot_path):
    """Fix a bot's __init__ to accept bot_info"""
    content = bot_path.read_text()
    
    # Pattern 1: __init__ with just self
    pattern1 = r'def __init__\(self\):\s+super\(\).__init__\(\)'
    replacement1 = 'def __init__(self, bot_info=None):\n        super().__init__(bot_info=bot_info)'
    
    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        bot_path.write_text(content)
        return True
    
    # Pattern 2: Already has bot_info (skip)
    if 'def __init__(self, bot_info' in content:
        return False
    
    return False

# List of bot files
bot_files = [
    "Samples/sitting_duck.py",
    "Samples/spin_bot.py",
    "Samples/walls_bot.py",
    "Samples/tracker_bot.py",
    "Samples/champion_bot.py",
    "Tutorials/Week1_MyFirstTank/my_first_tank.py",
    "Tutorials/Week2_Trigonometry/predictor_bot.py",
    "Tutorials/Week3_BoundaryChecking/boundary_bot.py",
    "Tutorials/Week4_Strategy/trickster_bot.py",
    "Tutorials/Week5_AdvancedTargeting/sniper_bot.py",
    "Tutorials/Week6_AdvancedPython/professional_tank.py",
    "Tutorials/Week7_AdvancedSkirmisher/skirmisher_tank.py",
    "Tutorials/Week8_AntiGravitySwarms/anti_gravity_tank.py",
    "Submissions/ExampleSubmission/example_tank.py",
    "Submissions/ClaudeCode/final_boss_tank.py",
    "Submissions/ClaudeCode/challenger_tank.py",
]

print("Fixing bot __init__ methods...")
fixed = 0
skipped = 0

for bot_file in bot_files:
    bot_path = Path(bot_file)
    if bot_path.exists():
        if fix_bot_init(bot_path):
            print(f"✓ Fixed {bot_file}")
            fixed += 1
        else:
            print(f"- Skipped {bot_file} (already correct or no match)")
            skipped += 1

print(f"\n✅ Fixed {fixed} files, skipped {skipped}")
