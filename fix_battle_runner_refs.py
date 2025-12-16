#!/usr/bin/env python3
"""
Script to replace battle_runner references with GUI instructions in all tutorial READMEs
"""
import re
from pathlib import Path

# Find all tutorial READMEs
tutorial_readmes = list(Path("Tutorials").glob("Week*/README.md"))

for readme_path in tutorial_readmes:
    print(f"Processing: {readme_path}")
    
    content = readme_path.read_text()
    original_content = content
    
    # Replace battle_runner commands with GUI instructions
    # Pattern 1: Simple battle_runner commands
    content = re.sub(
        r'```bash\npython battle_runner\.py (.+?)\n```',
        r'''```bash
# Start RoboCode GUI, then run your tank:
python \1
```

Add opponents in separate terminals, then click "Start Battle" in the GUI!''',
        content
    )
    
    # Pattern 2: battle_runner mentions in text
    content = content.replace(
        'battle_runner.py',
        'the RoboCode GUI arena'
    )
    
    content = content.replace(
        'battle_runner',
        'GUI arena'
    )
    
    # Pattern 3: scripts/battle_runner
    content = content.replace(
        'scripts/battle_runner',
        'the GUI arena'
    )
    
    if content != original_content:
        readme_path.write_text(content)
        print(f"  ✅ Updated {readme_path}")
    else:
        print(f"  ⏭️  No changes needed")

print("\n✨ Done!")
