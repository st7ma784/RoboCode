# Quick Start Guide

Get started with Python Tank Wars in 5 minutes!

## Setup (One-time)

### 1. Install Python

Make sure you have Python 3.8 or newer:
```bash
python --version
```

If not installed, download from [python.org](https://python.org)

### 2. Install Dependencies

```bash
cd RoboCode
pip install -r requirements.txt
```

## Your First Steps

### Week 1: Create Your First Tank

1. Go to `Tutorials/Week1_MyFirstTank/`
2. Read the `README.md`
3. Open `my_first_tank.py` and customize it
4. Make it your own!

```bash
cd Tutorials/Week1_MyFirstTank
python my_first_tank.py  # Check for errors
```

### Test Your Tank

```bash
# Test against SittingDuck
python ../../battle_runner.py my_first_tank.py ../../Samples/sitting_duck.py

# (Note: battle_runner.py needs to be created based on your chosen framework)
```

## Learning Path

Follow the tutorials in order:

1. **Week 1** (30 min): `Tutorials/Week1_MyFirstTank/`
   - Create basic tank
   - Understand structure
   - Make it move and shoot

2. **Week 2** (45 min): `Tutorials/Week2_Trigonometry/`
   - Learn angles and distance
   - Predict enemy movement
   - Improve targeting

3. **Week 3** (45 min): `Tutorials/Week3_BoundaryChecking/`
   - Avoid walls
   - Check boundaries
   - Validate targets

4. **Week 4** (60 min): `Tutorials/Week4_Strategy/`
   - Unpredictable movement
   - React to events
   - Use randomness

5. **Week 5** (60 min): `Tutorials/Week5_AdvancedTargeting/`
   - Hit probability
   - Shot simulation
   - Energy management

## Quick Reference

### Project Structure
```
RoboCode/
├── Tutorials/          ← Start here!
│   ├── Week1_MyFirstTank/
│   ├── Week2_Trigonometry/
│   ├── Week3_BoundaryChecking/
│   ├── Week4_Strategy/
│   └── Week5_AdvancedTargeting/
├── Samples/            ← Example tanks to fight
├── Guides/             ← Deep-dive explanations
├── Submissions/        ← Submit your tank here
└── README.md           ← Overview
```

### Useful Commands

```bash
# Check for Python errors
python your_tank.py

# Install dependencies
pip install -r requirements.txt

# Run tests (if you create them)
pytest

# Format code (optional)
black your_tank.py
```

### Sample Tanks to Fight

Test your tank against these (in order of difficulty):

1. `Samples/sitting_duck.py` - Doesn't move
2. `Samples/spin_bot.py` - Spins in place
3. `Samples/walls_bot.py` - Follows walls
4. `Samples/tracker_bot.py` - Hunts you down
5. `Samples/champion_bot.py` - Uses all techniques

## Getting Help

### Error Messages

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"IndentationError"**
- Check your spaces/tabs
- Python is picky about indentation

**"AttributeError"**
- Make sure you're using `self.` for instance variables
- Check spelling

### Resources

- **Python Basics**: `Guides/python_basics.md`
- **Math Help**: `Guides/trigonometry_guide.md`
- **Strategy Tips**: `Guides/strategy_guide.md`
- **GitHub Issues**: Ask questions!

## Next Steps

After Week 1:
1. ✅ Complete Week 2 tutorial
2. ✅ Test against SpinBot
3. ✅ Read Python Basics guide
4. ✅ Experiment with your tank

After Week 5:
1. ✅ Create your ultimate tank
2. ✅ Submit to Submissions folder
3. ✅ Create a Pull Request
4. ✅ See your battle results!

## Tips for Success

1. **Go Slow**: One week at a time
2. **Experiment**: Change values and see what happens
3. **Test Often**: Run your tank after each change
4. **Have Fun**: It's about learning, not winning
5. **Ask Questions**: We're here to help!

---

Ready? Start with `Tutorials/Week1_MyFirstTank/README.md`!

Good luck, commander! 🚀
