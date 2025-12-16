# Week 9: Team Battles - Coordinated Multi-Bot Strategies

> **Note:** This tutorial uses the BaseBot API which uses **property assignments** instead of method calls.
> - Movement: `self.forward = 100` (not `self.forward(100)`)
> - Turning: `self.turn_body = 45` (not `self.turn_right(45)`)
> - All event handlers must be `async` and use `await` for actions like `await self.fire()`

## 🎯 Learning Objectives
- Understand team communication and coordination
- Implement role-based team strategies
- Master teammate identification and messaging
- Create synergistic bot behaviors

## 📚 Team Battle Concepts

### Team Communication
Tank Royale allows teams to communicate through:
- **Teammate Events**: `on_scanned_bot` with `is_teammate` flag
- **Broadcast Messages**: Share position, target, and strategy data
- **Role Assignment**: Each bot has a specific role in the team

### Team Strategy Patterns

#### 1. **Swarm Behavior** (swarm_team.py)
Coordinated pack hunting with distributed damage:
- **Leader**: Coordinates attack patterns
- **Follower 1 & 2**: Follow leader and surround enemies
- All bots focus fire on the same target
- Dynamic formation based on battlefield state

#### 2. **Hunter-Killer** (hunter_killer_team.py)
Specialized roles for tracking and elimination:
- **Hunter 1 & 2**: Scout and track enemies, relay positions
- **Killer**: Heavy firepower bot that eliminates tagged targets
- Hunters use weak shots to conserve energy
- Killer uses maximum power for confirmed kills

#### 3. **Vampire Team** (vampire_team.py)
Energy farming with servant sacrifice:
- **Vampire Master**: Main combat bot, powerful and strategic
- **Servant 1 & 2**: Sacrifice themselves to feed the master
- Servants position near master for easy farming
- Master gains health by shooting servants when needed
- Servants avoid enemies, prioritize master survival

## 🔧 Key APIs for Teams

```python
# Check if a scanned bot is a teammate
def on_scanned_bot(self, event):
    if event.is_teammate:
        # It's your teammate! Position comes directly from event
        teammate_x = event.x
        teammate_y = event.y
    else:
        # It's an enemy!
        pass

# Send messages to teammates (broadcast)
def broadcast_message(self, message_type, data):
    # Note: Tank Royale uses shared state, not direct messaging
    # Teams coordinate through scanned bot events
    pass

# Identify your role
def __init__(self, bot_info: BotInfo):
    super().__init__(bot_info=bot_info)
    self.role = self.get_role_from_name()
    
def get_role_from_name(self):
    if "leader" in self.name.lower():
        return "LEADER"
    elif "hunter" in self.name.lower():
        return "HUNTER"
    elif "killer" in self.name.lower():
        return "KILLER"
    # etc...
```

## 🎮 Team Strategies Explained

### Swarm Strategy
```
Formation:
    Enemy
      ↑
  ┌───┼───┐
  │   │   │
 F1  Leader F2

- Leader locks onto enemy
- Followers maintain 120° spacing
- All fire when enemy in range
- Collapse formation when enemy weakened
```

### Hunter-Killer Strategy
```
Battlefield:
  H1 ←─┐
       ├→ Enemy ←─ KILLER
  H2 ←─┘

- Hunters scan quadrants
- Relay enemy position to Killer
- Killer calculates intercept
- Hunters retreat when Killer engages
```

### Vampire Strategy
```
Energy Flow:
  Servant1 ──→ Master ──→ Enemy
  Servant2 ──→   ↑
                 │
            (Farms servants
             when low HP)

- Servants stay near Master
- Master shoots servants for +3 energy
- Master engages enemies at full power
- Servants respawn, repeat cycle
```

## 📊 Team Configuration

Each team needs:
1. **Individual bot JSONs** for each team member
2. **Team JSON** that references all members
3. **Consistent naming** for role identification

Example team.json:
```json
{
  "name": "SwarmTeam",
  "version": "1.0.0",
  "gameTypes": ["melee", "team"],
  "teamMembers": [
    "SwarmLeader",
    "SwarmFollower1", 
    "SwarmFollower2"
  ]
}
```

## 🎯 Best Practices

1. **Clear Roles**: Each bot should know its purpose
2. **Fallback Behavior**: Handle missing teammates gracefully
3. **Energy Management**: Don't all shoot at once (waste)
4. **Spacing**: Avoid friendly fire and collisions
5. **Target Priority**: Focus fire, don't split damage
6. **Adaptability**: Adjust strategy when teammates die

## 🏆 Challenges

1. **Basic**: Get all three bots to track each other
2. **Intermediate**: Implement one complete team strategy
3. **Advanced**: Create a hybrid team that switches strategies
4. **Expert**: Build a team that adapts based on enemy behavior

## 📝 Testing Your Team

```bash
# Test swarm behavior
./start_robocode.sh
# In GUI: Select all 3 SwarmTeam bots + enemies

# Test hunter-killer coordination
# Select 2 Hunters + 1 Killer + enemies

# Test vampire strategy  
# Select Vampire Master + 2 Servants + enemies
```

## 🎓 Key Takeaways

- Teams require coordination, not just individual skill
- Role specialization creates powerful synergies
- Communication is key (scan for teammates constantly)
- Energy and position management matter more in teams
- A coordinated team beats stronger individual bots

---

**Next Steps**: Run the example teams, observe their behavior, then create your own team with a unique strategy!
