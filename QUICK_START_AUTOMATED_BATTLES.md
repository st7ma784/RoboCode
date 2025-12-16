# Quick Start: Automated Battles

Your tank will battle automatically when you submit it!

## For Participants

### 1. Create Your Tank

**Required files in `Submissions/YourName/`:**
```
Submissions/YourName/
├── your_tank_gui.py      # Your tank code (inherits from BaseBot)
└── your_tank_gui.json    # Config file
```

**Minimal tank template:**
```python
from robocode_tank_royale.bot_api import BaseBot, BotInfo
from pathlib import Path

class YourTank(BaseBot):
    async def run(self):
        while True:
            self.forward(100)
            self.turn_radar_right(30)
            await self.go()

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    json_file = script_dir / "your_tank_gui.json"
    bot_info = BotInfo.from_file(str(json_file))
    bot = YourTank(bot_info=bot_info)
    import asyncio
    asyncio.run(bot.start())
```

**Minimal JSON config:**
```json
{
  "name": "YourTank",
  "version": "1.0",
  "authors": ["Your Name"],
  "description": "My awesome tank",
  "url": "",
  "countryCodes": ["US"],
  "gameTypes": ["melee", "1v1"],
  "platform": "Python",
  "programmingLang": "Python 3.x"
}
```

### 2. Test Locally (Optional)

**Quick validation:**
```bash
python battle_runner.py Submissions/YourName/your_tank_gui.py Samples/sitting_duck.py
```

**Visual test (requires server):**
```bash
# Terminal 1: Start server
./start_server.sh  # or double-click robocode-tank-royale-server

# Terminal 2: Run your tank
python run_gui_battle.py Submissions/YourName/your_tank_gui.py
```

### 3. Submit

**Option A: Via Git**
```bash
git add Submissions/YourName/
git commit -m "Add my awesome tank"
git push
```

**Option B: Via Pull Request**
1. Fork the repository
2. Add your files
3. Create PR

### 4. Watch Battles Run

**Automatic process:**
1. ✅ GitHub Actions detects your submission
2. ✅ Launches Docker Tank Royale server
3. ✅ Runs your tank vs all others
4. ✅ Generates scoresheet
5. ✅ Comments results on PR
6. ✅ Commits BATTLE_RECORD.md to your submission folder

**Results appear in:**
- PR comments (if using PR)
- `SCORESHEET.md` (overall rankings)
- `Submissions/YourName/BATTLE_RECORD.md` (your stats)
- Artifacts (detailed JSON data)

## Example Results

**SCORESHEET.md:**
```markdown
# 🎮 Tank Battle Results

**Generated:** 2025-12-16T01:23:45Z
**Total Battles:** 15
**Participants:** 6

## 🏆 Rankings

| Rank | Tank | Author | Battles |
|------|------|--------|---------|
| 🥇 1 | final_boss_tank_gui | ClaudeCode | 5 |
| 🥈 2 | your_tank_gui | YourName | 5 |
```

**Your BATTLE_RECORD.md:**
```markdown
# your_tank_gui - Battle Record

**Author:** YourName
**Last Updated:** 2025-12-16 01:30:00 UTC

## Battle Record

| Opponent | Result |
|----------|--------|
| final_boss_tank_gui | ✅ Completed |
| sitting_duck_gui | ✅ Completed |

## Statistics

- Total Battles: 2
- Wins: 0  (tracking coming soon)
- Losses: 0
- Errors: 0
```

## Troubleshooting

### "Tank not detected"

**Problem:** Your tank doesn't appear in battle results

**Fix:**
1. File must end with `_gui.py`
2. Must have matching `.json` file
3. Must inherit from `BaseBot`

### "Battle failed"

**Problem:** Status shows ❌ Failed

**Common causes:**
- Syntax error in tank code
- Missing imports
- JSON file malformed

**Debug:**
```bash
# Test locally first
python Submissions/YourName/your_tank_gui.py
```

### "No scoresheet generated"

**Problem:** Workflow runs but no SCORESHEET.md

**Check:**
1. View workflow logs in Actions tab
2. Look for error messages
3. Check artifacts were uploaded

## Advanced

### View Workflow Logs

1. Go to **Actions** tab on GitHub
2. Click latest workflow run
3. Click "Run battle orchestrator" step
4. See detailed logs

### Download Artifacts

1. Go to workflow run
2. Scroll to **Artifacts** section
3. Download `battle-results-{sha}.zip`
4. Extract to see JSON data

### Manual Trigger

1. **Actions** tab → **Tank Battle Arena**
2. Click **Run workflow**
3. Select branch
4. Click **Run workflow**

## What's Automated

| Feature | Status |
|---------|--------|
| Tank discovery | ✅ Working |
| Server launch | ✅ Working |
| Battle execution | ✅ Working |
| Completion tracking | ✅ Working |
| Scoresheet generation | ✅ Working |
| PR commenting | ✅ Working |
| Auto-commit results | ✅ Working |
| Winner determination | ⏳ Coming soon |
| Damage statistics | ⏳ Coming soon |
| Replay files | ⏳ Coming soon |

## Next Steps

Want to improve your tank?

1. **Read your BATTLE_RECORD.md** - See who you faced
2. **Check SCORESHEET.md** - See overall rankings
3. **Update your code** - Improve strategy
4. **Push changes** - New battles run automatically!

## Getting Help

**Issues?**
- Check [Workflow README](.github/workflows/README.md)
- See [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- Open GitHub issue

**Questions about battles?**
- See logs in Actions tab
- Download artifacts for details
- Check individual BATTLE_RECORD.md files

---

**Ready?** Add your tank to `Submissions/YourName/` and push! 🚀
