# Sample Tanks

This folder contains example tanks of varying difficulty levels. Use these to:
- Test your own tanks against
- Learn new strategies
- Understand different complexity levels

## Difficulty Levels

### Level 1: Beginner
- **SittingDuck** - Doesn't move at all (easiest to beat!)

### Level 2: Easy
- **SpinBot** - Spins in place and shoots

### Level 3: Intermediate
- **Walls** - Drives around the perimeter
- **Tracker** - Follows and shoots at enemies

### Level 4: Advanced
- **Champion** - Uses advanced techniques from all tutorials

## Testing Your Tank

To test your tank against these samples:

```python
# Your battle runner script
from my_tank import MyTank
from Samples.sitting_duck import SittingDuck

# Run battle
battle([MyTank, SittingDuck])
```

## Learning from Samples

1. Start by reading **SittingDuck** - the simplest possible tank
2. Progress to **SpinBot** - adds basic movement
3. Study **Walls** - boundary awareness
4. Analyze **Tracker** - targeting and following
5. Master **Champion** - combines all skills

Each tank is heavily commented to help you learn!
