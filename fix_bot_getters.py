#!/usr/bin/env python3
"""
Fix all bots to use getter methods instead of direct property access
"""
import re
import sys
from pathlib import Path

# Mapping of properties to getter methods
REPLACEMENTS = [
    (r'\bself\.x\b', 'self.get_x()'),
    (r'\bself\.y\b', 'self.get_y()'),
    (r'\bself\.energy\b', 'self.get_energy()'),
    (r'\bself\.direction\b', 'self.get_direction()'),
    (r'\bself\.gun_direction\b', 'self.get_gun_direction()'),
    (r'\bself\.radar_direction\b', 'self.get_radar_direction()'),
    (r'\bself\.arena_width\b', 'self.get_arena_width()'),
    (r'\bself\.arena_height\b', 'self.get_arena_height()'),
]

def fix_file(filepath):
    """Fix a single file"""
    print(f"Fixing: {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Apply all replacements
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✓ Updated")
        return True
    else:
        print(f"  - No changes needed")
        return False

def main():
    root = Path('/home/user/Documents/RoboCode')
    
    # Find all bot/tank Python files
    patterns = ['**/*_bot.py', '**/*_tank.py']
    files = []
    for pattern in patterns:
        files.extend(root.glob(pattern))
    
    # Exclude the tracker_bot (already fixed) and this script
    files = [f for f in files if f.name not in ['fix_bot_getters.py', 'tracker_bot.py']]
    
    print(f"Found {len(files)} files to fix\n")
    
    fixed_count = 0
    for filepath in sorted(files):
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} of {len(files)} files")

if __name__ == '__main__':
    main()
