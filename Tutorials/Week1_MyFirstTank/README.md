# Week 1: My First Tank! 🎮

Welcome to your first week of Python Tank Wars! This week you'll:
1. Set up your GitHub account
2. Learn what a tank program is
3. Create your very first fighting tank

## Part 1: Getting on GitHub (20 minutes)

GitHub is like a magic folder where programmers store their code and share it with others.

### Steps to Sign Up:
1. Go to [github.com](https://github.com)
2. Click "Sign Up"
3. Choose a cool username (like "TankMaster2025" or "CodeWarrior")
4. Use your email and create a password
5. Verify your account

### Why GitHub?
- Save your code safely in the cloud
- Share your tanks with friends
- Learn from other people's code
- Show off your awesome creations!

## Part 2: Understanding Tank Programs (15 minutes)

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

## Part 3: Your First Tank - "MyFirstTank"

Let's create a simple tank that moves and shoots!

### Create Your Tank File

Create a file called `my_first_tank.py` and copy this code:

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

## Part 4: Make It Your Own! (20 minutes)

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

## Part 5: Testing Your Tank

To run your tank and see it in action:

```bash
# We'll set up the battle arena next week!
# For now, just make sure your code has no errors
python my_first_tank.py
```

## Homework

Before next week:
1. Create your tank file
2. Change at least 3 things to make it your own
3. Share your tank in the class discussion

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
