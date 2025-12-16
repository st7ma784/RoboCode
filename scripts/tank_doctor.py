"""
Tank Doctor - Interactive Debugging Assistant for Kids

This script helps young programmers diagnose and fix issues with their tanks.
It checks for common problems and provides step-by-step guidance.

Usage:
    python tank_doctor.py your_tank.py
"""

import sys
import ast
import os
from pathlib import Path
from typing import List, Dict, Tuple

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class TankDoctor:
    """
    Analyzes tank code and provides helpful feedback
    """

    def __init__(self, tank_file: str):
        self.tank_file = Path(tank_file)
        self.issues = []
        self.warnings = []
        self.suggestions = []
        self.content = ""

    def examine(self):
        """Run all checks on the tank"""
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════╗")
        print("║           🏥 TANK DOCTOR IS CHECKING...              ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}\n")

        # Check if file exists
        if not self.tank_file.exists():
            print(f"{Colors.RED}✗ File not found: {self.tank_file}{Colors.ENDC}")
            print(f"{Colors.YELLOW}Make sure the file path is correct!{Colors.ENDC}")
            return False

        print(f"{Colors.CYAN}📋 Patient: {self.tank_file.name}{Colors.ENDC}\n")

        # Read the file
        try:
            with open(self.tank_file, 'r') as f:
                self.content = f.read()
        except Exception as e:
            print(f"{Colors.RED}✗ Could not read file: {e}{Colors.ENDC}")
            return False

        # Run checks
        self.check_file_basics()
        self.check_syntax()
        self.check_class_structure()
        self.check_required_methods()
        self.check_common_mistakes()
        self.check_indentation_consistency()
        self.check_imports()

        # Show results
        self.show_diagnosis()

        return len(self.issues) == 0

    def check_file_basics(self):
        """Check basic file properties"""
        print(f"{Colors.BLUE}🔍 Checking file basics...{Colors.ENDC}")

        # Check if file is empty
        if not self.content.strip():
            self.issues.append("Your file is empty! Add some code to create your tank.")
            return

        # Check file size
        lines = self.content.split('\n')
        print(f"   File has {len(lines)} lines")

        if len(lines) < 10:
            self.warnings.append(
                f"Your file only has {len(lines)} lines. Most tanks need at least 15-20 lines."
            )

        print(f"{Colors.GREEN}   ✓ File basics OK{Colors.ENDC}\n")

    def check_syntax(self):
        """Check for Python syntax errors"""
        print(f"{Colors.BLUE}🔍 Checking Python syntax...{Colors.ENDC}")

        try:
            ast.parse(self.content)
            print(f"{Colors.GREEN}   ✓ No syntax errors found!{Colors.ENDC}\n")
        except SyntaxError as e:
            self.issues.append(
                f"Syntax error on line {e.lineno}: {e.msg}\n"
                f"   Problem: {e.text.strip() if e.text else 'Unknown'}\n"
                f"   Tip: Check for missing colons (:) or parentheses ()"
            )
            print(f"{Colors.RED}   ✗ Found syntax error{Colors.ENDC}\n")
        except IndentationError as e:
            self.issues.append(
                f"Indentation error on line {e.lineno}\n"
                f"   Tip: Make sure you use consistent spacing (Tab or 4 spaces)"
            )
            print(f"{Colors.RED}   ✗ Found indentation error{Colors.ENDC}\n")

    def check_class_structure(self):
        """Check if there's a proper tank class"""
        print(f"{Colors.BLUE}🔍 Checking tank class...{Colors.ENDC}")

        # Look for class definition
        if 'class ' not in self.content:
            self.issues.append(
                "No class found! Your tank needs a class definition.\n"
                "   Example:\n"
                "   class MyTank:\n"
                "       def __init__(self):\n"
                "           self.name = 'MyTank'"
            )
            print(f"{Colors.RED}   ✗ No class found{Colors.ENDC}\n")
            return

        # Check for __init__ method
        if 'def __init__' not in self.content:
            self.warnings.append(
                "No __init__ method found. While not required, it's good practice!\n"
                "   Example:\n"
                "   def __init__(self):\n"
                "       self.name = 'MyTank'"
            )
            print(f"{Colors.YELLOW}   ⚠ No __init__ method{Colors.ENDC}\n")
        else:
            print(f"{Colors.GREEN}   ✓ Class structure looks good!{Colors.ENDC}\n")

    def check_required_methods(self):
        """Check for required tank methods"""
        print(f"{Colors.BLUE}🔍 Checking required methods...{Colors.ENDC}")

        required = {
            'run': 'Main loop - this is where your tank\'s brain goes!',
        }

        recommended = {
            'on_scanned_bot': 'Called when you see an enemy - shoot here!',
            'on_hit_by_bullet': 'Called when you get hit - dodge here!',
        }

        # Check required
        missing_required = []
        for method, description in required.items():
            if f'def {method}' not in self.content:
                missing_required.append(f"   • {method}(): {description}")

        if missing_required:
            self.issues.append(
                "Missing required methods:\n" + "\n".join(missing_required)
            )
            print(f"{Colors.RED}   ✗ Missing required methods{Colors.ENDC}\n")
        else:
            print(f"{Colors.GREEN}   ✓ Required methods found!{Colors.ENDC}")

        # Check recommended
        missing_recommended = []
        for method, description in recommended.items():
            if f'def {method}' not in self.content:
                missing_recommended.append(f"   • {method}(): {description}")

        if missing_recommended:
            self.warnings.append(
                "Recommended methods not found (your tank will still work):\n" +
                "\n".join(missing_recommended)
            )
            print(f"{Colors.YELLOW}   ⚠ Some recommended methods missing{Colors.ENDC}\n")
        else:
            print(f"{Colors.GREEN}   ✓ All recommended methods found!{Colors.ENDC}\n")

    def check_common_mistakes(self):
        """Check for common beginner mistakes"""
        print(f"{Colors.BLUE}🔍 Checking for common mistakes...{Colors.ENDC}")

        found_issues = []

        # Check for missing 'self'
        methods = ['ahead', 'back', 'turn_right', 'turn_left', 'fire', 'turn_gun_to']
        for method in methods:
            # Look for method call without 'self.'
            if f'{method}(' in self.content and f'self.{method}(' not in self.content:
                found_issues.append(
                    f"Found '{method}()' - should this be 'self.{method}()'?"
                )

        # Check for common typos
        typos = {
            'selff': 'self',
            'slf': 'self',
            'sell': 'self',
            'def run' : 'def run(self):',
        }

        for typo, correct in typos.items():
            if typo in self.content.lower():
                found_issues.append(
                    f"Possible typo: '{typo}' - did you mean '{correct}'?"
                )

        # Check for assignment in if statements
        if ' = ' in self.content and 'if ' in self.content:
            lines = self.content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'if ' in line and ' = ' in line and ' == ' not in line:
                    found_issues.append(
                        f"Line {i}: Did you mean '==' instead of '=' in an if statement?"
                    )

        if found_issues:
            self.warnings.extend(found_issues)
            print(f"{Colors.YELLOW}   ⚠ Found {len(found_issues)} potential issues{Colors.ENDC}\n")
        else:
            print(f"{Colors.GREEN}   ✓ No common mistakes found!{Colors.ENDC}\n")

    def check_indentation_consistency(self):
        """Check if indentation is consistent"""
        print(f"{Colors.BLUE}🔍 Checking indentation...{Colors.ENDC}")

        lines = self.content.split('\n')
        uses_tabs = False
        uses_spaces = False

        for line in lines:
            if line.startswith('\t'):
                uses_tabs = True
            elif line.startswith('    '):
                uses_spaces = True

        if uses_tabs and uses_spaces:
            self.warnings.append(
                "Your file mixes tabs and spaces for indentation!\n"
                "   Tip: Pick one (spaces are recommended) and stick with it."
            )
            print(f"{Colors.YELLOW}   ⚠ Mixed tabs and spaces{Colors.ENDC}\n")
        else:
            print(f"{Colors.GREEN}   ✓ Indentation is consistent!{Colors.ENDC}\n")

    def check_imports(self):
        """Check for necessary imports"""
        print(f"{Colors.BLUE}🔍 Checking imports...{Colors.ENDC}")

        recommended_imports = {
            'math': 'Needed for trigonometry (sin, cos, sqrt, atan2)',
            'random': 'Needed for unpredictable movement',
        }

        missing = []
        for module, reason in recommended_imports.items():
            if f'import {module}' not in self.content:
                # Check if they use functions from this module
                if module == 'math' and any(f in self.content for f in ['sqrt', 'sin', 'cos', 'atan2']):
                    self.issues.append(
                        f"You're using math functions but haven't imported math!\n"
                        f"   Add at the top: import math"
                    )
                elif module == 'random' and 'random.' in self.content:
                    self.issues.append(
                        f"You're using random but haven't imported it!\n"
                        f"   Add at the top: import random"
                    )
                else:
                    missing.append(f"   • import {module}  # {reason}")

        if missing:
            self.suggestions.append(
                "Consider adding these imports (if you need them):\n" + "\n".join(missing)
            )
            print(f"{Colors.CYAN}   ℹ Some useful imports not found{Colors.ENDC}\n")
        else:
            print(f"{Colors.GREEN}   ✓ Imports look good!{Colors.ENDC}\n")

    def show_diagnosis(self):
        """Show the final diagnosis"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════╗")
        print("║                  📋 DIAGNOSIS                        ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}\n")

        # Show issues (must fix)
        if self.issues:
            print(f"{Colors.RED}{Colors.BOLD}🚨 CRITICAL ISSUES (Must Fix):{Colors.ENDC}")
            for i, issue in enumerate(self.issues, 1):
                print(f"\n{Colors.RED}{i}. {issue}{Colors.ENDC}")
            print()
        else:
            print(f"{Colors.GREEN}✓ No critical issues found!{Colors.ENDC}\n")

        # Show warnings (should fix)
        if self.warnings:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  WARNINGS (Should Fix):{Colors.ENDC}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"\n{Colors.YELLOW}{i}. {warning}{Colors.ENDC}")
            print()

        # Show suggestions (nice to have)
        if self.suggestions:
            print(f"{Colors.CYAN}{Colors.BOLD}💡 SUGGESTIONS (Nice to Have):{Colors.ENDC}")
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"\n{Colors.CYAN}{i}. {suggestion}{Colors.ENDC}")
            print()

        # Final verdict
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════╗")

        if not self.issues:
            print("║              ✅ TANK IS HEALTHY!                    ║")
            print("╚══════════════════════════════════════════════════════╝")
            print(f"{Colors.ENDC}\n")
            print(f"{Colors.GREEN}Your tank is ready to battle! 🎮{Colors.ENDC}\n")

            if self.warnings:
                print(f"{Colors.YELLOW}Fix the warnings to make your tank even better!{Colors.ENDC}\n")
        else:
            print("║           🏥 TANK NEEDS TREATMENT                   ║")
            print("╚══════════════════════════════════════════════════════╝")
            print(f"{Colors.ENDC}\n")
            print(f"{Colors.RED}Fix the critical issues above, then run Tank Doctor again!{Colors.ENDC}\n")

        # Encouragement
        print(f"{Colors.CYAN}Remember: Every bug you fix makes you a better programmer! 💪{Colors.ENDC}\n")


def main():
    if len(sys.argv) < 2:
        print(f"{Colors.RED}Usage: python tank_doctor.py your_tank.py{Colors.ENDC}")
        sys.exit(1)

    tank_file = sys.argv[1]
    doctor = TankDoctor(tank_file)
    success = doctor.examine()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
