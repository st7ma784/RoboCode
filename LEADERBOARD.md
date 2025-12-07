# 🏆 Leaderboard

*Last updated: 2025-12-07*

Welcome to the Python Tank Wars Leaderboard! This is where the best tanks compete for glory!

## Current Rankings

| Rank | Tank | Author | Score | W/L/T | Accuracy | Badge |
|------|------|--------|-------|-------|----------|-------|
| 🥇 | ChampionBot | Sample | 0 | 0/0/0 | 0% | 👑 |

*Submit your tank to join the leaderboard!*

## How to Climb the Leaderboard

1. **Create your tank** - Follow the tutorials
2. **Test locally** - Use `battle_runner.py` and `tank_doctor.py`
3. **Submit a PR** - Add your tank to `Submissions/YourName/`
4. **Earn points** - Win battles and improve your stats
5. **Earn badges** - Achieve milestones to unlock badges

## Scoring System

### Points per Battle
- **Win**: +100 points
- **Survival**: +50 points (if you survive the battle)
- **Damage Dealt**: +1 point per 10 damage
- **Damage Taken**: -1 point per 10 damage
- **Accuracy Bonus**: up to +25 points (based on hit percentage)

### Example Score Calculation
```
Win:              +100
Survived:         +50
Dealt 240 damage: +24
Took 80 damage:   -8
70% accuracy:     +17

Total:            +183 points
```

## Badge Legend

Earn badges by achieving these milestones:

- 🔰 **Rookie**: Submit your first tank
- ⚔️ **Warrior**: Fight 10 or more battles
- 🎯 **Sharpshooter**: Achieve 60%+ accuracy (minimum 5 battles)
- 🛡️ **Survivor**: Achieve 75%+ survival rate (minimum 5 battles)
- 👑 **Champion**: Reach #1 on the leaderboard
- 🏆 **Undefeated**: Win 5+ battles without any losses

## Statistics

### Overall Stats
- **Total Tanks**: 1
- **Total Battles**: 0
- **Total Submissions**: 0
- **Highest Score**: 0

### Battle Records
- Most wins: -
- Highest accuracy: -
- Best survival rate: -
- Most battles fought: -

## Hall of Fame

### Weekly Champions
*Coming soon!*

### Achievement Holders

**First Tank**: -
**First Win**: -
**First Undefeated**: -
**First to 1000 Points**: -

## Leaderboard Badges

Display your rank on your GitHub profile or in your submissions!

### How to Get Your Badge

After your tank is added to the leaderboard, badges are automatically generated. You can find them in the PR comments or generate them using:

```bash
python leaderboard_manager.py
```

### Example Badges

![Rank](https://img.shields.io/badge/rank-1-gold?style=for-the-badge&logo=trophy)
![Wins](https://img.shields.io/badge/wins-75%25-brightgreen?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/accuracy-85%25-brightgreen?style=for-the-badge&logo=target)
![Score](https://img.shields.io/badge/score-1500-blue?style=for-the-badge&logo=star)

## Tips for Success

1. **Start Simple**: Get a working tank first, then improve it
2. **Test Often**: Use `tank_doctor.py` to catch errors early
3. **Study Samples**: Learn from the sample tanks
4. **Read Guides**: Check the Guides folder for strategies
5. **Iterate**: Keep improving based on battle results
6. **Have Fun**: This is about learning, not just winning!

## Submission Guidelines

To appear on the leaderboard:

1. **Submit via Pull Request** to `Submissions/YourName/`
2. **Pass validation** - Tank Doctor must pass
3. **Include required methods** - At least `run()` method
4. **Follow the rules** - See CONTRIBUTING.md

## Rules

1. **No Cheating**: Don't access opponent's internal state
2. **Fair Play**: Don't exploit bugs in the system
3. **Be Original**: Write your own code
4. **Be Respectful**: Keep code and comments appropriate
5. **Have Fun**: This is a learning environment!

## Questions?

- **How often is the leaderboard updated?** After each successful PR merge
- **Can I resubmit?** Yes! Improve your tank and submit again
- **How are ties broken?** By number of wins, then by fewest battles
- **Can I see my battle videos?** Videos are available in the PR artifacts

---

Ready to join the battle? Start with [Week 1 Tutorial](Tutorials/Week1_MyFirstTank/README.md)!

Good luck, commander! 🚀
