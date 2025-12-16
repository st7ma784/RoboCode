# Contributing to Python Tank Wars

Thank you for your interest in contributing! This project is designed to help kids learn Python through fun tank battles.

## Ways to Contribute

### 1. Submit Your Tank (Students)

The primary way to participate! See [Submissions/README.md](Submissions/README.md) for instructions.

### 2. Improve Tutorials (Teachers/Contributors)

Help make the tutorials better:
- Fix typos or errors
- Add clearer explanations
- Create additional examples
- Improve code comments

### 3. Add Sample Tanks (Advanced Contributors)

Create new sample tanks with different strategies:
- New difficulty levels
- Interesting movement patterns
- Novel targeting strategies
- Educational value

### 4. Enhance Infrastructure (Developers)

Improve the project infrastructure:
- Better battle automation
- Video generation improvements
- Scoresheet enhancements
- Testing framework

## Submission Guidelines

### For Student Tank Submissions

1. **Fork** the repository
2. **Create** a folder in `Submissions/YourName/`
3. **Add** your tank .py file
4. **Test** locally first
5. **Create** a Pull Request
6. **Wait** for automated battle results

### For Tutorial Improvements

1. **Fork** the repository
2. **Make** your changes
3. **Test** that examples still work
4. **Document** what you changed
5. **Create** a Pull Request with clear description

### For Code Contributions

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Write** clean, commented code
4. **Test** your changes
5. **Commit** with clear messages
6. **Create** a Pull Request

## Code Style

### Python Code

```python
# Use descriptive names
def calculate_distance(x1, y1, x2, y2):
    """Calculate distance between two points"""
    # Add comments for complex logic
    x_diff = x2 - x1
    y_diff = y2 - y1
    return math.sqrt(x_diff**2 + y_diff**2)
```

### Guidelines

- Use 4 spaces for indentation
- Add docstrings to functions and classes
- Keep functions focused and simple
- Comment complex math or logic
- Use meaningful variable names
- Keep it beginner-friendly!

## Writing Tutorials

When creating or editing tutorials:

### Be Age-Appropriate
- Write for 8-year-olds
- Use simple language
- Provide lots of examples
- Break down complex concepts

### Be Encouraging
- Celebrate small wins
- Frame errors as learning opportunities
- Use positive language
- Make it fun!

### Be Clear
- One concept at a time
- Show, don't just tell
- Provide working code examples
- Explain WHY, not just WHAT

## Testing

Before submitting:

### For Tanks
```bash
# Make sure your tank has no syntax errors
python your_tank.py

# Test against sample tanks
python battle_runner.py your_tank.py Samples/sitting_duck.py
```

### For Tutorials
- Run all code examples
- Check for typos
- Verify links work
- Test on fresh environment

## Pull Request Process

1. **Title**: Clear and descriptive
   - Good: "Add Week 3 boundary checking exercises"
   - Bad: "Update"

2. **Description**: Explain what and why
   ```markdown
   ## Changes
   - Added 5 new practice problems to Week 3
   - Fixed typo in trigonometry guide
   - Improved example in circular movement

   ## Testing
   - Ran all code examples
   - Verified math accuracy
   - Tested with beginner students
   ```

3. **Small PRs**: One feature/fix at a time
4. **Be Patient**: Reviews may take a few days
5. **Be Responsive**: Address review feedback

## Community Guidelines

### Be Respectful
- Welcome beginners
- Constructive feedback only
- Encourage learning
- Celebrate diversity

### Be Helpful
- Answer questions
- Share knowledge
- Mentor others
- Stay positive

### Be Original
- Don't plagiarize
- Credit sources
- Respect licenses
- Create new content

## Getting Help

- **Questions**: Open a GitHub Issue
- **Bugs**: Open a GitHub Issue with details
- **Ideas**: Start a GitHub Discussion
- **Urgent**: Contact maintainers

## Recognition

Contributors will be:
- Listed in README
- Credited in commits
- Featured in releases
- Thanked by the community!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for making Python Tank Wars better! 🎮🚀

Every contribution, no matter how small, helps kids learn to code!
