# Python Tank Wars - Learn Coding Through Battle! 🎮

Welcome to Python Tank Wars! This is a fun tutorial series designed to teach 8-year-olds (and anyone else!) how to code by building battle tanks that fight each other.

## What is This?

You'll learn Python programming by creating your own robot tank that can:
- Move around an arena
- Shoot at other tanks
- Dodge bullets
- Use math to aim better
- Make smart decisions

## Getting Started

### What You'll Need
- Python 3.8 or newer
- A GitHub account (free!)
- Robocode Tank Royale GUI ([download here](https://github.com/robocode-dev/tank-royale/releases))
- Enthusiasm for robot battles!

### Quick Setup

1. **Fork this repository** on GitHub (click the Fork button above!)
2. **Download Robocode Tank Royale** from the releases page
3. **Clone YOUR fork** to your computer:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RoboCode.git
   cd RoboCode
   ```
4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Start the Robocode GUI** and launch your first battle!

### Testing Your Tanks

**In the Arena (Recommended):**
- Start the Robocode Tank Royale GUI
- Run your tank: `python Tutorials/Week1_MyFirstTank/my_first_tank.py`
- Add opponents in separate terminals
- Click "Start Battle" and watch the action! 🎮

**Automated Testing on GitHub:**
- Push your code to GitHub
- GitHub Actions automatically tests your tanks
- Check the "Actions" tab for battle results!
- No local setup needed - battles run in the cloud! ☁️

## Tutorial Structure

Follow these weekly tutorials in order:

### 📅 Week 1: GitHub Signup and My First Tank
**Location:** `Tutorials/Week1_MyFirstTank/`
- Create your GitHub account
- Learn what a tank program looks like
- Make your first tank move and shoot

### 📐 Week 2: Basic Trigonometry - Predicting Where Tanks Will Be
**Location:** `Tutorials/Week2_Trigonometry/`
- Learn about angles and directions
- Use math to predict where moving tanks will go
- Hit moving targets!

### ✅ Week 3: Checking Values - Stay Inside the Arena
**Location:** `Tutorials/Week3_BoundaryChecking/`
- Make sure your tank doesn't hit walls
- Check that you're aiming at valid targets
- Learn about if-statements and conditions

### 🎯 Week 4: Strategy - Unpredictable Movement
**Location:** `Tutorials/Week4_Strategy/`
- Make your tank move in tricky patterns
- React when someone shoots at you
- Learn to dodge!

### 🚀 Week 5: Advanced Targeting - Smart Shooting
**Location:** `Tutorials/Week5_AdvancedTargeting/`
- Choose how much power to use when shooting
- Predict if you'll hit before wasting a shot
- Become a tank master!

### 🏗️ Week 6: Advanced Python - Classes and Clean Code
**Location:** `Tutorials/Week6_AdvancedPython/`
- Learn to organize code like a professional
- Understand classes, inheritance, and polymorphism
- Create reusable components with the strategy pattern
- Build a modular tank architecture that's easy to modify and extend

### ⚔️ Week 7: Advanced Skirmisher - Battle Royale Mode
**Location:** `Tutorials/Week7_AdvancedSkirmisher/`
- Handle 30+ enemies at once efficiently
- Learn data structures (lists, dictionaries, arrays)
- Use NumPy for lightning-fast math on multiple targets
- Implement smart target selection and threat assessment
- Master vectorized operations and matrix math

### 🌊 Week 8: Anti-Gravity & Swarm Intelligence
**Location:** `Tutorials/Week8_AntiGravitySwarms/`
- Physics-based movement with repulsive forces
- Detect and escape from enemy swarms
- Analyze cluster formations and danger zones
- Advanced force-based navigation algorithms

### 🤝 Week 9: Team Battles - Coordinated Combat
**Location:** `Tutorials/Week9_TeamBattles/`
- Build tanks that work together in teams
- Share information between team members
- Coordinate attacks and defensive formations
- Implement team-based strategies and tactics

### 🧬 Week 10: Genetic Algorithms - Evolving the Perfect Tank
**Location:** `Tutorials/Week10_GeneticAlgorithm/`
- Learn evolutionary optimization techniques
- Evolve combat parameters automatically
- Implement mutation and crossover operations
- Let AI discover optimal tactics through generations
- Understand fitness functions and selection strategies

### 🤖 Week 11: Q-Learning - Real-Time AI Learning
**Location:** `Tutorials/Week11_QLearning/`
- Master reinforcement learning fundamentals
- Implement Q-Learning algorithm for combat
- Learn state discretization and action selection
- Build tanks that adapt during battle
- Explore exploration vs exploitation tradeoff

## 🛠️ Shared Code - tank_utils.py

Starting from Week 2, tutorials use `tank_utils.py` - a shared library of helper functions!

**Why?** Instead of copying math functions into every tank, we import them:

```python
from tank_utils import TankMath, TankTargeting

distance = TankMath.calculate_distance(x1, y1, x2, y2)
```

**Benefits:**
- ✅ Shorter, cleaner code
- ✅ Fix bugs once, all tanks benefit  
- ✅ Professional coding practices (DRY principle!)

See [TANK_UTILS_README.md](TANK_UTILS_README.md) for full documentation.

## Sample Tanks

Check out `Samples/` for example tanks:
- **SittingDuck** - Doesn't move (easy to beat!)
- **SpinBot** - Spins in circles
- **Walls** - Drives around the edges
- **Tracker** - Follows other tanks
- **Sniper** - Advanced targeting and movement

## Guides

The `Guides/` folder has detailed explanations:
- **Python Basics** - Variables, functions, classes
- **Trigonometry for Tanks** - Angles, distance, prediction
- **Strategy Guide** - Movement patterns and tactics
- **Genetic Algorithms** - Evolutionary optimization (Week 10)
- **Q-Learning** - Reinforcement learning (Week 11)

## Submitting Your Tank

Ready to compete? Submit your tank to the arena!

### How to Submit

1. **Create a GUI-compatible tank** in `Submissions/YourName/`:
   - File: `your_tank_gui.py` (must inherit from `BaseBot`)
   - Config: `your_tank_gui.json` (required for battles)

2. **Test locally** (optional but recommended):
   ```bash
   # Quick validation
   python battle_runner.py Submissions/YourName/your_tank_gui.py Samples/sitting_duck.py

   # Visual battle (requires Tank Royale server)
   python run_gui_battle.py Submissions/YourName/your_tank_gui.py
   ```

3. **Create a Pull Request** or **Push to main**

### Automated Battle System

When you submit, GitHub Actions automatically:

✅ **Discovers Your Tank** - Scans for GUI-compatible tanks
✅ **Launches Tank Royale Server** - Docker container with full battle arena
✅ **Runs Round-Robin Battles** - Your tank fights every other submission
✅ **Generates Results:**
   - `SCORESHEET.md` - Overall rankings and leaderboard
   - `Submissions/YourName/BATTLE_RECORD.md` - Your tank's win/loss record
   - JSON artifacts with detailed battle data
✅ **Comments on PRs** - See battle results right in your pull request

**Example Results:**
```markdown
# 🎮 Tank Battle Results

## 🏆 Rankings
| Rank | Tank | Author | Battles |
|------|------|--------|---------|
| 🥇 1 | FinalBossTank | ClaudeCode | 5 |
| 🥈 2 | YourTank | YourName | 5 |
```

**View Details:** Check the [Workflows README](.github/workflows/README.md) for technical details

### Battle Requirements

Your tank must:
- Inherit from `Bot` (for GUI battles)
- Have a matching `.json` config file
- Be named with `_gui.py` suffix (e.g., `my_tank_gui.py`)

**Example:**
```python
from robocode_tank_royale.bot_api import BaseBot, BotInfo

class MyTank(Bot):
    async def run(self):
        while True:
            self.forward(100)
            self.turn_radar_right(30)
            await self.go()
```

## Rules

1. Have fun!
2. Help others learn
3. Be creative with your strategies
4. No peeking at other students' code before you try yourself

## Resources

- [Robocode.py GitHub](https://github.com/scilicet64/robocode.py) - Simple Python version
- [Robocode Tank Royale](https://robocode-dev.github.io/tank-royale/) - Advanced version

---

Ready to build your first tank? Start with Week 1! 🎉
