"""
Leaderboard Manager for Python Tank Wars

Manages rankings, scores, and badges for submitted tanks.
Generates shields.io badges for display.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
import urllib.parse


class LeaderboardManager:
    """
    Manages the tank leaderboard and badge system
    """

    def __init__(self, leaderboard_file: str = "leaderboard.json"):
        self.leaderboard_file = leaderboard_file
        self.data = self.load_leaderboard()

    def load_leaderboard(self) -> Dict:
        """Load the leaderboard from JSON file"""
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'r') as f:
                return json.load(f)
        else:
            # Return default structure
            return {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "rankings": [],
                "badge_criteria": {},
                "statistics": {
                    "total_tanks": 0,
                    "total_battles": 0,
                    "total_submissions": 0
                }
            }

    def save_leaderboard(self):
        """Save the leaderboard to JSON file"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_or_update_tank(self, tank_data: Dict) -> Dict:
        """
        Add a new tank or update existing tank's stats

        tank_data should include:
        - name: tank name
        - author: author name
        - file: file path
        - battle_results: dict with wins, losses, damage, etc.
        """
        name = tank_data['name']
        author = tank_data['author']

        # Find existing tank
        existing = None
        for tank in self.data['rankings']:
            if tank['name'] == name and tank['author'] == author:
                existing = tank
                break

        if existing:
            # Update existing tank
            self.update_tank_stats(existing, tank_data.get('battle_results', {}))
        else:
            # Add new tank
            new_tank = {
                "name": name,
                "author": author,
                "file": tank_data.get('file', ''),
                "total_score": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "battles_fought": 0,
                "total_damage_dealt": 0,
                "total_damage_taken": 0,
                "accuracy": 0.0,
                "survival_rate": 0.0,
                "avg_score_per_battle": 0.0,
                "badge": "rookie",
                "achievements": [],
                "first_battle": datetime.now().isoformat()
            }

            if 'battle_results' in tank_data:
                self.update_tank_stats(new_tank, tank_data['battle_results'])

            self.data['rankings'].append(new_tank)
            self.data['statistics']['total_tanks'] += 1

        # Recalculate rankings
        self.recalculate_rankings()

        # Award badges
        self.award_badges()

        # Save
        self.save_leaderboard()

        return self.get_tank_info(name, author)

    def update_tank_stats(self, tank: Dict, battle_results: Dict):
        """Update a tank's statistics from battle results"""
        # Update battle counts
        tank['battles_fought'] += 1
        if battle_results.get('won'):
            tank['wins'] += 1
        elif battle_results.get('lost'):
            tank['losses'] += 1
        else:
            tank['ties'] += 1

        # Update damage stats
        tank['total_damage_dealt'] += battle_results.get('damage_dealt', 0)
        tank['total_damage_taken'] += battle_results.get('damage_taken', 0)

        # Update accuracy
        if battle_results.get('shots_fired', 0) > 0:
            new_hits = battle_results.get('shots_hit', 0)
            new_shots = battle_results.get('shots_fired', 0)

            # Calculate weighted average accuracy
            old_accuracy = tank.get('accuracy', 0.0)
            old_battles = tank['battles_fought'] - 1

            if old_battles > 0:
                tank['accuracy'] = (old_accuracy * old_battles + (new_hits / new_shots)) / tank['battles_fought']
            else:
                tank['accuracy'] = new_hits / new_shots

        # Update survival rate
        if battle_results.get('survived'):
            old_survival = tank.get('survival_rate', 0.0)
            old_battles = tank['battles_fought'] - 1
            tank['survival_rate'] = (old_survival * old_battles + 1.0) / tank['battles_fought']
        else:
            old_survival = tank.get('survival_rate', 0.0)
            old_battles = tank['battles_fought'] - 1
            tank['survival_rate'] = (old_survival * old_battles) / tank['battles_fought']

        # Calculate score for this battle
        battle_score = self.calculate_battle_score(battle_results)
        tank['total_score'] += battle_score
        tank['avg_score_per_battle'] = tank['total_score'] / tank['battles_fought']

        # Update global stats
        self.data['statistics']['total_battles'] += 1

    def calculate_battle_score(self, battle_results: Dict) -> int:
        """
        Calculate score for a single battle

        Scoring system:
        - Win: 100 points
        - Survival: 50 points
        - Damage dealt: 1 point per 10 damage
        - Damage taken: -1 point per 10 damage
        - Accuracy bonus: up to 25 points
        """
        score = 0

        if battle_results.get('won'):
            score += 100
        if battle_results.get('survived'):
            score += 50

        score += battle_results.get('damage_dealt', 0) // 10
        score -= battle_results.get('damage_taken', 0) // 10

        # Accuracy bonus
        if battle_results.get('shots_fired', 0) > 0:
            accuracy = battle_results['shots_hit'] / battle_results['shots_fired']
            score += int(accuracy * 25)

        return max(0, score)  # Minimum score is 0

    def recalculate_rankings(self):
        """Sort tanks by total score and assign ranks"""
        # Sort by total score (descending)
        self.data['rankings'].sort(
            key=lambda x: (x['total_score'], x['wins'], -x['battles_fought']),
            reverse=True
        )

        # Assign ranks
        for i, tank in enumerate(self.data['rankings'], 1):
            tank['rank'] = i

    def award_badges(self):
        """Award badges based on criteria"""
        for tank in self.data['rankings']:
            badges = []

            # Rookie - first battle
            if tank['battles_fought'] >= 1:
                badges.append('rookie')

            # Warrior - many battles
            if tank['battles_fought'] >= 10:
                badges.append('warrior')

            # Sharpshooter - high accuracy
            if tank['accuracy'] >= 0.6 and tank['battles_fought'] >= 5:
                badges.append('sharpshooter')

            # Survivor - high survival rate
            if tank['survival_rate'] >= 0.75 and tank['battles_fought'] >= 5:
                badges.append('survivor')

            # Champion - rank 1
            if tank['rank'] == 1:
                badges.append('champion')

            # Undefeated
            if tank['wins'] >= 5 and tank['losses'] == 0:
                badges.append('undefeated')

            # Update badges
            tank['badge'] = badges[-1] if badges else 'rookie'
            tank['achievements'] = list(set(badges))

    def get_tank_info(self, name: str, author: str) -> Dict:
        """Get information about a specific tank"""
        for tank in self.data['rankings']:
            if tank['name'] == name and tank['author'] == author:
                return tank
        return {}

    def generate_badge_url(self, tank_name: str, tank_author: str) -> Dict[str, str]:
        """
        Generate shields.io badge URLs for a tank

        Returns dict with different badge types
        """
        tank = self.get_tank_info(tank_name, tank_author)
        if not tank:
            return {}

        base_url = "https://img.shields.io/badge"

        badges = {}

        # Rank badge
        rank = tank.get('rank', 0)
        if rank == 1:
            color = "gold"
        elif rank <= 3:
            color = "silver"
        elif rank <= 10:
            color = "brightgreen"
        else:
            color = "blue"

        badges['rank'] = f"{base_url}/rank-{rank}-{color}?style=for-the-badge&logo=trophy"

        # Win rate badge
        if tank['battles_fought'] > 0:
            win_rate = int((tank['wins'] / tank['battles_fought']) * 100)
            if win_rate >= 75:
                color = "brightgreen"
            elif win_rate >= 50:
                color = "yellow"
            else:
                color = "red"
            badges['winrate'] = f"{base_url}/wins-{win_rate}%25-{color}?style=for-the-badge"

        # Accuracy badge
        accuracy_pct = int(tank.get('accuracy', 0) * 100)
        if accuracy_pct >= 70:
            color = "brightgreen"
        elif accuracy_pct >= 50:
            color = "yellow"
        else:
            color = "red"
        badges['accuracy'] = f"{base_url}/accuracy-{accuracy_pct}%25-{color}?style=for-the-badge&logo=target"

        # Score badge
        score = tank.get('total_score', 0)
        badges['score'] = f"{base_url}/score-{score}-blue?style=for-the-badge&logo=star"

        # Achievement badge
        achievement = tank.get('badge', 'rookie')
        achievement_colors = {
            'rookie': 'lightgrey',
            'warrior': 'blue',
            'sharpshooter': 'orange',
            'survivor': 'green',
            'champion': 'gold',
            'undefeated': 'purple'
        }
        color = achievement_colors.get(achievement, 'lightgrey')
        badges['achievement'] = f"{base_url}/achievement-{achievement}-{color}?style=for-the-badge&logo=award"

        return badges

    def generate_leaderboard_markdown(self, top_n: int = 10) -> str:
        """Generate markdown for displaying the leaderboard"""
        md = "# 🏆 Leaderboard\n\n"
        md += f"*Last updated: {self.data['last_updated']}*\n\n"

        md += "| Rank | Tank | Author | Score | W/L/T | Accuracy | Badge |\n"
        md += "|------|------|--------|-------|-------|----------|-------|\n"

        for i, tank in enumerate(self.data['rankings'][:top_n], 1):
            # Medal emoji for top 3
            if i == 1:
                rank_display = "🥇"
            elif i == 2:
                rank_display = "🥈"
            elif i == 3:
                rank_display = "🥉"
            else:
                rank_display = str(i)

            name = tank['name']
            author = tank['author']
            score = tank['total_score']
            wlt = f"{tank['wins']}/{tank['losses']}/{tank['ties']}"
            accuracy = f"{int(tank['accuracy'] * 100)}%"

            # Badge emoji
            badge_emojis = {
                'rookie': '🔰',
                'warrior': '⚔️',
                'sharpshooter': '🎯',
                'survivor': '🛡️',
                'champion': '👑',
                'undefeated': '🏆'
            }
            badge = badge_emojis.get(tank.get('badge', 'rookie'), '🔰')

            md += f"| {rank_display} | {name} | {author} | {score} | {wlt} | {accuracy} | {badge} |\n"

        md += "\n## Badge Legend\n\n"
        md += "- 🔰 **Rookie**: First battle\n"
        md += "- ⚔️ **Warrior**: 10+ battles fought\n"
        md += "- 🎯 **Sharpshooter**: 60%+ accuracy\n"
        md += "- 🛡️ **Survivor**: 75%+ survival rate\n"
        md += "- 👑 **Champion**: #1 on leaderboard\n"
        md += "- 🏆 **Undefeated**: 5+ wins, 0 losses\n"

        return md

    def generate_tank_profile_markdown(self, tank_name: str, tank_author: str) -> str:
        """Generate a detailed markdown profile for a tank"""
        tank = self.get_tank_info(tank_name, tank_author)
        if not tank:
            return f"Tank {tank_name} by {tank_author} not found."

        badges = self.generate_badge_url(tank_name, tank_author)

        md = f"# {tank['name']} by {tank['author']}\n\n"

        # Display badges
        if badges:
            md += "## Badges\n\n"
            for badge_type, badge_url in badges.items():
                md += f"![{badge_type}]({badge_url}) "
            md += "\n\n"

        md += "## Statistics\n\n"
        md += f"- **Rank**: #{tank['rank']}\n"
        md += f"- **Total Score**: {tank['total_score']}\n"
        md += f"- **Battles**: {tank['battles_fought']}\n"
        md += f"- **Record**: {tank['wins']}W - {tank['losses']}L - {tank['ties']}T\n"
        md += f"- **Win Rate**: {int((tank['wins'] / tank['battles_fought']) * 100) if tank['battles_fought'] > 0 else 0}%\n"
        md += f"- **Accuracy**: {int(tank['accuracy'] * 100)}%\n"
        md += f"- **Survival Rate**: {int(tank['survival_rate'] * 100)}%\n"
        md += f"- **Avg Score/Battle**: {tank['avg_score_per_battle']:.1f}\n"

        if tank['achievements']:
            md += "\n## Achievements\n\n"
            for achievement in tank['achievements']:
                md += f"- {achievement}\n"

        return md


def main():
    """Example usage"""
    manager = LeaderboardManager()

    # Example: Add a new battle result
    example_tank = {
        'name': 'TestTank',
        'author': 'Student1',
        'file': 'Submissions/Student1/test_tank.py',
        'battle_results': {
            'won': True,
            'survived': True,
            'damage_dealt': 250,
            'damage_taken': 50,
            'shots_fired': 20,
            'shots_hit': 15
        }
    }

    manager.add_or_update_tank(example_tank)

    # Generate leaderboard
    print(manager.generate_leaderboard_markdown())

    # Generate tank profile
    print(manager.generate_tank_profile_markdown('TestTank', 'Student1'))

    # Get badge URLs
    badges = manager.generate_badge_url('TestTank', 'Student1')
    print("\nBadge URLs:")
    for badge_type, url in badges.items():
        print(f"{badge_type}: {url}")


if __name__ == "__main__":
    main()
