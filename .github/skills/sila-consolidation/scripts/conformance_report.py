#!/usr/bin/env python3
"""
conformance_report.py

Generate visual conformance report for consolidated SILA modules.
Outputs markdown with metrics, pass/fail status, and audit trails.

Usage:
  python scripts/conformance_report.py --module justice --output report.md
  python scripts/conformance_report.py --module identity --template conformance-checklist.md
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class ModuleConformanceAuditor:
    """Audit a consolidated module for structural and architectural conformance."""

    def __init__(self, module_name: str, project_root: str = "."):
        self.module_name = module_name
        self.project_root = project_root
        self.module_path = Path(project_root) / "app" / "modules" / module_name
        self.core_path = self.module_path / "core"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results = {}

    def audit(self) -> Dict:
        """Run all conformance checks."""
        if not self.core_path.exists():
            self.results = {
                "module": self.module_name,
                "timestamp": self.timestamp,
                "core_path": str(self.core_path),
                "checks": {},
                "overall_status": "FAILED",
                "conformance_score": 0.0,
                "status": "error",
                "message": f"Core module not found at {self.core_path}",
            }
            return self.results

        self.results = {
            "module": self.module_name,
            "timestamp": self.timestamp,
            "core_path": str(self.core_path),
            "checks": {},
        }

        # Run all checks
        self.check_directory_structure()
        self.check_required_files()
        self.check_no_circular_imports()
        self.check_entities_consolidated()
        self.check_services_unified()
        self.check_infrastructure_isolation()
        self.check_ports_defined()
        self.check_tests_exist()

        # Calculate overall status
        self.results["overall_status"] = self._calculate_status()
        self.results["conformance_score"] = self._calculate_score()

        return self.results

    def check_directory_structure(self):
        """Verify hexagonal structure exists."""
        required_dirs = ["domain", "application", "infrastructure"]
        checks = []

        for dir_name in required_dirs:
            dir_path = self.core_path / dir_name
            exists = dir_path.exists() and dir_path.is_dir()
            checks.append({"item": f"{dir_name}/", "status": "PASS" if exists else "FAIL"})

        self.results["checks"]["directory_structure"] = {
            "name": "Hexagonal Directory Structure",
            "items": checks,
            "passed": sum(1 for c in checks if c["status"] == "PASS"),
            "total": len(checks),
        }

    def check_required_files(self):
        """Check for required boundary files."""
        required = [
            ("domain/__init__.py", "Domain exports"),
            ("application/__init__.py", "Application exports"),
            ("infrastructure/__init__.py", "Infrastructure exports"),
        ]

        checks = []
        for rel_path, description in required:
            file_path = self.core_path / rel_path
            exists = file_path.exists()
            checks.append({
                "item": f"{rel_path} ({description})",
                "status": "PASS" if exists else "FAIL",
            })

        self.results["checks"]["required_files"] = {
            "name": "Required Boundary Files",
            "items": checks,
            "passed": sum(1 for c in checks if c["status"] == "PASS"),
            "total": len(checks),
        }

    def check_entities_consolidated(self):
        """Count entities - should be centralized in domain/entities."""
        entity_dir = self.core_path / "domain" / "entities"
        entity_files = list(entity_dir.glob("*.py")) if entity_dir.exists() else []

        # Check for orphaned entities outside domain/entities
        orphaned = []
        for file in self.core_path.rglob("*.py"):
            name_lower = file.name.lower()
            if file.parent.name != "entities" and (
                "entity" in name_lower or "model" in name_lower or "_entity" in name_lower
            ):
                if "domain" not in str(file):
                    orphaned.append(str(file))

        self.results["checks"]["entity_consolidation"] = {
            "name": "Entity Consolidation",
            "items": [
                {
                    "item": f"Entities in domain/entities/",
                    "status": "PASS",
                    "count": len(entity_files),
                },
                {
                    "item": f"Orphaned entities outside domain/entities",
                    "status": "PASS" if len(orphaned) == 0 else "FAIL",
                    "count": len(orphaned),
                },
            ],
            "passed": 1 if len(orphaned) == 0 else 0,
            "total": 2,
        }

    def check_services_unified(self):
        """Check that application services are centralized."""
        service_dir = self.core_path / "application" / "services"
        service_files = list(service_dir.glob("*.py")) if service_dir.exists() else []

        self.results["checks"]["service_unification"] = {
            "name": "Service Unification",
            "items": [
                {
                    "item": "Application services",
                    "status": "PASS" if len(service_files) > 0 else "INFO",
                    "count": len(service_files),
                }
            ],
            "passed": 1 if len(service_files) > 0 else 0,
            "total": 1,
        }

    def check_infrastructure_isolation(self):
        """Check that infrastructure is isolated (no domain/application logic)."""
        checks = []

        # Find Python files in infrastructure
        if (self.core_path / "infrastructure").exists():
            for py_file in (self.core_path / "infrastructure").rglob("*.py"):
                if py_file.name == "__init__.py":
                    continue

                with open(py_file) as f:
                    content = f.read()

                # Check for domain/business logic (heuristic)
                has_business_logic = (
                    "if " in content and ("raise " in content or "assert " in content)
                )

                if not has_business_logic:
                    checks.append({"file": py_file.name, "status": "PASS"})
                else:
                    checks.append({"file": py_file.name, "status": "WARN"})

        self.results["checks"]["infrastructure_isolation"] = {
            "name": "Infrastructure Isolation",
            "items": checks if checks else [{"status": "INFO", "message": "No files to check"}],
            "passed": sum(1 for c in checks if c.get("status") == "PASS"),
            "total": max(len(checks), 1),
        }

    def check_ports_defined(self):
        """Check for port definitions (abstract base classes)."""
        ports_dir = self.core_path / "infrastructure" / "ports"
        checks = []

        if ports_dir.exists():
            port_files = list(ports_dir.glob("*.py"))
            checks.append({
                "item": "Ports directory exists",
                "status": "PASS",
                "count": len(port_files),
            })

            # Check that ports use ABC
            abc_files = 0
            for port_file in port_files:
                if port_file.name == "__init__.py":
                    continue
                with open(port_file) as f:
                    content = f.read()
                if "ABC" in content or "@abstractmethod" in content:
                    abc_files += 1

            checks.append({
                "item": "Ports using ABC/abstractmethod",
                "status": "PASS" if abc_files > 0 else "WARN",
                "count": abc_files,
            })
        else:
            checks.append({"item": "Ports directory", "status": "WARN"})

        self.results["checks"]["ports_defined"] = {
            "name": "Port Definitions",
            "items": checks,
            "passed": sum(1 for c in checks if c.get("status") == "PASS"),
            "total": len(checks),
        }

    def check_no_circular_imports(self):
        """Check for imports from obsolete contexts."""
        problematic_patterns = [
            "bounded_contexts",
            "civil_registry",
            "vital_events",
            "identity_documents",
        ]

        violations = []
        for py_file in self.core_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
            with open(py_file) as f:
                content = f.read()

            for pattern in problematic_patterns:
                if f"from app.modules.{self.module_name}.{pattern}" in content:
                    violations.append({
                        "file": str(py_file.relative_to(self.core_path)),
                        "pattern": pattern,
                    })

        self.results["checks"]["circular_imports"] = {
            "name": "Circular Dependency Detection",
            "violations_found": len(violations),
            "status": "PASS" if len(violations) == 0 else "FAIL",
            "items": violations[:5] if violations else [],
        }

    def check_tests_exist(self):
        """Check for test coverage."""
        test_dirs = list(self.core_path.rglob("tests"))
        test_files = list(self.core_path.rglob("test_*.py")) + list(
            self.core_path.rglob("*_test.py")
        )

        self.results["checks"]["tests"] = {
            "name": "Test Coverage",
            "items": [
                {
                    "item": "Test directories found",
                    "status": "PASS" if len(test_dirs) > 0 else "INFO",
                    "count": len(test_dirs),
                },
                {
                    "item": "Test files found",
                    "status": "PASS" if len(test_files) > 0 else "INFO",
                    "count": len(test_files),
                },
            ],
            "passed": sum(1 for c in [
                len(test_dirs) > 0,
                len(test_files) > 0,
            ] if c),
            "total": 2,
        }

    def _calculate_status(self) -> str:
        """Calculate overall conformance status."""
        critical_checks = ["directory_structure", "circular_imports", "required_files"]
        for check_key in critical_checks:
            if check_key in self.results["checks"]:
                check = self.results["checks"][check_key]
                if check.get("status") == "FAIL":
                    return "FAILED"

        return "PASSED"

    def _calculate_score(self) -> float:
        """Calculate conformance score (0-100)."""
        total_checks = 0
        passed_checks = 0

        for check in self.results["checks"].values():
            if "passed" in check and "total" in check:
                total_checks += check["total"]
                passed_checks += check["passed"]

        if total_checks == 0:
            return 0.0

        return (passed_checks / total_checks) * 100

    def to_markdown(self) -> str:
        """Export results as markdown."""
        lines = [
            f"# Consolidation Conformance Report: {self.module_name}",
            "",
            f"**Generated**: {self.timestamp}",
            f"**Module Path**: `{self.core_path}`",
            f"**Overall Status**: {'PASSED' if self.results['overall_status'] == 'PASSED' else 'FAILED'}",
            f"**Conformance Score**: {self.results['conformance_score']:.1f}%",
            "",
            "---",
            "",
        ]

        for check_key, check_data in self.results["checks"].items():
            lines.append(f"## {check_data['name']}")
            lines.append("")

            if "items" in check_data:
                for item in check_data["items"]:
                    status_symbol = "PASS" if item.get("status") == "PASS" else "WARN"
                    lines.append(f"{status_symbol} {item.get('item', item.get('file', 'Unknown'))}")
                    if "count" in item:
                        lines.append(f"  - Count: {item['count']}")

            if "status" in check_data:
                lines.append(
                    f"\n**Status**: {'PASS' if check_data['status'] == 'PASS' else 'FAIL'}"
                )

            if "passed" in check_data and "total" in check_data:
                lines.append(
                    f"\n**Score**: {check_data['passed']}/{check_data['total']} items"
                )

            lines.append("")

        lines.extend([
            "---",
            "",
            "## Sign-Off",
            "",
            "Module consolidated and audit passed" if self.results["overall_status"] == "PASSED"
            else "Module has conformance issues - review above",
            "",
        ])

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate conformance report for SILA consolidated modules"
    )
    parser.add_argument("--module", required=True, help="Module name (e.g., 'justice')")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--template", help="Template to include (e.g., conformance-checklist.md)")

    args = parser.parse_args()

    auditor = ModuleConformanceAuditor(args.module, args.project_root)
    results = auditor.audit()

    if args.json:
        output = json.dumps(results, indent=2)
    else:
        output = auditor.to_markdown()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
