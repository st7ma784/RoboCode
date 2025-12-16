# GitHub Actions - Automated Tank Battles

This directory contains GitHub Actions workflows that automatically run tank battles when submissions are added or updated.

## Tank Battle Arena Workflow

**File:** `tank-battles.yml`

### What It Does

Every time someone submits a tank (push or pull request), this workflow:

1. **Discovers Submitted Tanks**
   - Scans `Submissions/` folder for GUI-compatible tanks (`*_gui.py`)
   - Validates each tank has a matching `.json` config file
   - Lists all participants

2. **Runs Round-Robin Battles**
   - Launches Tank Royale server via Docker
   - Runs each tank against every other tank
   - Each battle lasts 60 seconds
   - Tracks wins, losses, and errors

3. **Generates Results**
   - Creates `SCORESHEET.md` with overall rankings
   - Updates individual `BATTLE_RECORD.md` for each submission
   - Saves detailed battle data as JSON artifacts

4. **Shares Results**
   - Comments on PRs with battle results
   - Commits scoresheets back to the repository
   - Uploads artifacts for download

### Triggers

The workflow runs when:
- **Push** - Changes to `Submissions/**/*.py` or `Submissions/**/*.json`
- **Pull Request** - Changes to submission files
- **Manual** - Via `workflow_dispatch` (Actions tab → Run workflow)

### System Architecture

```
┌─────────────────────────────────────────┐
│   GitHub Actions Runner (Ubuntu)        │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Tank Royale Server (Docker)   │    │
│  │  Port 7654: WebSocket          │    │
│  │  Port 8080: REST API           │    │
│  └────────────────────────────────┘    │
│              ↑                          │
│              │ WebSocket connections    │
│              │                          │
│  ┌──────────┴──────────┐               │
│  │                     │               │
│  ▼                     ▼               │
│ ┌────┐             ┌────┐              │
│ │Bot1│ subprocess  │Bot2│ subprocess   │
│ └────┘             └────┘              │
│                                         │
└─────────────────────────────────────────┘
```

### How Battles Work

1. **Docker Service Starts**
   - Tank Royale server launches automatically
   - Health checks ensure server is ready

2. **Tank Discovery**
   - Python script scans for `*_gui.py` files
   - Validates JSON configs exist
   - Creates `discovered_tanks.json`

3. **Battle Execution** (for each pair of tanks)
   ```python
   # Launch tank 1
   proc1 = subprocess.Popen([python, tank1.py])

   # Launch tank 2
   proc2 = subprocess.Popen([python, tank2.py])

   # Wait for connection (5 seconds)
   await asyncio.sleep(5)

   # Battle runs (60 seconds)
   await asyncio.sleep(60)

   # Collect results and terminate
   ```

4. **Result Collection**
   - Battle status tracked (completed/failed)
   - Stats aggregated per tank
   - Scoresheets generated

### Output Files

**Generated Files:**
- `SCORESHEET.md` - Overall tournament results
- `Submissions/{Author}/BATTLE_RECORD.md` - Individual tank records
- `battle_results/results_{timestamp}.json` - Raw battle data

**Example SCORESHEET.md:**
```markdown
# 🎮 Tank Battle Results

**Generated:** 2025-12-16T01:23:45Z
**Total Battles:** 15
**Participants:** 6

## 📊 Battle Summary

| Tank 1 | Tank 2 | Status |
|--------|--------|--------|
| FinalBoss | Challenger | ✅ completed |
| ...

## 🏆 Rankings

| Rank | Tank | Author | Battles |
|------|------|--------|---------|
| 🥇 1 | FinalBoss | ClaudeCode | 5 |
```

**Example BATTLE_RECORD.md:**
```markdown
# final_boss_tank_gui - Battle Record

**Author:** ClaudeCode
**Last Updated:** 2025-12-16 01:30:00 UTC

## Battle Record

| Opponent | Result |
|----------|--------|
| challenger_tank_gui | ✅ Completed |
| example_tank_gui | ✅ Completed |

## Statistics

- Total Battles: 2
- Wins: 0  (requires API integration)
- Losses: 0
- Errors: 0
- Win Rate: N/A
```

### Current Limitations

**Battle Results Parsing:**
The workflow successfully:
- ✅ Launches tanks as separate processes
- ✅ Connects them to Tank Royale server
- ✅ Runs battles for 60 seconds
- ✅ Tracks battle completion status

**TODO - Future Enhancements:**
- ⏳ Parse actual battle results from Tank Royale WebSocket events
- ⏳ Determine winner/loser from damage dealt
- ⏳ Calculate detailed statistics (accuracy, damage, survival time)
- ⏳ Generate replay files for visualization
- ⏳ Implement ELO rating system

The infrastructure is in place - we just need to integrate the Tank Royale event listener to parse real-time battle data.

### Artifacts

Each workflow run uploads artifacts containing:
- `battle_results/` - JSON files with battle data
- `SCORESHEET.md` - Generated scoresheet
- `discovered_tanks.json` - List of participating tanks

**Download artifacts:**
1. Go to Actions tab
2. Click on a workflow run
3. Scroll to "Artifacts" section
4. Download `battle-results-{sha}`

### Manual Triggering

To run battles manually:

1. Go to **Actions** tab in GitHub
2. Select **Tank Battle Arena** workflow
3. Click **Run workflow** button
4. Select branch (usually `main`)
5. Click **Run workflow**

This is useful for:
- Testing the workflow
- Re-running battles after server updates
- Generating fresh scoresheets

### Debugging

**If battles fail:**

1. **Check workflow logs:**
   - Actions tab → Click failed run → Click "Run battle orchestrator" step

2. **Common issues:**
   - Missing `.json` config file for a tank
   - Tank code has syntax errors
   - Tank doesn't inherit from `BaseBot`
   - Server health check fails

3. **Validate tank locally:**
   ```bash
   # Test that tank can launch
   python Submissions/YourName/your_tank_gui.py

   # Should see connection attempt (will fail without server)
   ```

### Adding Your Tank

For your tank to be included in automated battles:

1. **Create GUI-compatible tank:**
   ```python
   from robocode_tank_royale.bot_api import BaseBot, BotInfo

   class YourTank(BaseBot):
       async def run(self):
           # Your code here
           pass
   ```

2. **Create JSON config:**
   - File: `your_tank_gui.json`
   - Same directory as your tank

3. **Submit via PR:**
   - Place in `Submissions/YourName/`
   - Push to your fork
   - Create pull request

4. **Workflow runs automatically:**
   - Discovers your tank
   - Runs battles
   - Comments results on PR

### Configuration

**Workflow Settings:**

```yaml
# Trigger paths
paths:
  - 'Submissions/**/*.py'
  - 'Submissions/**/*.json'

# Battle duration per match
battle_timeout: 60 seconds

# Connection timeout
connection_timeout: 5 seconds

# Server health check
health_interval: 10 seconds
```

**To modify:**
Edit `.github/workflows/tank-battles.yml`

### Performance

**Current metrics:**
- Tank discovery: ~2 seconds
- Per battle: ~70 seconds (5s connect + 60s battle + 5s cleanup)
- For N tanks: `N*(N-1)/2 * 70` seconds total

**Example:**
- 3 tanks = 3 battles = ~3.5 minutes
- 6 tanks = 15 battles = ~17.5 minutes
- 10 tanks = 45 battles = ~52.5 minutes

GitHub Actions free tier: 2000 minutes/month (should be plenty!)

### Security

**Sandboxing:**
- Runs in isolated GitHub Actions environment
- Each tank runs as separate subprocess
- Docker container for server
- No access to secrets or tokens

**Safe to run:**
- User-submitted tank code is executed
- But isolated from repository secrets
- Cannot modify workflow files
- Cannot access other runners

### Contributing

To improve the workflow:

1. **Add WebSocket event parsing:**
   - Listen to battle events from server
   - Parse `BotDeathEvent`, `BulletHitEvent`, etc.
   - Calculate real win/loss/damage stats

2. **Add replay generation:**
   - Save battle recordings
   - Upload as artifacts
   - Link in scoresheets

3. **Add ELO ratings:**
   - Calculate skill ratings
   - Update over time
   - Show in leaderboard

4. **Optimize performance:**
   - Run battles in parallel (multiple servers)
   - Reduce battle duration for CI
   - Cache Docker images

---

**Questions?** Open an issue or check the [Tank Royale API docs](https://robocode-dev.github.io/tank-royale/)
