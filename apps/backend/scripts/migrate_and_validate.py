#!/usr/bin/env python3
"""
Automated Migration and Validation Script for CI/CD

This script combines configuration migration and validation for the CI/CD pipeline.
It automatically migrates old configuration patterns and validates the new system.

Usage:
    python scripts/migrate_and_validate.py [--dry-run] [--environment ENV] [--strict]

Exit Codes:
    0: Success - Migration and validation completed
    1: Warning - Completed with warnings
    2: Error - Migration or validation failed
    3: Fatal - System errors
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

try:
    from config.migrate_config import ConfigMigrator
    from config import settings, validate_configuration, get_config_manager
except ImportError as e:
    print(f"❌ FATAL: Cannot import configuration system: {e}")
    sys.exit(3)


class MigrationValidator:
    """Combined migration and validation for CI/CD."""

    def __init__(
        self, dry_run: bool = False, environment: str = None, strict: bool = False
    ):
        """Initialize migration validator."""
        self.dry_run = dry_run
        self.environment = environment or settings.ENVIRONMENT
        self.strict = strict
        self.migrator = ConfigMigrator(str(backend_path))
        self.results = {
            "migration": {
                "total_files": 0,
                "files_to_migrate": 0,
                "successful_migrations": 0,
                "failed_migrations": 0,
                "migration_details": [],
            },
            "validation": {
                "valid": False,
                "errors": [],
                "warnings": [],
                "total_errors": 0,
                "total_warnings": 0,
            },
            "summary": {"success": False, "exit_code": 0},
        }

    def run_migration_and_validation(self) -> Dict[str, Any]:
        """Run complete migration and validation process."""
        print("🔄 SILA Configuration Migration & Validation")
        print("=" * 60)
        print(f"Environment: {self.environment}")
        print(f"Dry Run: {self.dry_run}")
        print(f"Strict Mode: {self.strict}")
        print("=" * 60)

        # Step 1: Run migration
        print("\n📦 STEP 1: Configuration Migration")
        print("-" * 40)
        self._run_migration()

        # Step 2: Run validation
        print("\n🔍 STEP 2: Configuration Validation")
        print("-" * 40)
        self._run_validation()

        # Step 3: Generate summary
        print("\n📊 STEP 3: Results Summary")
        print("-" * 40)
        self._generate_summary()

        return self.results

    def _run_migration(self):
        """Run configuration migration."""
        try:
            migration_results = self.migrator.migrate_all(dry_run=self.dry_run)

            self.results["migration"] = {
                "total_files": migration_results["total_files"],
                "files_to_migrate": migration_results["files_to_migrate"],
                "successful_migrations": migration_results["successful_migrations"],
                "failed_migrations": len(migration_results["migration_results"])
                - migration_results["successful_migrations"],
                "migration_details": migration_results["migration_results"],
            }

            print(f"📁 Total files analyzed: {migration_results['total_files']}")
            print(
                f"🔄 Files needing migration: {migration_results['files_to_migrate']}"
            )
            print(
                f"✅ Successful migrations: {migration_results['successful_migrations']}"
            )
            print(
                f"❌ Failed migrations: {self.results['migration']['failed_migrations']}"
            )

            # Show migration details for failed files
            failed_migrations = [
                r
                for r in migration_results["migration_results"]
                if not r.get("migrated", False)
            ]
            if failed_migrations:
                print(f"\n❌ Migration Failures:")
                for result in failed_migrations[:5]:  # Show first 5 failures
                    error = result.get("error", "Unknown error")
                    file_path = result.get("file", "Unknown file")
                    print(f"  - {file_path}: {error}")

                if len(failed_migrations) > 5:
                    print(f"  ... and {len(failed_migrations) - 5} more failures")

        except Exception as e:
            error_msg = f"Migration failed: {e}"
            print(f"❌ {error_msg}")
            self.results["migration"]["error"] = error_msg

    def _run_validation(self):
        """Run configuration validation."""
        try:
            # Import validation script
            from scripts.validate_config import CIConfigValidator

            validator = CIConfigValidator(
                environment=self.environment, strict_mode=self.strict
            )

            validation_results = validator.validate_all()

            self.results["validation"] = {
                "valid": validation_results["valid"],
                "errors": validation_results["errors"],
                "warnings": validation_results["warnings"],
                "total_errors": validation_results["total_errors"],
                "total_warnings": validation_results["total_warnings"],
            }

        except Exception as e:
            error_msg = f"Validation failed: {e}"
            print(f"❌ {error_msg}")
            self.results["validation"]["error"] = error_msg

    def _generate_summary(self):
        """Generate final summary and determine exit code."""
        migration = self.results["migration"]
        validation = self.results["validation"]

        # Determine success
        migration_success = migration.get("failed_migrations", 0) == 0
        validation_success = validation.get("valid", False)

        overall_success = migration_success and validation_success

        # Determine exit code
        if not overall_success:
            if (
                validation.get("total_errors", 0) > 0
                or migration.get("failed_migrations", 0) > 0
            ):
                exit_code = 2  # Error
            else:
                exit_code = 1  # Warning
        elif validation.get("total_warnings", 0) > 0 and self.strict:
            exit_code = 1  # Warning in strict mode
        else:
            exit_code = 0  # Success

        self.results["summary"] = {
            "success": overall_success,
            "exit_code": exit_code,
            "migration_success": migration_success,
            "validation_success": validation_success,
        }

        # Print summary
        print(f"Migration Status: {'✅ SUCCESS' if migration_success else '❌ FAILED'}")
        print(
            f"Validation Status: {'✅ SUCCESS' if validation_success else '❌ FAILED'}"
        )
        print(f"Overall Status: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")
        print(f"Exit Code: {exit_code}")

        if exit_code == 0:
            print("\n🎉 Migration and validation completed successfully!")
        elif exit_code == 1:
            print("\n⚠️  Migration and validation completed with warnings")
        else:
            print("\n❌ Migration and validation failed!")

    def save_report(self, output_path: str = None):
        """Save detailed report to file."""
        if not output_path:
            output_path = f"migration_validation_report_{self.environment}.json"

        try:
            with open(output_path, "w") as f:
                json.dump(self.results, f, indent=2, default=str)
            print(f"\n📄 Detailed report saved to: {output_path}")
        except Exception as e:
            print(f"⚠️  Could not save report: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate and validate SILA configuration"
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Run migration in dry-run mode (no changes applied)",
    )
    parser.add_argument("--environment", "-e", help="Target environment")
    parser.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="Enable strict mode (warnings become errors)",
    )
    parser.add_argument("--output", "-o", help="Output report file path")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Quiet mode (minimal output)"
    )

    args = parser.parse_args()

    try:
        # Run migration and validation
        mv = MigrationValidator(
            dry_run=args.dry_run, environment=args.environment, strict=args.strict
        )

        results = mv.run_migration_and_validation()

        # Save report if requested
        if args.output:
            mv.save_report(args.output)

        # Exit with appropriate code
        sys.exit(results["summary"]["exit_code"])

    except KeyboardInterrupt:
        print("\n❌ Process interrupted by user")
        sys.exit(3)
    except Exception as e:
        print(f"❌ FATAL: System error: {e}")
        if not args.quiet:
            import traceback

            traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()
