# How to Use Python Tank Wars 🎮

Quick reference guide for students, teachers, and contributors.

## For Students: Creating Your First Tank

### 1. Check if your tank has errors
```bash
python tank_doctor.py your_tank.py
```

**Tank Doctor will tell you:**
- ✅ What's working correctly
- ⚠️ Warnings (things you should fix)
- ❌ Critical errors (things you must fix)
- 💡 Suggestions for improvement

**Example:**
```bash
$ python tank_doctor.py my_awesome_tank.py

╔══════════════════════════════════════════════════════╗
║           🏥 TANK DOCTOR IS CHECKING...              ║
╚══════════════════════════════════════════════════════╝

📋 Patient: my_awesome_tank.py

🔍 Checking file basics...
   File has 42 lines
   ✓ File basics OK

🔍 Checking Python syntax...
   ✓ No syntax errors found!

✅ TANK IS HEALTHY!
```

### 2. Test your tank against opponents
```bash
# Fight one opponent
python battle_runner.py your_tank.py Samples/sitting_duck.py

# Fight all sample tanks
python battle_runner.py your_tank.py --all-samples
```

**Battle Runner shows:**
- Loading status (checks for errors)
- Validation results
- Battle simulation status
- Kid-friendly error messages if something's wrong

### 3. Fix any errors
If you see errors, Tank Doctor explains them in simple terms:

```
🔧 Missing Attribute

What happened:
You're trying to use something that doesn't exist on your object.

How to fix it:
Check that you're using the right method names.
Remember to use "self." before tank methods!

Example:
Good:
    self.ahead(50)
    self.fire(2)

Bad:
    ahead(50)  ← Missing "self."
```

### 4. Submit your tank
When your tank is ready:

```bash
# 1. Create your submission folder
mkdir -p Submissions/YourName

# 2. Copy your tank there
cp your_tank.py Submissions/YourName/

# 3. Commit and push
git add Submissions/YourName/
git commit -m "Add YourName's tank"
git push

# 4. Create a Pull Request on GitHub
```

### 5. Get your results!
GitHub Actions will automatically:
- ✅ Run Tank Doctor on your code
- ✅ Validate it against samples
- ✅ Update the leaderboard
- ✅ Award badges
- ✅ Post results as a comment on your PR!

---

## For Teachers: Running Class Battles

### Quick Class Setup

```bash
# 1. Clone the repository
git clone https://github.com/YourUsername/RoboCode.git
cd RoboCode

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test the setup
python tank_doctor.py Samples/sitting_duck.py
python battle_runner.py Samples/spin_bot.py Samples/sitting_duck.py
```

### Checking Student Code

```bash
# Validate a student's tank
python tank_doctor.py Submissions/StudentName/their_tank.py

# Test their tank
python battle_runner.py Submissions/StudentName/their_tank.py --all-samples
```

### Running Class Tournaments

```bash
# Battle all student tanks against each other
# (Create a script for this based on battle_runner.py)

for tank1 in Submissions/*/*.py; do
    for tank2 in Submissions/*/*.py; do
        if [ "$tank1" != "$tank2" ]; then
            python battle_runner.py "$tank1" "$tank2"
        fi
    done
done
```

### Viewing the Leaderboard

```bash
# Generate current standings
python leaderboard_manager.py

# Or view LEADERBOARD.md
cat LEADERBOARD.md
```

### Generating Badges for Students

```python
from leaderboard_manager import LeaderboardManager

manager = LeaderboardManager()

# Get badges for a student
badges = manager.generate_badge_url('StudentTank', 'StudentName')

# Display badge URLs
for badge_type, url in badges.items():
    print(f"{badge_type}: {url}")
```

---

## Common Workflows

### Workflow 1: Student Submitting First Tank

```bash
# Step 1: Create tank using tutorials
cd Tutorials/Week1_MyFirstTank
# ... edit my_first_tank.py ...

# Step 2: Check for errors
cd ../..
python tank_doctor.py Tutorials/Week1_MyFirstTank/my_first_tank.py

# Step 3: Test locally
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/sitting_duck.py

# Step 4: Copy to submissions
mkdir -p Submissions/MyName
cp Tutorials/Week1_MyFirstTank/my_first_tank.py Submissions/MyName/

# Step 5: Submit
git add Submissions/MyName/
git commit -m "Add my first tank!"
git push origin main

# Step 6: Create PR and wait for results!
```

### Workflow 2: Improving Your Tank

```bash
# Step 1: Edit your tank
# ... make improvements ...

# Step 2: Quick validation
python tank_doctor.py Submissions/MyName/my_tank.py

# Step 3: Test against tougher opponents
python battle_runner.py Submissions/MyName/my_tank.py Samples/champion_bot.py

# Step 4: If it works, submit!
git add Submissions/MyName/
git commit -m "Improved movement and targeting"
git push
```

### Workflow 3: Teacher Reviewing Submissions

```bash
# Check all pending PRs
# (Use GitHub interface)

# For each PR, GitHub Actions automatically:
# - Runs Tank Doctor
# - Validates code
# - Simulates battles
# - Updates leaderboard
# - Posts results

# Teacher can review the automated comments and:
# - Request changes if needed
# - Merge if everything looks good
# - Leaderboard auto-updates on merge!
```

---

## Understanding Error Messages

### Example 1: IndentationError

**Your code:**
```python
def run(self):
self.ahead(50)  # Not indented!
```

**Tank Doctor says:**
```
🔧 Indentation Problem

What happened:
Python is picky about spaces! Each line inside a function needs
to be indented by pressing Tab or 4 spaces.

How to fix it:
Check your code - lines inside "def" should be indented.
```

**Fixed code:**
```python
def run(self):
    self.ahead(50)  # Indented!
```

### Example 2: NameError

**Your code:**
```python
def run(self):
    ahead(50)  # Missing 'self.'
```

**Tank Doctor says:**
```
🔧 Unknown Name

What happened:
Python doesn't know what "ahead" means. You probably meant "self.ahead"!

How to fix it:
You need "self.ahead()" not just "ahead()"
```

**Fixed code:**
```python
def run(self):
    self.ahead(50)  # With 'self.'
```

---

## Tools Reference

### Tank Doctor (`tank_doctor.py`)
**Purpose**: Find and explain errors in tank code

**Usage:**
```bash
python tank_doctor.py <tank_file.py>
```

**What it checks:**
- File basics (not empty, reasonable size)
- Python syntax errors
- Class structure (has a class, has __init__)
- Required methods (run, etc.)
- Recommended methods (on_scanned_bot, etc.)
- Common mistakes (missing self., typos)
- Indentation consistency
- Missing imports (math, random)

### Battle Runner (`battle_runner.py`)
**Purpose**: Validate and test tanks

**Usage:**
```bash
# Test one tank vs another
python battle_runner.py tank1.py tank2.py

# Test against all samples
python battle_runner.py your_tank.py --all-samples
```

**What it does:**
- Loads tank code safely
- Checks for errors with kid-friendly messages
- Validates tank structure
- Simulates battle (validation mode)
- Extended timeout (30 minutes for slow code)

**Note:** For real battles, you need Tank Royale server running.

### Leaderboard Manager (`leaderboard_manager.py`)
**Purpose**: Manage rankings and badges

**Usage:**
```python
from leaderboard_manager import LeaderboardManager

manager = LeaderboardManager()

# Add battle result
manager.add_or_update_tank({
    'name': 'MyTank',
    'author': 'Student',
    'battle_results': {
        'won': True,
        'damage_dealt': 250,
        # ... more stats
    }
})

# Generate leaderboard
print(manager.generate_leaderboard_markdown())

# Get badges
badges = manager.generate_badge_url('MyTank', 'Student')
```

---

## Tips and Tricks

### For Students

**Tip 1: Always run Tank Doctor first**
```bash
python tank_doctor.py my_tank.py
```
Fix all errors before testing battles!

**Tip 2: Start simple, then improve**
1. Get a basic tank working
2. Test it
3. Add one feature at a time
4. Test again

**Tip 3: Use print() to debug**
```python
def run(self):
    print(f"My energy: {self.energy}")
    print(f"My position: ({self.x}, {self.y})")
    self.ahead(50)
```

### For Teachers

**Tip 1: Use Tank Doctor in class**
Project Tank Doctor output on screen while helping students debug.

**Tip 2: Create custom challenges**
Add sample tanks with specific difficulty levels for different lessons.

**Tip 3: Celebrate achievements**
When students earn badges, highlight them in class!

---

## Troubleshooting

### "I can't run battle_runner.py"
**Check:**
1. Are you in the RoboCode directory?
2. Did you run `pip install -r requirements.txt`?
3. Is Python installed? (`python --version`)

### "Tank Doctor says my code is wrong but I don't see the problem"
**Try:**
1. Read the error explanation carefully
2. Look at the example code provided
3. Check Guides/python_basics.md
4. Ask your teacher
5. Create a GitHub issue

### "My PR didn't get automated results"
**Check:**
1. Is your tank in `Submissions/YourName/`?
2. Does the filename end with `.py`?
3. Check the Actions tab on GitHub for errors
4. Look at the PR comments for clues

---

## Quick Command Reference

```bash
# Check for errors
python tank_doctor.py <tank.py>

# Test against one opponent
python battle_runner.py <your_tank.py> <opponent.py>

# Test against all samples
python battle_runner.py <your_tank.py> --all-samples

# View leaderboard
cat LEADERBOARD.md

# Generate new leaderboard
python leaderboard_manager.py

# Install/update dependencies
pip install -r requirements.txt

# Check Python version
python --version
```

---

## Next Steps

- **New students**: Start with `Tutorials/Week1_MyFirstTank/README.md`
- **Ready to submit**: Follow the submission workflow above
- **Want to help**: See `CONTRIBUTING.md`
- **Found a bug**: Create a GitHub Issue
- **Have a question**: Ask in GitHub Discussions

---

Happy coding! May your tank dominate the arena! 🏆🤖
