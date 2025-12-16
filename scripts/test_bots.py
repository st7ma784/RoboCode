#!/usr/bin/env python3
"""
Test script to verify all converted bots have correct syntax and can be imported.
This is useful for CI/CD testing before running actual battles.
"""

import sys
import importlib.util
from pathlib import Path

def test_bot(bot_path):
    """Test if a bot file can be imported successfully"""
    bot_path = Path(bot_path)
    
    if not bot_path.exists():
        return False, f"File not found: {bot_path}"
    
    try:
        # Try to import the module
        spec = importlib.util.spec_from_file_location("test_bot", bot_path)
        if spec is None or spec.loader is None:
            return False, "Could not load module spec"
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check if it has a BaseBot subclass
        from robocode_tank_royale.bot_api import BaseBot
        
        bot_class = None
        for item_name in dir(module):
            if item_name.startswith('_'):
                continue
            item = getattr(module, item_name)
            if isinstance(item, type) and issubclass(item, BaseBot) and item != BaseBot:
                bot_class = item
                break
        
        if bot_class is None:
            return False, "No BaseBot subclass found"
        
        return True, f"Found bot class: {bot_class.__name__}"
    
    except Exception as e:
        return False, str(e)

def main():
    """Test all bots in the repository"""
    print("=" * 70)
    print("  🤖 Testing All Converted Bots")
    print("=" * 70)
    print()
    
    # List of all bot files to test
    bot_files = [
        # Samples
        "Samples/sitting_duck.py",
        "Samples/spin_bot.py",
        "Samples/walls_bot.py",
        "Samples/tracker_bot.py",
        "Samples/champion_bot.py",
        
        # Tutorials
        "Tutorials/Week1_MyFirstTank/my_first_tank.py",
        "Tutorials/Week2_Trigonometry/predictor_bot.py",
        "Tutorials/Week3_BoundaryChecking/boundary_bot.py",
        "Tutorials/Week4_Strategy/trickster_bot.py",
        "Tutorials/Week5_AdvancedTargeting/sniper_bot.py",
        "Tutorials/Week6_AdvancedPython/professional_tank.py",
        "Tutorials/Week7_AdvancedSkirmisher/skirmisher_tank.py",
        "Tutorials/Week8_AntiGravitySwarms/anti_gravity_tank.py",
        
        # Submissions
        "Submissions/ClaudeCode/final_boss_tank.py",
        "Submissions/ClaudeCode/challenger_tank.py",
        "Submissions/ExampleSubmission/example_tank.py",
    ]
    
    passed = 0
    failed = 0
    results = []
    
    for bot_file in bot_files:
        success, message = test_bot(bot_file)
        status = "✅" if success else "❌"
        
        bot_name = Path(bot_file).stem
        print(f"{status} {bot_name:30s} - {message}")
        
        if success:
            passed += 1
        else:
            failed += 1
        
        results.append((bot_file, success, message))
    
    print()
    print("=" * 70)
    print(f"  Results: {passed} passed, {failed} failed out of {len(bot_files)} bots")
    print("=" * 70)
    
    if failed > 0:
        print("\n❌ Some bots failed. Details:")
        for bot_file, success, message in results:
            if not success:
                print(f"  - {bot_file}: {message}")
        sys.exit(1)
    else:
        print("\n✅ All bots passed! Ready for battle!")
        sys.exit(0)

if __name__ == "__main__":
    main()
