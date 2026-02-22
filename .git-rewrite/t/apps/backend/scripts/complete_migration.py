#!/usr/bin/env python3
"""
Complete Configuration Migration Script

This script completes the migration to the new centralized configuration system.
It migrates all remaining files and provides a final validation report.

Usage:
    python scripts/complete_migration.py [--force] [--validate-only]

Exit Codes:
    0: Success - Migration completed
    1: Warning - Completed with warnings
    2: Error - Migration failed
    3: Fatal - System errors
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

try:
    from config.migrate_config import ConfigMigrator
    from config import settings, validate_configuration
    from scripts.validate_config import CIConfigValidator
except ImportError as e:
    print(f"❌ FATAL: Cannot import configuration system: {e}")
    sys.exit(3)


class CompleteMigration:
    """Complete migration orchestrator."""

    def __init__(self, force: bool = False, validate_only: bool = False):
        """Initialize migration orchestrator."""
        self.force = force
        self.validate_only = validate_only
        self.migrator = ConfigMigrator(str(backend_path))
        self.results = {
            "migration_completed": False,
            "files_migrated": 0,
            "files_failed": 0,
            "validation_passed": False,
            "errors": [],
            "warnings": [],
        }

    def run_complete_migration(self) -> Dict[str, Any]:
        """Run complete migration process."""
        print("🚀 SILA Complete Configuration Migration")
        print("=" * 60)

        if self.validate_only:
            print("🔍 VALIDATION ONLY MODE")
            print("=" * 60)
            return self._validate_only()

        # Step 1: Analyze current state
        print("\n📊 STEP 1: Analyzing Current State")
        print("-" * 40)
        self._analyze_current_state()

        # Step 2: Perform migration
        print("\n🔄 STEP 2: Performing Migration")
        print("-" * 40)
        self._perform_migration()

        # Step 3: Validate results
        print("\n✅ STEP 3: Validating Results")
        print("-" * 40)
        self._validate_results()

        # Step 4: Generate final report
        print("\n📋 STEP 4: Final Report")
        print("-" * 40)
        self._generate_final_report()

        return self.results

    def _validate_only(self) -> Dict[str, Any]:
        """Run validation only."""
        try:
            # Validate configuration
            validator = CIConfigValidator(environment=settings.ENVIRONMENT)
            validation_results = validator.validate_all()

            self.results["validation_passed"] = validation_results["valid"]
            self.results["errors"] = validation_results["errors"]
            self.results["warnings"] = validation_results["warnings"]

            if validation_results["valid"]:
                print("✅ Configuration is valid")
                self.results["migration_completed"] = True
            else:
                print("❌ Configuration has errors")

            return self.results

        except Exception as e:
            error_msg = f"Validation failed: {e}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)
            return self.results

    def _analyze_current_state(self):
        """Analyze current migration state."""
        try:
            python_files = self.migrator.find_python_files()
            files_to_migrate = []

            for file_path in python_files:
                result = self.migrator.analyze_imports(file_path)
                if result.get("needs_migration", False):
                    files_to_migrate.append(file_path)

            print(f"📁 Total Python files: {len(python_files)}")
            print(f"🔄 Files needing migration: {len(files_to_migrate)}")

            # Show categories
            categories = self._categorize_files(files_to_migrate)
            for category, files in categories.items():
                if files:
                    print(f"  - {category}: {len(files)} files")

            self.results["total_files"] = len(python_files)
            self.results["files_to_migrate"] = len(files_to_migrate)

        except Exception as e:
            error_msg = f"Analysis failed: {e}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)

    def _categorize_files(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Categorize files by type."""
        categories = {
            "Core modules": [],
            "Auth modules": [],
            "API endpoints": [],
            "Database related": [],
            "Scripts": [],
            "Tests": [],
            "Configuration": [],
            "Other": [],
        }

        for file_path in files:
            path_str = str(file_path)

            if "core/" in path_str:
                categories["Core modules"].append(file_path)
            elif "auth/" in path_str:
                categories["Auth modules"].append(file_path)
            elif "endpoints.py" in path_str or "routes.py" in path_str:
                categories["API endpoints"].append(file_path)
            elif "database" in path_str or "db" in path_str:
                categories["Database related"].append(file_path)
            elif "scripts/" in path_str:
                categories["Scripts"].append(file_path)
            elif "tests/" in path_str or "test_" in path_str:
                categories["Tests"].append(file_path)
            elif "config" in path_str:
                categories["Configuration"].append(file_path)
            else:
                categories["Other"].append(file_path)

        return categories

    def _perform_migration(self):
        """Perform the actual migration."""
        if self.validate_only:
            return

        try:
            # Run migration
            migration_results = self.migrator.migrate_all(dry_run=False)

            self.results["files_migrated"] = migration_results["successful_migrations"]
            self.results["files_failed"] = (
                migration_results["files_to_migrate"]
                - migration_results["successful_migrations"]
            )

            print(
                f"✅ Successfully migrated: {migration_results['successful_migrations']} files"
            )

            if self.results["files_failed"] > 0:
                print(f"❌ Failed migrations: {self.results['files_failed']} files")

                # Show failed files
                failed_files = [
                    r
                    for r in migration_results["migration_results"]
                    if not r.get("migrated", False)
                ]
                for result in failed_files[:5]:  # Show first 5
                    print(
                        f"  - {result.get('file', 'Unknown')}: {result.get('error', 'Unknown error')}"
                    )

                if len(failed_files) > 5:
                    print(f"  ... and {len(failed_files) - 5} more failures")

            # Check if migration was successful enough
            if self.results["files_failed"] == 0:
                print("🎉 All files migrated successfully!")
                self.results["migration_completed"] = True
            elif self.force:
                print("⚠️  Migration completed with some failures (force mode)")
                self.results["migration_completed"] = True
            else:
                print(
                    "❌ Migration incomplete. Use --force to continue despite failures."
                )
                self.results["migration_completed"] = False

        except Exception as e:
            error_msg = f"Migration failed: {e}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)

    def _validate_results(self):
        """Validate migration results."""
        try:
            # Validate configuration
            is_valid, errors, warnings = validate_configuration()

            self.results["validation_passed"] = is_valid
            self.results["errors"].extend(errors)
            self.results["warnings"].extend(warnings)

            if is_valid:
                print("✅ Configuration validation passed")
            else:
                print("❌ Configuration validation failed")
                for error in errors:
                    print(f"  - {error}")

            # Test imports of key modules
            self._test_key_imports()

        except Exception as e:
            error_msg = f"Validation failed: {e}"
            print(f"❌ {error_msg}")
            self.results["errors"].append(error_msg)

    def _test_key_imports(self):
        """Test imports of key migrated modules."""
        key_modules = [
            "main",
            "app",
            "core.database",
            "core.health",
            "modules.auth.endpoints",
            "modules.auth.auth_utils",
        ]

        failed_imports = []

        for module_name in key_modules:
            try:
                __import__(module_name)
                print(f"✅ {module_name}: Import successful")
            except Exception as e:
                print(f"❌ {module_name}: {e}")
                failed_imports.append(module_name)

        if failed_imports:
            error_msg = f"Failed imports: {', '.join(failed_imports)}"
            self.results["errors"].append(error_msg)

    def _generate_final_report(self):
        """Generate final migration report."""
        print("\n" + "=" * 60)
        print("📊 MIGRATION FINAL REPORT")
        print("=" * 60)

        # Migration status
        if self.results["migration_completed"]:
            print("✅ Migration Status: COMPLETED")
        else:
            print("❌ Migration Status: INCOMPLETE")

        # Statistics
        print(f"\n📈 Statistics:")
        print(f"  - Files migrated: {self.results['files_migrated']}")
        print(f"  - Files failed: {self.results['files_failed']}")

        # Validation status
        if self.results["validation_passed"]:
            print("✅ Validation Status: PASSED")
        else:
            print("❌ Validation Status: FAILED")

        # Errors and warnings
        if self.results["errors"]:
            print(f"\n🚨 Errors ({len(self.results['errors'])}):")
            for error in self.results["errors"][:5]:
                print(f"  - {error}")
            if len(self.results["errors"]) > 5:
                print(f"  ... and {len(self.results['errors']) - 5} more errors")

        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"][:3]:
                print(f"  - {warning}")
            if len(self.results["warnings"]) > 3:
                print(f"  ... and {len(self.results['warnings']) - 3} more warnings")

        # Next steps
        print(f"\n📋 Next Steps:")
        if self.results["migration_completed"] and self.results["validation_passed"]:
            print("  ✅ Migration completed successfully!")
            print("  🧪 Run your application tests")
            print("  🗑️  Remove old configuration files after verification")
            print("  📚 Update documentation")
        else:
            print("  🔧 Fix remaining migration issues")
            print("  🔄 Re-run migration with --force if needed")
            print("  🔍 Check error logs above")

        # Save report
        self._save_report()

    def _save_report(self):
        """Save migration report to file."""
        try:
            report_path = "complete_migration_report.json"
            with open(report_path, "w") as f:
                json.dump(self.results, f, indent=2, default=str)
            print(f"\n📄 Detailed report saved to: {report_path}")
        except Exception as e:
            print(f"⚠️  Could not save report: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Complete SILA configuration migration"
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force completion despite some failures",
    )
    parser.add_argument(
        "--validate-only",
        "-v",
        action="store_true",
        help="Only validate current configuration",
    )

    args = parser.parse_args()

    try:
        # Run complete migration
        cm = CompleteMigration(force=args.force, validate_only=args.validate_only)
        results = cm.run_complete_migration()

        # Determine exit code
        if results["migration_completed"] and results["validation_passed"]:
            exit_code = 0  # Success
        elif results["errors"]:
            exit_code = 2  # Error
        else:
            exit_code = 1  # Warning

        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n❌ Migration interrupted by user")
        sys.exit(3)
    except Exception as e:
        print(f"❌ FATAL: System error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()
