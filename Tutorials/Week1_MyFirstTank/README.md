# Week 1: My First Tank! 🎮🚀

> **Note:** This tutorial uses the BaseBot API which uses **property assignments** instead of method calls.
> - Movement: `self.forward = 100` (not `self.forward(100)`)
> - Turning: `self.turn_body = 45` (not `self.turn_right(45)`)
> - All event handlers must be `async` and use `await` for actions like `await self.fire()`

Welcome to Python Tank Wars! Get ready to build your very own fighting robot tank and watch it battle in the arena!

This week you'll:
1. Learn about GitHub (your code's home on the internet!)
2. Set up Python on your computer
3. Download the RoboCode battle arena
4. Create your very first fighting tank
5. Watch it battle in the arena!
6. Share your tank on GitHub for others to battle!

## Part 1: Understanding GitHub (10 minutes)

### What is GitHub? 🏠

Think of GitHub like **Instagram for code**! Instead of sharing photos, programmers share their code projects. Here's why it's awesome:

- **📦 It's a Backpack for Code**: Stores all your tank programs safely in the cloud
- **⏰ It's a Time Machine**: See every change you ever made and undo mistakes
- **🤝 It's a Collaboration Tool**: Work with friends on the same tank
- **🏆 It's a Portfolio**: Show off your best tanks to everyone!
- **🤖 It Has Robots**: GitHub Actions automatically test your tank in battles!

### Real-World Analogy

Imagine you're writing a story:
- **Without GitHub**: Save to one file. Computer crashes? Story gone. Want to try a different ending? You have to delete the old one or make copies like "story_v2.docx", "story_final.docx", "story_final_REALLY.docx"
- **With GitHub**: Every version saved forever. Try new ideas safely. Work on different chapters at once. Your friend can read and suggest edits. If your computer explodes, your story is still safe online!

### Creating Your GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign Up" (it's free!)
3. Choose a cool username (this will be public! Pick something you like)
4. Use your real email (you'll need to verify it)
5. Solve the puzzle (proves you're not a robot 🤖)
6. Check your email and click the verification link

**🎉 Congratulations!** You now have a home for all your future code projects!

### Forking This Project (Making Your Own Copy)

To create your own version of Python Tank Wars:

1. Go to the main RoboCode repository (your instructor will give you the link)
2. Click the **"Fork"** button in the top-right corner
3. This creates YOUR OWN copy of the entire project!
4. Now you can change anything without breaking the original

**Analogy**: Forking is like photocopying a recipe book. You have the same recipes, but you can write notes, add your own recipes, and highlight your favorites without messing up the library's copy!

## Part 2: Setting Up Your Battle Station (15 minutes)

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

### Step 2: Download Your Forked Project from GitHub

Now let's get YOUR copy of the code onto your computer!

**Option A: Download as ZIP (Easiest for Beginners)**
1. Go to YOUR forked repository on GitHub (github.com/YOUR_USERNAME/RoboCode)
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Unzip it to your Documents folder
5. Rename the folder from "RoboCode-main" to "RoboCode"

**Option B: Clone with Git (Recommended if you've used it before)**
```bash
# Replace YOUR_USERNAME with your actual GitHub username!
git clone https://github.com/YOUR_USERNAME/RoboCode.git
cd RoboCode
```

**What's the difference?**
- **ZIP download**: Like getting a snapshot. Easy to start, but you'll need to upload changes manually later.
- **Git clone**: Like having a live connection. Changes sync automatically, but requires learning a few extra commands.

### Step 3: Download RoboCode Tank Royale (The Battle Arena!)

This is the actual game engine where your tanks fight! You write the AI (brains), it provides the arena (body).

**🎮 Step 3a: Download the Battle Arena**

Visit the official releases page:
👉 [Robocode Tank Royale Releases](https://github.com/robocode-dev/tank-royale/releases)

Look for the latest release and download the right file for your computer:

- **Windows**: `robocode-tank-royale-gui-x.x.x-win64.zip`
- **Mac**: `robocode-tank-royale-gui-x.x.x-mac.dmg`
- **Linux**: `robocode-tank-royale-gui-x.x.x-linux.tar.gz`

**🗂️ Step 3b: Install It**

**Windows:**
1. Unzip the downloaded file
2. Move the `robocode-tank-royale` folder to `C:\Program Files\` (or anywhere you like!)
3. Double-click `robocode-tank-royale.exe` to start

**Mac:**
1. Open the `.dmg` file
2. Drag "Robocode Tank Royale" to your Applications folder
3. Open it from Applications (you might need to right-click → Open the first time due to security)

**Linux:**
1. Extract: `tar -xzf robocode-tank-royale-*.tar.gz`
2. Move to /opt: `sudo mv robocode-tank-royale /opt/`
3. Run: `/opt/robocode-tank-royale/robocode-tank-royale`

### Step 4: Install Python Dependencies

Open your terminal or command prompt and navigate to YOUR RoboCode folder:

```bash
cd Documents/RoboCode  # Or wherever you extracted it!
pip install -r requirements.txt
```

This installs all the Python tools needed to control your tank!

### Step 5: Test Your Tank in the Arena!

**🚀 Starting Your First Battle**

1. **Start the Robocode Tank Royale GUI**:
   - **Windows**: Double-click `robocode-tank-royale.exe`
   - **Mac**: Open from Applications
   - **Linux**: Run the executable from where you installed it

2. **The arena window will open** - this is where the battles happen!

3. **Connect your tank to the arena**:

Open a terminal in your RoboCode project folder and run:

```bash
python Tutorials/Week1_MyFirstTank/my_first_tank.py
```

Your tank will say: `🚀 Connected to arena! Waiting for battle to start...`

4. **Add an opponent**:

Open a SECOND terminal and run a sample tank:

```bash
python Samples/sitting_duck.py
```

5. **In the GUI window**, click **"Start Battle"**!

Watch your tank fight! 🎮💥

**What you'll see:**
- Tanks moving around the arena
- Bullets flying
- Explosions when tanks get hit!
- A winner at the end!

### 🎯 Quick Testing Without the GUI

If you just want to check if your code works (no graphics needed):

```bash
# Just verify the tank code runs
python Tutorials/Week1_MyFirstTank/my_first_tank.py --test
```

This checks for errors without needing the GUI running!
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

## Part 2: What is a Tank Program? (10 minutes)

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
        self.turn_body = 10

        # Move forward a little
        self.ahead(20)

        # Shoot!
        self.fire(1)

    def on_scanned_robot(self, event):
        """Called when we see an enemy tank!"""
        # Calculate distance from event coordinates
        dx = event.x - self.get_x()
        dy = event.y - self.get_y()
        distance = math.sqrt(dx**2 + dy**2)
        print(f"I see an enemy at {distance:.1f} units away!")
        # Shoot at them!
        self.fire(3)

    def on_hit_by_bullet(self, hit_by_bullet):
        """Called when we get hit by a bullet!"""
        print("Ouch! I got hit!")
        # Turn around to face attacker
        self.turn_body = 90
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
    self.turn_body = 10
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
# Start RoboCode GUI, then run your tank:
python Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/sitting_duck.py
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

🎉 You should see your tank fighting! The battle runner will show you:
- What's happening in the battle
- How much damage each tank deals
- Who wins!

### Battle Against Different Opponents

Try fighting different sample tanks to see how your tank performs:

**Easy opponent:**
```bash
# Start RoboCode GUI, then run your tank:
python Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/sitting_duck.py
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

**Medium opponent:**
```bash
# Start RoboCode GUI, then run your tank:
python Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/spin_bot.py
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

**Harder opponent:**
```bash
# Start RoboCode GUI, then run your tank:
python Tutorials/Week1_MyFirstTank/my_first_tank.py Samples/walls_bot.py
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

**Battle ALL sample tanks at once:**
```bash
# Start RoboCode GUI, then run your tank:
python Tutorials/Week1_MyFirstTank/my_first_tank.py --all-samples
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

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
# Start RoboCode GUI, then run your tank:
python Submissions/YourName/your_tank.py Samples/sitting_duck.py
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!

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
- `self.forward = -distance` - Move backward (negative distance)
- `self.turn_body = degrees` - Turn right (positive degrees)
- `self.turn_body = -degrees` - Turn left (negative degrees)

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
