# Week 1: My First Tank! 🎮🚀

Welcome to Python Tank Wars! Get ready to build your very own fighting robot tank and watch it battle in the arena!

This week you'll:
1. Set up Python on your computer
2. Learn what a tank program is
3. Create your very first fighting tank
4. See it battle in the arena!
5. Submit your tank to compete with others

## Part 1: Setting Up Your Battle Station (15 minutes)

Let's get your computer ready to run tank battles!

### Step 1: Install Python

**Windows:**
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download Python 3.8 or newer
3. Run the installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH" before clicking Install!

**Mac:**
1. Open Terminal (search for "Terminal" in Spotlight)
2. Install Homebrew if you don't have it: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Run: `brew install python3`

**Linux:**
Most Linux systems have Python installed! Open a terminal and check:
```bash
python3 --version
```
If you need to install it: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### Step 2: Get the RoboCode Project

**Option A: Download the Code**
1. Go to the RoboCode GitHub page
2. Click the green "Code" button
3. Click "Download ZIP"
4. Unzip it to your Documents folder

**Option B: Clone with Git (if you know Git)**
```bash
git clone https://github.com/YourUsername/RoboCode.git
cd RoboCode
```

### Step 3: Install Battle Requirements

Open your terminal or command prompt and navigate to the RoboCode folder:

```bash
cd Documents/RoboCode
pip install -r requirements.txt
```

This installs all the tools needed to run tank battles!

### Step 3.5: Install Battle Server (Optional - For Visual Battles)

**Good news:** You can start learning RIGHT NOW without this! The `battle_runner.py` validates your code works. But if you want to see **actual animated tank battles with graphics**, you'll need the Robocode Tank Royale server.

**Quick Install Options:**

**🎮 Option A: Pre-built Download (Easiest)**
1. Visit [Robocode Tank Royale Releases](https://github.com/robocode-dev/tank-royale/releases)
2. Download the latest release for your system (Windows/Mac/Linux)
3. Extract the files
4. Double-click the server to run it
5. Open your web browser to `http://localhost:8080` to watch battles!

**🐳 Option B: Docker (For Advanced Users)**
```bash
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
```

**🔧 Option C: Build from Source (Requires Java 11+)**
```bash
git clone https://github.com/robocode-dev/tank-royale.git
cd tank-royale
./gradlew build
./gradlew run
```

**Note:** Your tanks need a `.json` config file (already created for you!) to connect to the server. All tutorial and sample tanks now have these files ready to go!

### Step 4: Test Your Setup

Let's make sure everything works:

```bash
python battle_runner.py Samples/sitting_duck.py Samples/spin_bot.py
```

You should see a battle happen! If you see colorful text showing a battle, you're ready! 🎉

### Step 5: Watch Your First Battle in the GUI! (Optional but Awesome! 🎮)

**Two ways to run battles:**
1. **Text mode** (battle_runner.py) - Quick validation, no setup needed
2. **Visual GUI** (Tank Royale) - See animated battles with explosions! 💥

Let's get the GUI working so you can SEE your tanks fight!

#### 🎮 Starting the Visual Battle GUI

**Step 5a: Start the Tank Royale Server**

Find where you installed Robocode Tank Royale and start the server:

**Windows:**
- Double-click `robocode-tank-royale-server.exe` or `tank-royale.exe`

**Mac/Linux:**
```bash
# If you downloaded the release:
./robocode-tank-royale-server

# If using Docker:
docker run -p 7654:7654 -p 8080:8080 robocode/tank-royale-server
```

You should see a message saying the server is running on port 7654!

**Step 5b: Open the Battle Arena in Your Browser**

Open your web browser and go to:
```
http://localhost:8080
```

You should see the **Robocode Tank Royale** arena! 🎮

**Step 5c: Launch Your Tank**

Open a **new terminal** (keep the server running!) and run:

```bash
# From the RoboCode directory
python run_gui_battle.py Tutorials/Week1_MyFirstTank/my_first_tank.py
```

You'll see:
```
🚀 STARTING TANK - Connect to GUI
📺 Open your browser to: http://localhost:8080
```

**Step 5d: Start the Battle!**

1. In your browser (at `http://localhost:8080`), you should see your tank listed
2. Select 1-2 sample bots from `Samples/` folder (run them in separate terminals)
3. Click **"Start Battle"**
4. **WATCH YOUR TANK FIGHT!** 💥🎯

#### 🎯 Quick Start Commands for GUI Battles

**Launch sample opponents in separate terminals:**

Terminal 1 (Your tank):
```bash
python run_gui_battle.py Tutorials/Week1_MyFirstTank/my_first_tank.py
```

Terminal 2 (Opponent 1):
```bash
python run_gui_battle.py Samples/sitting_duck.py
```

Terminal 3 (Opponent 2):
```bash
python run_gui_battle.py Samples/spin_bot.py
```

Then in browser (`http://localhost:8080`):
- Select all 3 bots
- Click "Start Battle"
- Watch the action! 🎮

#### 📝 Important Notes

**Server Must Be Running:** The Tank Royale server must be running BEFORE you launch bots.

**Multiple Terminals:** Each bot runs in its own terminal. Keep them open!

**Stopping Bots:** Press `Ctrl+C` in each terminal to stop a bot.

**Can't Connect?**
- Make sure server is running (check for "Server running on port 7654")
- Check browser is at `http://localhost:8080` (not https!)
- Make sure no firewall is blocking ports 7654 or 8080

#### 🆚 Battle Runner vs GUI

| Feature | battle_runner.py | GUI (run_gui_battle.py) |
|---------|------------------|-------------------------|
| **Setup** | No extra setup | Need Tank Royale server |
| **Speed** | Instant | Takes 30 seconds to setup |
| **Visual** | Text only | Animated graphics! 🎨 |
| **Purpose** | Quick testing | Watching epic battles |
| **Best for** | Development | Showcasing your tank |

**TIP:** Use `battle_runner.py` while coding, then use the GUI to watch your tank in action!

## Part 2: Getting on GitHub (10 minutes)

GitHub is where you'll share your tank and compete with others around the world!

### Steps to Sign Up:
1. Go to [github.com](https://github.com)
2. Click "Sign Up"
3. Choose a cool username (like "TankCommander2025" or "CodeWarrior")
4. Use your email and create a password
5. Verify your account

### Fork the RoboCode Repository

1. Go to the RoboCode repository on GitHub
2. Click the "Fork" button in the top-right corner
3. This creates YOUR OWN copy of the project where you can add your tanks!

## Part 3: Understanding Tank Programs (10 minutes)

A tank program is like writing instructions for a robot. The tank will follow exactly what you tell it to do!

### What Can Your Tank Do?

Your tank has these abilities:
- **Move** - Go forward, backward, or turn
- **Scan** - Look for enemy tanks with your radar
- **Shoot** - Fire bullets at enemies
- **Sense** - Know when you're hit or see other tanks

### The Tank's Brain

Your tank has a "brain" which is the code you write. Every time the game updates (many times per second), your tank asks:
1. "What should I do now?"
2. Your code gives it instructions
3. The tank does what you said
4. Repeat!

## Part 4: Your First Tank - "MyFirstTank"

Let's create a simple tank that moves and shoots!

### Create Your Tank File

In the `Tutorials/Week1_MyFirstTank/` folder, open the file `my_first_tank.py` and you'll see this code:

```python
"""
My First Tank!
This tank spins around and shoots.
"""

class MyFirstTank:
    def __init__(self):
        """Set up our tank when it starts"""
        self.name = "MyFirstTank"

    def run(self):
        """This is the tank's brain - it runs over and over!"""
        # Spin our tank
        self.turn_right(10)

        # Move forward a little
        self.ahead(20)

        # Shoot!
        self.fire(1)

    def on_scanned_robot(self, scanned_robot):
        """Called when we see an enemy tank!"""
        print(f"I see an enemy at {scanned_robot.distance} units away!")
        # Shoot at them!
        self.fire(3)

    def on_hit_by_bullet(self, hit_by_bullet):
        """Called when we get hit by a bullet!"""
        print("Ouch! I got hit!")
        # Turn around to face attacker
        self.turn_right(90)
```

### Understanding the Code

Let's break down what each part does:

#### The Class
```python
class MyFirstTank:
```
This creates a "template" for your tank. Think of it like a blueprint for building your robot!

#### The __init__ Method
```python
def __init__(self):
    self.name = "MyFirstTank"
```
This runs once when your tank is born. It's like naming your tank when it's created.

#### The run Method
```python
def run(self):
    self.turn_right(10)
    self.ahead(20)
    self.fire(1)
```
This is the tank's main brain! It runs over and over:
- `turn_right(10)` - Turn 10 degrees to the right
- `ahead(20)` - Move forward 20 pixels
- `fire(1)` - Shoot a bullet with power 1

#### Event Methods
```python
def on_scanned_robot(self, scanned_robot):
```
This is called automatically when your radar spots an enemy! You can shoot at them here.

```python
def on_hit_by_bullet(self, hit_by_bullet):
```
This is called when you get hit! You can react and fight back.

## Part 5: Make It Your Own! (20 minutes)

Now it's your turn to experiment! Try changing these things:

### Easy Changes:
1. Change the tank's name to something cool
2. Make it turn left instead of right: change `turn_right` to `turn_left`
3. Make it move faster: increase the number in `ahead(20)` to `ahead(50)`
4. Make it shoot harder: change `fire(1)` to `fire(3)`

### Challenge Changes:
1. Make the tank move backward sometimes (hint: use `back(20)`)
2. Make it turn different amounts each time
3. Add a message when it scans an enemy: use `print("Found you!")`

## Part 6: See Your Tank Battle! 🎬

Time to watch your tank in action!

### Battle Against a Sample Tank

Run this command in your terminal (make sure you're in the RoboCode folder):

```bash
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/sitting_duck.py
```

🎉 You should see your tank fighting! The battle runner will show you:
- What's happening in the battle
- How much damage each tank deals
- Who wins!

### Battle Against Different Opponents

Try fighting different sample tanks to see how your tank performs:

**Easy opponent:**
```bash
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/sitting_duck.py
```

**Medium opponent:**
```bash
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/spin_bot.py
```

**Harder opponent:**
```bash
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/walls_bot.py
```

**Battle ALL sample tanks at once:**
```bash
python battle_runner.py Tutorials/Week1_MyFirstTank/my_first_tank.py --all-samples
```

### Making Changes and Testing

After you make changes to your tank:
1. Save the file
2. Run the battle command again
3. See if your changes made your tank better!

Keep experimenting until your tank can beat at least the sitting duck! 🎯

## Part 7: Submit Your Tank to the Arena! 🏆

Ready to show the world your tank? Let's submit it to compete!

### Step 1: Create Your Submission Folder

1. In the RoboCode project, find the `Submissions` folder
2. Create a new folder with YOUR name: `Submissions/YourName/`
3. Copy your `my_first_tank.py` file into this folder
4. Rename it to something cool like `awesome_tank.py` or `destroyer_bot.py`

### Step 2: Make Sure Your Tank Works

Test your tank one more time:
```bash
python battle_runner.py Submissions/YourName/your_tank.py Samples/sitting_duck.py
```

If it runs without errors, you're ready! 🎉

### Step 3: Create a Pull Request

Now let's share your tank with the world!

**If you're using GitHub Desktop:**
1. Open GitHub Desktop
2. Make sure you're in the RoboCode repository
3. You should see your new files in the "Changes" tab
4. Add a commit message: "Add [YourName]'s first tank!"
5. Click "Commit to main"
6. Click "Push origin"
7. Click "Create Pull Request"

**If you're using the command line:**
```bash
# Make sure you're in the RoboCode folder
cd Documents/RoboCode

# Add your new tank files
git add Submissions/YourName/

# Commit with a message
git commit -m "Add [YourName]'s first tank!"

# Push to your fork
git push origin main

# Now go to GitHub.com and click "Create Pull Request"
```

**If you're using the GitHub website:**
1. Go to your forked RoboCode repository on GitHub.com
2. Click "Add file" → "Upload files"
3. Drag your tank folder or files
4. Add commit message: "Add [YourName]'s first tank!"
5. Click "Commit changes"
6. Click the "Contribute" button
7. Click "Open pull request"

### Step 4: Fill Out the Pull Request

When creating your PR, add this info:

**Title:** `[Submission] YourName's First Tank`

**Description:**
```
## Tank Submission

**Tank Name:** MyAwesomeTank
**Week:** Week 1
**Strategy:** My tank spins and shoots!

I'm excited to see how my tank performs! 🎮
```

### Step 5: Watch the Magic Happen! ✨

After you submit your PR:
1. The automated system will run your tank in battles
2. It will create videos of your tank fighting
3. You'll get a scoresheet showing:
   - Wins and losses
   - Damage dealt
   - Accuracy percentage
   - Overall score
4. You'll appear on the leaderboard!

### Step 6: Improve and Resubmit!

After seeing how your tank does:
1. Make it better!
2. Test locally with the battle runner
3. Update your submission
4. Push the changes to your PR
5. Watch it battle again with the improvements!

## Homework

Before next week:
1. ✅ Set up Python and the battle runner
2. ✅ Customize your tank (change at least 3 things!)
3. ✅ Test it against at least 3 different sample tanks
4. ✅ Submit your tank via Pull Request
5. ✅ Check your battle results!

## What's Next?

Next week, you'll learn about **angles** and **trigonometry** so your tank can aim perfectly at moving enemies!

## Quick Reference

### Movement Commands
- `ahead(distance)` - Move forward
- `back(distance)` - Move backward
- `turn_right(degrees)` - Turn right
- `turn_left(degrees)` - Turn left

### Shooting Commands
- `fire(power)` - Shoot! Power can be 1-3
  - Power 1: Fast but weak bullet
  - Power 3: Slow but strong bullet

### Radar Commands
- `turn_radar_right(degrees)` - Turn radar right
- `turn_radar_left(degrees)` - Turn radar left

## Help!

Stuck? Here are common problems:

**"My code has an error!"**
- Check that all your parentheses `()` match up
- Make sure you indented (pressed Tab) inside the `def` blocks
- Python is picky about capital letters - `Fire` is different from `fire`

**"My tank doesn't do what I want!"**
- Add `print()` statements to see what's happening
- Try smaller numbers to see the effect more slowly
- Read the code out loud - does it match what you want?

---

Great job! You've created your first tank! 🎉
