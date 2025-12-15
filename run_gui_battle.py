#!/usr/bin/env python3
"""
GUI Battle Launcher for Robocode Tank Royale

This script helps you launch tanks in the visual GUI.
It connects your Python bots to the Robocode Tank Royale server.

Usage:
    python run_gui_battle.py your_tank.py
    python run_gui_battle.py Submissions/ClaudeCode/final_boss_tank.py
    python run_gui_battle.py Tutorials/Week1_MyFirstTank/my_first_tank.py

Then:
    1. Open browser to http://localhost:8080
    2. Click "Start Battle"
    3. Watch your tank fight!
"""

import sys
import os
import importlib.util
from pathlib import Path

def print_header(text):
    """Print colorful header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def load_bot_from_file(tank_path):
    """Load a tank class from a Python file"""
    tank_path = Path(tank_path)

    if not tank_path.exists():
        print(f"❌ Error: Tank file not found: {tank_path}")
        sys.exit(1)

    # Load the module
    spec = importlib.util.spec_from_file_location("tank_module", tank_path)
    if spec is None or spec.loader is None:
        print(f"❌ Error: Could not load {tank_path.name}")
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    sys.modules["tank_module"] = module
    spec.loader.exec_module(module)

    # Find the tank class (skip private classes starting with _)
    tank_class = None
    for item_name in dir(module):
        item = getattr(module, item_name)
        if isinstance(item, type) and not item_name.startswith('_'):
            tank_class = item
            break

    if tank_class is None:
        print(f"❌ Error: No tank class found in {tank_path.name}")
        sys.exit(1)

    return tank_class

def main():
    print_header("🎮 Robocode Tank Royale - GUI Battle Launcher")

    if len(sys.argv) < 2:
        print("❌ Error: Please provide a tank file to run")
        print("\nUsage:")
        print("  python run_gui_battle.py your_tank.py")
        print("\nExamples:")
        print("  python run_gui_battle.py Submissions/ClaudeCode/final_boss_tank.py")
        print("  python run_gui_battle.py Tutorials/Week1_MyFirstTank/my_first_tank.py")
        print("  python run_gui_battle.py Samples/champion_bot.py")
        sys.exit(1)

    tank_path = sys.argv[1]

    print(f"📋 Loading tank from: {tank_path}")

    try:
        # Try to import robocode
        from robocode_tank_royale.bot_api import BaseBot

        # Load the tank class
        tank_class = load_bot_from_file(tank_path)

        print(f"✅ Loaded tank: {tank_class.__name__}")
        print("\n" + "=" * 60)
        print("  🚀 STARTING TANK - Connect to GUI")
        print("=" * 60)
        print("\n📺 Open your browser to: http://localhost:8080")
        print("🎮 Click 'Start Battle' to begin!")
        print("⚠️  Make sure the Tank Royale server is running!")
        print("\nPress Ctrl+C to stop the bot")
        print("=" * 60 + "\n")

        # Create and start the bot (connects to server)
        bot = tank_class()
        bot.start()

    except ImportError:
        print("\n❌ Error: robocode-tank-royale not installed!")
        print("\nTo install:")
        print("  pip install robocode-tank-royale")
        print("\nOr install all requirements:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. Tank Royale server is running")
        print("  2. Your tank code has no errors")
        print("  3. You're connected to localhost:7654 (server port)")
        sys.exit(1)

if __name__ == "__main__":
    main()
