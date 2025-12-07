# Setup Guide for Python Tank Wars 🚀

Complete setup instructions for teachers, students, and contributors.

## Table of Contents
1. [Quick Start (Students)](#quick-start-students)
2. [Full Setup (Teachers)](#full-setup-teachers)
3. [Running Battles](#running-battles)
4. [Troubleshooting](#troubleshooting)

---

## Quick Start (Students)

### Step 1: Install Python

**Windows:**
1. Go to [python.org](https://python.org)
2. Download Python 3.11 or newer
3. Run installer
4. ✅ Check "Add Python to PATH"
5. Click "Install Now"

**Mac:**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

### Step 2: Install Dependencies

```bash
cd RoboCode
pip install -r requirements.txt
```

**Note:** This will install:
- `robocode-tank-royale` - The game framework
- Other helpful libraries for battles and visualizations

### Step 3: Test Your Setup

```bash
# Check Python version
python --version
# Should show 3.11 or higher

# Run Tank Doctor on a sample
python tank_doctor.py Samples/sitting_duck.py
```

### Step 4: Start Learning!

```bash
cd Tutorials/Week1_MyFirstTank
# Read the README.md and start coding!
```

---

## Full Setup (Teachers)

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/RoboCode.git
cd RoboCode

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Robocode Tank Royale Server (Optional for Real Battles)

For running actual battles (not just validation), you need the Tank Royale server:

#### Option A: Download Pre-built Server
1. Go to [Robocode Tank Royale Releases](https://github.com/robocode-dev/tank-royale/releases)
2. Download the latest release
3. Extract and run the server

#### Option B: Build from Source
```bash
# Clone Tank Royale
git clone https://github.com/robocode-dev/tank-royale.git
cd tank-royale

# Build (requires Java 11+)
./gradlew build

# Run server
./gradlew run
```

### 3. Configure GitHub Actions

The repository includes automated battle testing via GitHub Actions.

**Setup Steps:**
1. Enable Actions in your GitHub repository settings
2. Actions will run automatically on PRs to `Submissions/`
3. Results post as comments on PRs

**Secrets needed:** None! Everything runs automatically.

---

## Running Battles

### Method 1: Validation Mode (No Server Required)

This validates your tank's code without running actual battles:

```bash
# Test a single tank
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/sitting_duck.py

# Test against all samples
python battle_runner.py your_tank.py --all-samples
```

**What it does:**
- ✅ Loads your tank code
- ✅ Checks for syntax errors
- ✅ Validates required methods
- ✅ Provides kid-friendly error messages
- ❌ Doesn't run actual battles (needs server)

### Method 2: Full Battles (With Tank Royale Server)

Coming soon! This will require:
1. Tank Royale server running
2. Bot configuration files (.json)
3. WebSocket connection setup

---

## Using Tank Doctor

Tank Doctor helps debug your code with kid-friendly messages:

```bash
python tank_doctor.py your_tank.py
```

**What it checks:**
- File basics (not empty, reasonable size)
- Python syntax errors
- Class structure
- Required methods (run, etc.)
- Recommended methods (on_scanned_bot, etc.)
- Common mistakes (missing `self.`, typos)
- Indentation consistency
- Missing imports

**Example Output:**
```
╔══════════════════════════════════════════════════════╗
║           🏥 TANK DOCTOR IS CHECKING...              ║
╚══════════════════════════════════════════════════════╝

📋 Patient: my_tank.py

🔍 Checking file basics...
   File has 45 lines
   ✓ File basics OK

🔍 Checking Python syntax...
   ✓ No syntax errors found!

🔍 Checking tank class...
   ✓ Class structure looks good!

...

╔══════════════════════════════════════════════════════╗
║              ✅ TANK IS HEALTHY!                    ║
╚══════════════════════════════════════════════════════╝
```

---

## Submitting Your Tank

### Step 1: Create Your Folder

```bash
mkdir -p Submissions/YourName
cd Submissions/YourName
```

### Step 2: Add Your Tank

```python
# your_awesome_tank.py
class YourAwesomeTank:
    def __init__(self):
        self.name = "YourAwesomeTank"

    def run(self):
        self.ahead(50)
        self.turn_right(15)

    def on_scanned_bot(self, enemy):
        self.fire(2)
```

### Step 3: Test Locally

```bash
# Run Tank Doctor
python ../../tank_doctor.py your_awesome_tank.py

# Validate against samples
python ../../battle_runner.py your_awesome_tank.py ../../Samples/sitting_duck.py
```

### Step 4: Create Pull Request

```bash
# Add your tank
git add Submissions/YourName/

# Commit
git commit -m "Add YourName's awesome tank"

# Push to your fork
git push origin main

# Create PR on GitHub
```

### Step 5: Wait for Results!

GitHub Actions will automatically:
- ✅ Run Tank Doctor
- ✅ Validate your code
- ✅ Simulate battles
- ✅ Update leaderboard
- ✅ Post results as comment
- ✅ Award badges! 🏆

---

## Leaderboard System

### How Scoring Works

**Battle Score Formula:**
```
Win: +100 points
Survival: +50 points
Damage Dealt: +1 per 10 damage
Damage Taken: -1 per 10 damage
Accuracy Bonus: +0 to +25 (based on hit %)

Total Score = Sum of all battles
```

### Badges

Earn badges by achieving milestones:

- 🔰 **Rookie**: First battle
- ⚔️ **Warrior**: 10+ battles
- 🎯 **Sharpshooter**: 60%+ accuracy (min 5 battles)
- 🛡️ **Survivor**: 75%+ survival rate (min 5 battles)
- 👑 **Champion**: #1 on leaderboard
- 🏆 **Undefeated**: 5+ wins, 0 losses

### Viewing the Leaderboard

```bash
# Generate current leaderboard
python leaderboard_manager.py
```

Or view `LEADERBOARD.md` in the repository.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'robocode_tank_royale'"

**Solution:**
```bash
pip install robocode-tank-royale
```

### "IndentationError" when running my tank

**Solution:**
- Use consistent indentation (all tabs OR all spaces, not mixed)
- Recommended: 4 spaces per indent level
- Run `python tank_doctor.py your_tank.py` for hints

### Tank Doctor shows errors I don't understand

**Solution:**
- Read the error explanation carefully
- Look at the examples provided
- Check the `Guides/python_basics.md` for help
- Ask a teacher or create a GitHub issue

### "File not found" error

**Solution:**
- Use absolute paths or run from the RoboCode directory
- Example: `python battle_runner.py Submissions/MyName/my_tank.py`

### Tank validation passes but battles don't run

**Explanation:**
- `battle_runner.py` in validation mode only checks your code
- For real battles, you need Tank Royale server running
- This is normal! Validation is enough to learn

### GitHub Actions failing

**Solutions:**
1. Check Tank Doctor results in the PR comments
2. Fix any syntax errors
3. Make sure your file is in `Submissions/YourName/`
4. Ensure it ends with `.py`

---

## Advanced Configuration

### Increasing Timeout for Slow Computers

Edit `.github/workflows/tank_battle_leaderboard.yml`:

```yaml
jobs:
  validate-and-battle:
    timeout-minutes: 60  # Increase from 30 to 60
```

### Custom Battle Runner Settings

Edit `battle_runner.py` to customize:
- Error message detail level
- Color output
- Validation strictness

---

## Getting Help

### For Students:
1. **Read error messages carefully** - they're designed to help!
2. **Run Tank Doctor** - `python tank_doctor.py your_tank.py`
3. **Check the Guides** - Especially `python_basics.md`
4. **Ask your teacher** - They're there to help!

### For Teachers:
1. **GitHub Issues** - Report bugs or request features
2. **GitHub Discussions** - Share teaching experiences
3. **Pull Requests** - Contribute improvements!

### For Developers:
1. See `CONTRIBUTING.md` for contribution guidelines
2. Check existing issues before creating new ones
3. Join community discussions

---

## Next Steps

- ✅ Setup complete? Start with `Tutorials/Week1_MyFirstTank/`
- ✅ Completed Week 1? Test against `Samples/sitting_duck.py`
- ✅ Ready to submit? Follow the submission guide above
- ✅ Want to help? See `CONTRIBUTING.md`

---

Happy coding! May your tank dominate the arena! 🏆🤖
