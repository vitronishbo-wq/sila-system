"""
Configuration migration script for SILA system.

Migrates existing modules to use the new centralized configuration system.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


class ConfigMigrator:
    """Migrates existing configuration usage to centralized settings."""

    def __init__(self, backend_path: str):
        """Initialize migrator with backend path."""
        self.backend_path = Path(backend_path)
        self.migration_log: List[Dict[str, Any]] = []

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the backend."""
        python_files = []
        for root, dirs, files in os.walk(self.backend_path):
            # Skip virtual environments and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'venv']

            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)

        return python_files

    def analyze_imports(self, file_path: Path) -> Dict[str, Any]:
        """Analyze configuration-related imports in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for old config imports
            old_imports = {
                'from config import settings
                'from config import settings
                'from config import settings': False,
                'from os import getenv': False,
                'os.getenv': False,
                'os.environ': False,
            }

            for pattern in old_imports:
                old_imports[pattern] = pattern in content

            # Look for direct environment access
            env_access_patterns = [
                r'os\.getenv\s*\(',
                r'os\.environ\s*\[',
                r'os\.environ\.get\s*\(',
            ]

            env_access_count = 0
            for pattern in env_access_patterns:
                env_access_count += len(re.findall(pattern, content))

            return {
                'file': str(file_path),
                'old_imports': old_imports,
                'env_access_count': env_access_count,
                'needs_migration': any(old_imports.values()) or env_access_count > 0
            }

        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e),
                'needs_migration': False
            }

    def migrate_file(self, file_path: Path, dry_run: bool = True) -> Dict[str, Any]:
        """Migrate a single file to use new configuration."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            content = original_content
            changes_made = []

            # Replace old imports
            import_replacements = {
                r'from core\.config import.*': 'from config import settings',
                r'from app\.core\.config import.*': 'from config import settings',
                r'import core\.config': 'from config import settings',
            }

            for pattern, replacement in import_replacements.items():
                try:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        changes_made.append(f"Import: {pattern} -> {replacement}")
                except re.error as e:
                    print(f"Warning: Import regex error in {file_path}: {e}")
                    continue

            # Replace direct os.getenv calls with settings
            env_replacements = {
                r'os\.getenv\s*\(\s*["\']([^"\']+)["\']\s*(?:,\s*["\']([^"\']*)["\'])?\s*\)': r'settings.\1',
                r'os\.environ\s*\[\s*["\']([^"\']+)["\']\s*\]': r'settings.\1',
                r'os\.environ\.get\s*\(\s*["\']([^"\']+)["\']\s*(?:,\s*["\']([^"\']*)["\'])?\s*\)': r'settings.\1',
            }

            for pattern, replacement in env_replacements.items():
                try:
                    matches = re.findall(pattern, content)
                    if matches:
                        content = re.sub(pattern, replacement, content)
                        changes_made.append(f"Environment access: {len(matches)} replacements")
                except re.error as e:
                    print(f"Warning: Environment regex error in {file_path}: {e}")
                    continue

            # Replace common config variable names
            variable_replacements = {
                r'config\.': 'settings.',
                r'settings_instance\.': 'settings.',
                r'app_settings\.': 'settings.',
            }

            for pattern, replacement in variable_replacements.items():
                try:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        changes_made.append(f"Variable: {pattern} -> {replacement}")
                except re.error as e:
                    print(f"Warning: Variable regex error in {file_path}: {e}")
                    continue

            # Write changes if not dry run
            if changes_made and not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            return {
                'file': str(file_path),
                'changes_made': changes_made,
                'migrated': len(changes_made) > 0
            }

        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e),
                'migrated': False
            }

    def migrate_all(self, dry_run: bool = True) -> Dict[str, Any]:
        """Migrate all Python files to use new configuration."""
        python_files = self.find_python_files()

        print(f"Found {len(python_files)} Python files to analyze...")

        # Analyze files
        analysis_results = []
        files_to_migrate = []

        for file_path in python_files:
            result = self.analyze_imports(file_path)
            analysis_results.append(result)

            if result.get('needs_migration', False):
                files_to_migrate.append(file_path)

        print(f"Found {len(files_to_migrate)} files that need migration")

        # Migrate files
        migration_results = []
        successful_migrations = 0

        for file_path in files_to_migrate:
            print(f"Migrating: {file_path}")
            result = self.migrate_file(file_path, dry_run)
            migration_results.append(result)

            if result.get('migrated', False):
                successful_migrations += 1
                changes_count = len(result.get('changes_made', []))
                print(f"  ✅ Migrated ({changes_count} changes)")
            else:
                error_msg = result.get('error', 'Unknown error')
                print(f"  ❌ Failed: {error_msg}")

        return {
            'total_files': len(python_files),
            'files_analyzed': len(analysis_results),
            'files_to_migrate': len(files_to_migrate),
            'successful_migrations': successful_migrations,
            'dry_run': dry_run,
            'analysis_results': analysis_results,
            'migration_results': migration_results
        }

    def create_migration_report(self, results: Dict[str, Any]) -> str:
        """Create a detailed migration report."""
        report = []
        report.append("=" * 80)
        report.append("SILA CONFIGURATION MIGRATION REPORT")
        report.append("=" * 80)

        report.append(f"\n📊 SUMMARY")
        report.append(f"Total Python files: {results['total_files']}")
        report.append(f"Files analyzed: {results['files_analyzed']}")
        report.append(f"Files needing migration: {results['files_to_migrate']}")
        report.append(f"Successful migrations: {results['successful_migrations']}")
        report.append(f"Dry run: {'Yes' if results['dry_run'] else 'No'}")

        if results['dry_run']:
            report.append(f"\n⚠️  THIS WAS A DRY RUN - NO FILES WERE MODIFIED")
            report.append(f"Run again with dry_run=False to apply changes")

        # Files that need migration
        files_needing_migration = [
            r for r in results['analysis_results']
            if r.get('needs_migration', False)
        ]

        if files_needing_migration:
            report.append(f"\n📋 FILES REQUIRING MIGRATION:")
            for result in files_needing_migration:
                report.append(f"  - {result['file']}")
                if 'old_imports' in result:
                    imports = [k for k, v in result['old_imports'].items() if v]
                    if imports:
                        report.append(f"    Old imports: {', '.join(imports)}")
                if result.get('env_access_count', 0) > 0:
                    report.append(f"    Environment access: {result['env_access_count']} calls")

        # Migration results
        if results['migration_results']:
            report.append(f"\n🔄 MIGRATION RESULTS:")
            for result in results['migration_results']:
                if result.get('migrated', False):
                    report.append(f"  ✅ {result['file']}")
                    for change in result.get('changes_made', []):
                        report.append(f"    - {change}")
                else:
                    report.append(f"  ❌ {result['file']}")
                    if 'error' in result:
                        report.append(f"    Error: {result['error']}")

        # Recommendations
        report.append(f"\n💡 RECOMMENDATIONS:")
        if results['files_to_migrate'] > 0:
            report.append(f"  - Review migrated files for any custom logic")
            report.append(f"  - Update imports to use specific config functions")
            report.append(f"  - Test migrated modules thoroughly")
        else:
            report.append(f"  - All files are already using the new configuration system")

        report.append(f"  - Update documentation to reflect new configuration structure")
        report.append(f"  - Remove old core.settings.py file after migration is complete")

        report.append("=" * 80)

        return "\n".join(report)

    def update_requirements(self) -> None:
        """Update requirements.txt to include pydantic-settings."""
        requirements_file = self.backend_path / "requirements.txt"

        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                content = f.read()

            if 'pydantic-settings' not in content:
                with open(requirements_file, 'a') as f:
                    f.write('\n# Configuration management\npydantic-settings>=2.0.0\n')
                print("✅ Added pydantic-settings to requirements.txt")
            else:
                print("ℹ️  pydantic-settings already in requirements.txt")
        else:
            print("⚠️  requirements.txt not found")


def main():
    """Main migration function."""
    import argparse

    parser = argparse.ArgumentParser(description="Migrate SILA configuration to centralized system")
    parser.add_argument(
        "--backend-path",
        default="/opt/sila-system/backend",
        help="Path to backend directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Perform dry run without making changes"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (disables dry run)"
    )
    parser.add_argument(
        "--update-requirements",
        action="store_true",
        help="Update requirements.txt with pydantic-settings"
    )

    args = parser.parse_args()

    # Override dry run if apply is specified
    dry_run = args.dry_run and not args.apply

    print("SILA Configuration Migration Tool")
    print("=" * 40)
    print(f"Backend path: {args.backend_path}")
    print(f"Dry run: {'Yes' if dry_run else 'No'}")
    print()

    # Initialize migrator
    migrator = ConfigMigrator(args.backend_path)

    # Update requirements if requested
    if args.update_requirements:
        migrator.update_requirements()
        print()

    # Run migration
    results = migrator.migrate_all(dry_run=dry_run)

    # Generate and print report
    report = migrator.create_migration_report(results)
    print(report)

    # Save report to file
    report_file = Path(args.backend_path) / "config_migration_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n📄 Detailed report saved to: {report_file}")

    # Exit with error code if migrations failed
    if results['files_to_migrate'] > 0 and results['successful_migrations'] < results['files_to_migrate']:
        sys.exit(1)


if __name__ == "__main__":
    main()
