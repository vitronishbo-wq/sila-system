#!/usr/bin/env python3
"""
SILA Exception Consolidation Script
Moves all exceptions to core/exceptions, eliminates duplicates, updates imports
Follows 3 inviolable rules: tree-index discovery, parallel batch normalization, visual reporting
"""

import asyncio
import re
from collections import defaultdict
from pathlib import Path

# Configuration
BACKEND_ROOT = Path("/home/dev03wsl/sila-system/apps/backend")
CORE_EXCEPTIONS_DIR = BACKEND_ROOT / "core" / "exceptions"
MODULES_DIR = BACKEND_ROOT / "app" / "modules"

# Exception patterns to consolidate
EXCEPTION_PATTERNS = {
    "NotFoundException": r"class\s+(\w+)?NotFoundException\(",
    "ValidationException": r"class\s+(\w+)?ValidationException\(",
    "DomainException": r"class\s+(\w+)?DomainException\(",
    "ConflictException": r"class\s+(\w+)?ConflictException\(",
    "UnauthorizedException": r"class\s+(\w+)?UnauthorizedException\(",
}


class ConsolidationAuditor:
    """Audits and maps exception consolidation"""

    def __init__(self):
        self.exceptions_found: dict[str, list[str]] = defaultdict(list)
        self.modules_with_exceptions: set[str] = set()
        self.import_statements: dict[str, set[str]] = defaultdict(set)
        self.actions_log: list[str] = []

    def discover_exceptions(self) -> dict[str, int]:
        """
        BATCH 1: Discovery phase - map all exception definitions
        Returns: { exception_type: count }
        """
        self.actions_log.append("=" * 80)
        self.actions_log.append("PHASE 1: EXCEPTION DISCOVERY")
        self.actions_log.append("=" * 80)

        for module_dir in MODULES_DIR.rglob("*.py"):
            if "__pycache__" in str(module_dir):
                continue

            try:
                content = module_dir.read_text(encoding="utf-8")

                # Find all exception definitions
                for pattern_name, pattern in EXCEPTION_PATTERNS.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        self.exceptions_found[pattern_name].append(str(module_dir))
                        self.modules_with_exceptions.add(str(module_dir.parent))

                        # Log specific exceptions found
                        for match in matches:
                            class_name = f"{match}{pattern_name}" if match else pattern_name
                            self.actions_log.append(
                                f"  ✓ {class_name} in {module_dir.relative_to(BACKEND_ROOT)}"
                            )

            except Exception as e:
                self.actions_log.append(f"  ⚠ Error reading {module_dir}: {e}")

        # Summary
        total_exceptions = sum(len(v) for v in self.exceptions_found.values())
        self.actions_log.append("")
        self.actions_log.append("Discovery Summary:")
        for exc_type, locations in self.exceptions_found.items():
            self.actions_log.append(f"  • {exc_type}: {len(locations)} definitions")
        self.actions_log.append(f"  • Total: {total_exceptions} exception definitions found")
        self.actions_log.append(f"  • Affected modules: {len(self.modules_with_exceptions)}")

        return {k: len(v) for k, v in self.exceptions_found.items()}

    def map_imports(self):
        """
        BATCH 1B: Map all exception imports to understand usage
        """
        self.actions_log.append("")
        self.actions_log.append("Mapping exception imports...")

        for module_dir in MODULES_DIR.rglob("*.py"):
            if "__pycache__" in str(module_dir):
                continue

            try:
                content = module_dir.read_text(encoding="utf-8")

                # Find import statements
                import_matches = re.findall(
                    r"from\s+[\w\.]+exceptions\s+import\s+([^\n]+)", content
                )
                if import_matches:
                    for imports in import_matches:
                        self.import_statements[str(module_dir.relative_to(BACKEND_ROOT))].add(
                            imports.strip()
                        )

            except Exception:
                pass

        self.actions_log.append(f"  • Mapped imports from {len(self.import_statements)} files")

    def generate_consolidation_action_list(self) -> list[tuple[str, str]]:
        """
        BATCH 2: Generate actions to move exceptions to core
        Returns: { (source, action): description }
        """
        self.actions_log.append("")
        self.actions_log.append("=" * 80)
        self.actions_log.append("PHASE 2: CONSOLIDATION ACTIONS")
        self.actions_log.append("=" * 80)

        actions = []

        # For each exception type found, create consolidation action
        for exc_type, locations in self.exceptions_found.items():
            core_file = CORE_EXCEPTIONS_DIR / f"{exc_type.lower()}_hierarchy.py"
            actions.append((f"consolidate_{exc_type}", f"Move {len(locations)} → {core_file}"))

        for action_name, description in actions:
            self.actions_log.append(f"  ✓ {description}")

        return actions

    def generate_import_replacement_plan(self) -> dict[str, str]:
        """
        BATCH 3: Generate import replacement rules
        """
        self.actions_log.append("")
        self.actions_log.append("=" * 80)
        self.actions_log.append("PHASE 3: IMPORT REPLACEMENT")
        self.actions_log.append("=" * 80)

        replacements = {}

        # Create replacement rules for each discovered exception
        for exc_type in self.exceptions_found.keys():
            old_patterns = [
                rf"from\s+[\w\.]+\.exceptions\s+import\s+.*{exc_type}",
                rf"from\s+[\w\.]+\.domain\.exceptions\s+import\s+.*{exc_type}",
            ]
            new_import = f"from apps.backend.app.core.exceptions import {exc_type}"

            for old_pattern in old_patterns:
                replacements[old_pattern] = new_import
                self.actions_log.append(f"  ✓ {old_pattern[:60]}... → {new_import}")

        self.actions_log.append(f"  • Total import replacements planned: {len(replacements)}")

        return replacements

    def generate_report(self) -> str:
        """Generate visual consolidation report"""
        report = "\n".join(self.actions_log)
        report += "\n\n" + "=" * 80
        report += "\n" + "CONSOLIDATION AUDIT METRICS" + "\n"
        report += "=" * 80 + "\n"

        total_exc = sum(len(v) for v in self.exceptions_found.values())
        total_imports = len(self.import_statements)

        report += "\nBefore Consolidation:\n"
        report += f"  • Exception definitions: {total_exc}\n"
        report += f"  • Scattered across: {len(self.modules_with_exceptions)} module locations\n"
        report += f"  • Files with import statements: {total_imports}\n\n"

        report += "After Consolidation (Target):\n"
        report += f"  • Exception definitions: ~{len(self.exceptions_found)} (centralized)\n"
        report += "  • Scattered across: 1 module (core/exceptions/)\n"
        report += "  • Import pattern: from apps.backend.app.core.exceptions import <exception>\n"
        report += f"  • Reduction: {((total_exc - len(self.exceptions_found)) / total_exc * 100):.1f}%\n\n"

        report += f"Modules Affected: {len(self.modules_with_exceptions)}\n"

        return report


async def main():
    """Main execution following SILA consolidation workflow"""

    print("\n" + "=" * 80)
    print("SILA EXCEPTION CONSOLIDATION - DISCOVERY & PLANNING PHASE")
    print("=" * 80)

    auditor = ConsolidationAuditor()

    # Phase 1: Discover
    print("\n[PHASE 1] Discovering exceptions...")
    summary = auditor.discover_exceptions()

    # Phase 1B: Map imports
    print("[PHASE 1B] Mapping import patterns...")
    auditor.map_imports()

    # Phase 2: Generate actions
    print("[PHASE 2] Generating consolidation actions...")
    actions = auditor.generate_consolidation_action_list()

    # Phase 3: Import replacement
    print("[PHASE 3] Planning import replacements...")
    replacements = auditor.generate_import_replacement_plan()

    # Generate report
    report = auditor.generate_report()
    print("\n" + report)

    # Save report
    report_file = BACKEND_ROOT / "EXCEPTION_CONSOLIDATION_DISCOVERY.md"
    report_file.write_text(report)
    print(f"\n✅ Report saved: {report_file}")

    # Summary JSON for next phase
    summary_data = {
        "exceptions_found": summary,
        "total_definitions": sum(summary.values()),
        "modules_affected": len(auditor.modules_with_exceptions),
        "import_files": len(auditor.import_statements),
        "consolidation_actions": len(actions),
    }

    print("\n📊 READY FOR EXECUTION PHASE:")
    print(f"   • {summary_data['total_definitions']} exception definitions to consolidate")
    print(f"   • {summary_data['modules_affected']} modules affected")
    print(f"   • {summary_data['import_files']} files needing import updates")


if __name__ == "__main__":
    asyncio.run(main())
