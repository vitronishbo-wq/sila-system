#!/usr/bin/env python3
"""
Automated code fixes for common Python issues in the SILA system.
Integrates with existing tools like isort, black, and autoflake.
"""

import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("autofix")


class CodeAutoFixer:
    """Automatically fix common code issues in Python files."""

    def __init__(self, root_dir: str = None, check_mode: bool = False):
        self.root_dir = Path(root_dir or os.getcwd()).resolve()
        self.fixes_applied = 0
        self.files_processed = 0
        self.check_mode = check_mode
        self.ignored_dirs = {
            "__pycache__",
            ".git",
            "venv",
            "env",
            ".mypy_cache",
            ".pytest_cache",
        }
        self.issues_found = {
            "imports": 0,
            "formatting": 0,
            "exceptions": 0,
            "type_hints": 0,
            "pydantic": 0,
        }

    def run_command(self, cmd: str, cwd: str = None) -> tuple[bool, str]:
        """Run a shell command and return success status and output."""
        try:
            logger.debug(f"Running: {cmd}")
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or self.root_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr.strip()}")
                return False, result.stderr.strip()
            return True, result.stdout.strip()
        except Exception as e:
            logger.error(f"Error running command: {e}")
            return False, str(e)

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if a file should be skipped based on path patterns."""
        # Skip files in ignored directories
        for part in file_path.parts:
            if part in self.ignored_dirs:
                return True
        return False

    # ===== Core Fixers =====

    def fix_imports(self, file_path: Path) -> bool:
        """Fix import ordering and remove unused imports using isort and autoflake."""
        if not file_path.suffix == ".py":
            return False

        logger.info(f"Fixing imports in {file_path.relative_to(self.root_dir)}")

        # First run isort to organize imports
        success, _ = self.run_command(f"isort --profile black {file_path}")
        if not success:
            return False

        # Then run autoflake to remove unused imports
        success, _ = self.run_command(
            f"autoflake --remove-all-unused-imports --ignore-init-module-imports --in-place {file_path}"
        )

        return success

    def format_code(self, file_path: Path) -> bool:
        """Format code using black."""
        if not file_path.suffix == ".py":
            return False

        logger.info(f"Formatting {file_path.relative_to(self.root_dir)}")
        success, _ = self.run_command(f"black {file_path}")
        return success

    # ===== Specific Issue Fixers =====

    def fix_exception_handling(self, content: str) -> str:
        """Improve exception handling patterns."""
        # Replace bare except with specific exception handling
        content = re.sub(
            r"except\s*:\s*",
            'except Exception as e:\n        logger.error(f"An error occurred: {e}")\n        ',
            content,
        )

        # Add logging for caught exceptions
        content = re.sub(
            r"except\s+(\w+)\s+as\s+(\w+):",
            r'except \1 as \2:\n        logger.error(f"Error: {\2}", exc_info=True)\n        ',
            content,
        )

        return content

    def fix_http_exceptions(self, content: str) -> str:
        """Convert direct HTTPException usage to custom exceptions."""
        # Replace direct HTTPException with custom exceptions
        replacements = [
            (
                r'raise\s+HTTPException\(status_code=404,\s*detail="([^"]+)"\)',
                r'raise ResourceNotFound(resource_type="resource", resource_id="")  # TODO: Specify resource type and ID',
            ),
            (
                r'raise\s+HTTPException\(status_code=401,\s*detail="([^"]+)"\)',
                r'raise AuthenticationError(detail="\1")',
            ),
            (
                r'raise\s+HTTPException\(status_code=403,\s*detail="([^"]+)"\)',
                r'raise AuthorizationError(detail="\1")',
            ),
            (
                r'raise\s+HTTPException\(status_code=400,\s*detail="([^"]+)"\)',
                r'raise ValidationError(detail="\1")',
            ),
            (
                r'raise\s+HTTPException\(status_code=409,\s*detail="([^"]+)"\)',
                r'raise BusinessRuleError(detail="\1")',
            ),
        ]

        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)

        return content

    def fix_missing_type_hints(self, content: str) -> str:
        """Add basic type hints to function parameters and return types."""
        # This is a simplified version - consider using a proper static type checker
        lines = content.splitlines()
        in_function = False

        for i, line in enumerate(lines):
            # Skip docstrings and comments
            if line.strip().startswith('"""') or line.strip().startswith("#"):
                continue

            # Detect function definitions
            if line.strip().startswith("def "):
                in_function = True

                # Add return type annotation if missing
                if "->" not in line and ":" in line:
                    # Simple heuristic: if function name starts with 'get_', 'find_', 'list_', assume it returns a list
                    func_name = line.split("def ")[1].split("(")[0].strip()
                    if any(func_name.startswith(prefix) for prefix in ["get_", "find_", "list_"]):
                        lines[i] = line.replace("):", ") -> List[Any]:")
                    # If function name starts with 'is_', 'has_', 'should_', assume it returns bool
                    elif any(func_name.startswith(prefix) for prefix in ["is_", "has_", "should_"]):
                        lines[i] = line.replace("):", ") -> bool:")
                    # Default to Any for other cases
                    else:
                        lines[i] = line.replace("):", ") -> Any:")

            # Add parameter type hints
            if in_function and "=" in line and ":" not in line.split("=")[0]:
                param = line.split("=")[0].strip()
                if not any(c in param for c in " 	"):  # Skip if already has type hint
                    # Simple type inference
                    if param.startswith("is_") or param.startswith("has_"):
                        lines[i] = line.replace("=", ": bool =")
                    elif param.endswith("_id"):
                        lines[i] = line.replace("=", ": str =")
                    elif param.endswith("s"):  # Plural might be a list
                        lines[i] = line.replace("=", ": List[Any] =")

        return "\n".join(lines)

    def fix_pydantic_models(self, content: str) -> str:
        """Ensure Pydantic models follow best practices."""
        lines = content.splitlines()
        in_model = False
        has_config = False

        for i, line in enumerate(lines):
            # Check if we're in a Pydantic model
            if "BaseModel" in line and "class " in line:
                in_model = True
                has_config = "Config" in content

            # Check for model fields without type hints
            if in_model and "=" in line and ":" not in line.split("=")[0]:
                field = line.split("=")[0].strip()
                if not any(c in field for c in " 	"):  # Skip if already has type hint
                    # Add Any as a default type hint
                    lines[i] = f"    {field}: Any = {line.split('=', 1)[1].strip()}"

            # Check for model end
            if in_model and line.strip() == "":
                in_model = False

                # Add Config class if missing
                if not has_config and i > 0 and "class " in lines[i - 1]:
                    config_block = [
                        "",
                        "    class Config:",
                        "        from_attributes = True  # orm_mode in Pydantic v2",
                        "        arbitrary_types_allowed = True",
                        "        json_encoders = {",
                        "            # Add custom JSON encoders here",
                        "        }",
                    ]
                    lines[i:i] = config_block

        return "\n".join(lines)

    def fix_common_issues(self, file_path: Path) -> bool:
        """Fix common Python code issues."""
        if not file_path.suffix == ".py":
            return False

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Apply all fixers
            content = self.fix_exception_handling(content)
            content = self.fix_http_exceptions(content)
            content = self.fix_missing_type_hints(content)
            content = self.fix_pydantic_models(content)

            # Clean up trailing whitespace and ensure proper newlines
            lines = [line.rstrip() for line in content.splitlines()]
            content = "\n".join(lines) + "\n"

            # Write back if changes were made
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return True

            return False

        except Exception as e:
            logger.error(f"Error fixing {file_path}: {e}")
            return False

    # ===== File Processing =====

    def process_file(self, file_path: Path) -> bool:
        """Apply all fixes to a single file."""
        if not file_path.is_file() or not file_path.suffix == ".py":
            return False

        if self.should_skip_file(file_path):
            return False

        relative_path = file_path.relative_to(self.root_dir)
        logger.info(f"\n{'Checking' if self.check_mode else 'Processing'} {relative_path}")
        self.files_processed += 1
        file_modified = False

        # Get file content for analysis
        with open(file_path, encoding="utf-8") as f:
            original_content = f.read()

        # Define fixers and their categories
        fixers = [
            (self.fix_imports, "imports"),
            (self.fix_common_issues, "formatting"),
            (self.fix_exception_handling, "exceptions"),
            (self.fix_missing_type_hints, "type_hints"),
            (self.fix_pydantic_models, "pydantic"),
            (self.format_code, "formatting"),
        ]

        for fixer, category in fixers:
            try:
                if fixer == self.fix_common_issues:
                    # For fix_common_issues, we need to handle it specially
                    fixed_content = self.fix_common_issues_content(original_content)
                    if fixed_content != original_content:
                        self.issues_found[category] += 1
                        if self.check_mode:
                            self._show_diff(
                                original_content,
                                fixed_content,
                                str(relative_path),
                                category,
                            )
                        file_modified = True
                else:
                    # For other fixers, check if they would make changes
                    temp_file = file_path.with_suffix(".tmp")
                    with open(temp_file, "w", encoding="utf-8") as f:
                        f.write(original_content)

                    if fixer(temp_file):
                        self.issues_found[category] += 1
                        if self.check_mode:
                            with open(temp_file, encoding="utf-8") as f:
                                fixed_content = f.read()
                            self._show_diff(
                                original_content,
                                fixed_content,
                                str(relative_path),
                                category,
                            )
                        file_modified = True

                    # Clean up
                    if temp_file.exists():
                        temp_file.unlink()

            except Exception as e:
                logger.error(f"Error in {fixer.__name__} for {file_path}: {e}")

        if file_modified and not self.check_mode:
            self.fixes_applied += 1

        return file_modified

    def _show_diff(self, original: str, modified: str, filepath: str, category: str):
        """Show a diff between original and modified content."""
        import difflib

        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"original/{filepath}",
            tofile=f"fixed/{filepath}",
            n=3,
        )

        diff_text = "".join(diff)
        if diff_text:
            logger.info(f"\n=== {filepath} - {category.upper()} ===\n{diff_text}")

    def fix_common_issues_content(self, content: str) -> str:
        """Apply common fixes to content and return the result."""
        content = self.fix_exception_handling(content)
        content = self.fix_http_exceptions(content)
        content = self.fix_missing_type_hints(content)
        content = self.fix_pydantic_models(content)
        return content

    def process_directory(self, directory: Path = None) -> dict[str, Any]:
        """Process all Python files in a directory recursively."""
        directory = directory or self.root_dir
        modified_files = 0

        logger.info(f"Scanning directory: {directory.relative_to(self.root_dir)}")

        for file_path in directory.rglob("*.py"):
            if self.should_skip_file(file_path):
                continue

            if self.process_file(file_path):
                modified_files += 1

        result = {
            "files_processed": self.files_processed,
            "files_with_issues": modified_files,
            "fixes_applied": self.fixes_applied,
            "issues_by_category": self.issues_found,
        }

        if self.check_mode:
            self._print_summary(result)

        return result

    def _print_summary(self, stats: dict[str, Any]):
        """Print a summary of issues found."""
        print("\n" + "=" * 80)
        print("DRY RUN SUMMARY")
        print("=" * 80)
        print(f"\nScanned {stats['files_processed']} Python files")
        print(f"Found issues in {stats['files_with_issues']} files\n")

        if stats["files_with_issues"] == 0:
            print("No issues found!")
            return

        print("ISSUES BY CATEGORY:")
        print("-" * 40)
        for category, count in stats["issues_by_category"].items():
            if count > 0:
                print(f"- {category.replace('_', ' ').title()}: {count}")

        print("\nRECOMMENDED ACTIONS:")
        print("-" * 40)
        if stats["issues_by_category"]["imports"] > 0:
            print("- Run 'isort' and 'autoflake' to organize and clean up imports")
        if stats["issues_by_category"]["formatting"] > 0:
            print("- Run 'black' to fix code formatting")
        if stats["issues_by_category"]["exceptions"] > 0:
            print("- Review and update exception handling patterns")
        if stats["issues_by_category"]["type_hints"] > 0:
            print("- Add type hints to functions and variables")
        if stats["issues_by_category"]["pydantic"] > 0:
            print("- Update Pydantic models to follow best practices")

        print("\nTo apply these fixes, run without the --check flag")
        print("=" * 80 + "\n")


def main():
    """Command-line interface for the code fixer."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically fix common Python code issues.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check for issues in current directory
  python autofix.py --check

  # Fix all Python files in a directory
  python autofix.py /path/to/project

  # Check a specific file
  python autofix.py --check path/to/file.py

  # Get more detailed output
  python autofix.py -v  # Info level
  python autofix.py -vv  # Debug level
""",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to file or directory to process (default: current directory)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for issues without making changes (dry run)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )
    args = parser.parse_args()

    # Set log level based on verbosity
    if args.verbose >= 2:
        logger.setLevel(logging.DEBUG)
    elif args.verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    target_path = Path(args.path).resolve()
    if not target_path.exists():
        logger.error(f"Path not found: {target_path}")
        sys.exit(1)

    # Initialize fixer with check mode
    fixer = CodeAutoFixer(
        root_dir=target_path if target_path.is_dir() else target_path.parent,
        check_mode=args.check,
    )

    try:
        if target_path.is_file():
            fixer.process_file(target_path)
        else:
            stats = fixer.process_directory(target_path)

            if not args.check:
                logger.info("\n=== Fixing Complete ===")
                logger.info(f"Files processed: {stats['files_processed']}")
                logger.info(f"Files modified: {stats['files_with_issues']}")
                logger.info(f"Total fixes applied: {sum(stats['issues_by_category'].values())}")
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=args.verbose > 0)
        sys.exit(1)


if __name__ == "__main__":
    main()
