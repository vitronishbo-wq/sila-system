#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Legacy Script Deprecation Wrapper for Code Quality Tools

This script provides backward compatibility for deprecated code quality and fixing scripts.
It redirects calls to the new automated pre-commit hook system.

DEPRECATED: Use pre-commit hooks instead of manual scripts
"""

import sys
import os
from pathlib import Path

def main():
    """Main entry point for deprecated scripts."""
    script_name = Path(sys.argv[0]).name

    print("⚠️  DEPRECATED SCRIPT WARNING"    print(f"   The script '{script_name}' has been deprecated.")
    print("   Code quality and formatting is now handled automatically by pre-commit hooks.")
    print()
    print("   🔧 NEW AUTOMATED SYSTEM:"    print("   All formatting and linting now runs automatically before commits.")
    print()
    print("   📋 SETUP:"    print("   # Install pre-commit hooks")
    print("   pip install pre-commit")
    print("   pre-commit install")
    print()
    print("   # Frontend setup")
    print("   cd frontend && npm install && npm run prepare")
    print()
    print("   📖 COMMANDS:"    print("   # Run all quality checks")
    print("   pre-commit run --all-files")
    print()
    print("   # Frontend checks")
    print("   cd frontend && npm run lint && npm run format:check")
    print()
    print("   # Backend checks")
    print("   black . && isort . && flake8 . && bandit -r .")
    print()
    print("   📚 See 'DEVELOPER_ONBOARDING_QUALITY.md' for complete documentation")
    print()

    # Map old script names to new commands
    command_map = {
        'auto_fix_syntax.py': 'pre-commit run --all-files',
        'fix_missing_imports.py': 'pre-commit run mypy --all-files',
        'scan_and_fix_imports.py': 'pre-commit run mypy --all-files',
        'corrigir_erros_sintaxe_batch.py': 'pre-commit run --all-files',
        'fix_pydantic_v2_config.py': 'pre-commit run --all-files',
        'fix_sqlalchemy_declarative_imports.py': 'pre-commit run --all-files',
        'auto_heal_imports.py': 'pre-commit run mypy --all-files'
    }

    if script_name in command_map:
        new_command = command_map[script_name]
        print(f"   💡 For '{script_name}', run: {new_command}")
    else:
        print("   💡 Use 'pre-commit run --all-files' for comprehensive quality checks")

    print()
    print("   🔄 This script will be removed in a future version.")
    print("   Please update your automation scripts and documentation.")

    # Ask if user wants to run the new command
    try:
        response = input("   ❓ Would you like to run the new automated check now? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            if 'frontend' in script_name.lower() or 'lint' in script_name.lower():
                print("   🚀 Running frontend quality checks...")
                os.system("cd frontend && npm run lint && npm run format:check")
            else:
                print("   🚀 Running backend quality checks...")
                os.system("pre-commit run --all-files")
    except KeyboardInterrupt:
        print("\n   ❌ Operation cancelled.")

    sys.exit(1)

if __name__ == "__main__":
    main()
