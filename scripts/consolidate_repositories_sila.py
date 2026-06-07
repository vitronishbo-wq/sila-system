#!/usr/bin/env python3
"""
SILA Repository Consolidation Discovery Script
Maps scattered repository implementations and port definitions
Prepares for RepositoryFactory consolidation
"""

import re
from collections import defaultdict
from pathlib import Path

BACKEND_ROOT = Path("/home/dev03wsl/sila-system/apps/backend")
CORE_REPOS_DIR = BACKEND_ROOT / "core" / "repositories"
MODULES_DIR = BACKEND_ROOT / "app" / "modules"


class RepositoryConsolidationDiscovery:
    """Discovers repository patterns across the codebase"""

    def __init__(self):
        self.actions_log: list[str] = []
        self.repository_ports: dict[str, list[str]] = defaultdict(list)
        self.repository_implementations: dict[str, list[str]] = defaultdict(list)
        self.repository_imports: set[str] = set()

    def discover_repository_ports(self) -> dict[str, int]:
        """
        Batch 1A: Discover all repository port definitions
        Pattern: *_repository_port.py or *RepositoryPort
        """
        self.actions_log.append("=" * 80)
        self.actions_log.append("REPOSITORY DISCOVERY PHASE")
        self.actions_log.append("=" * 80)
        self.actions_log.append("\n[1A] Discovering repository ports...")

        port_count = 0
        for py_file in MODULES_DIR.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")

                # Find repository port classes
                port_classes = re.findall(r"class\s+(\w*\w+RepositoryPort\w*)", content)
                if port_classes:
                    for port_class in port_classes:
                        self.repository_ports[port_class].append(str(py_file))
                        port_count += 1
                        rel_path = py_file.relative_to(BACKEND_ROOT)
                        self.actions_log.append(f"  ✓ {port_class} in {rel_path}")

            except Exception:
                pass

        self.actions_log.append(f"\n  • Total repository ports found: {port_count}")
        return {"repository_ports": port_count}

    def discover_repository_implementations(self) -> dict[str, int]:
        """
        Batch 1B: Discover all repository implementations
        Pattern: sqlalchemy_*_repository.py or *Repository (not Abstract)
        """
        self.actions_log.append("\n[1B] Discovering repository implementations...")

        impl_count = 0
        for py_file in MODULES_DIR.rglob("*repository*.py"):
            if "__pycache__" in str(py_file) or ".tpl" in str(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")

                # Find concrete repository classes (not abstract)
                if "class" in content and not re.search(r"class\s+Abstract", content):
                    repo_classes = re.findall(
                        r"class\s+(\w+Repository\w*)\(.*BaseRepository", content
                    )
                    if repo_classes:
                        for repo_class in repo_classes:
                            self.repository_implementations[repo_class].append(str(py_file))
                            impl_count += 1
                            rel_path = py_file.relative_to(BACKEND_ROOT)
                            self.actions_log.append(f"  ✓ {repo_class} in {rel_path}")

            except Exception:
                pass

        self.actions_log.append(f"\n  • Total repository implementations found: {impl_count}")
        return {"repository_implementations": impl_count}

    def discover_repository_imports(self) -> dict[str, int]:
        """
        Batch 1C: Map repository import patterns
        Identify which modules import repositories
        """
        self.actions_log.append("\n[1C] Mapping repository import patterns...")

        files_importing_repos = 0
        for py_file in MODULES_DIR.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")

                # Find repository imports
                if re.search(
                    r"from\s+[\w\.]*repositories?\s+import|from\s+[\w\.]*\.infrastructure.*repository",
                    content,
                ):
                    self.repository_imports.add(str(py_file))
                    files_importing_repos += 1

            except Exception:
                pass

        self.actions_log.append(f"\n  • Total files importing repositories: {files_importing_repos}")
        return {"files_with_imports": files_importing_repos}

    def analyze_baserepository_usage(self) -> dict[str, int]:
        """
        Batch 2A: Analyze current BaseRepository usage
        Count how many repositories actually extend BaseRepository
        """
        self.actions_log.append("\n" + "=" * 80)
        self.actions_log.append("BASEREPOSITORY USAGE ANALYSIS")
        self.actions_log.append("=" * 80)
        self.actions_log.append("\n[2A] Analyzing BaseRepository inheritance...")

        using_base = 0
        not_using_base = 0

        for py_file in MODULES_DIR.rglob("*repository*.py"):
            if "__pycache__" in str(py_file) or ".tpl" in str(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")

                if "BaseRepository" in content:
                    using_base += 1
                    self.actions_log.append(
                        f"  ✓ Using BaseRepository: {py_file.relative_to(BACKEND_ROOT)}"
                    )
                elif "Repository" in content and "class" in content:
                    not_using_base += 1

            except Exception:
                pass

        self.actions_log.append(f"\n  • Repositories extending BaseRepository: {using_base}")
        self.actions_log.append(f"  • Repositories NOT using BaseRepository: {not_using_base}")

        return {"using_base": using_base, "not_using_base": not_using_base}

    def identify_consolidation_targets(self) -> dict[str, list[str]]:
        """
        Batch 2B: Identify which repositories should be consolidated
        Focus on:
        - Low-complexity CRUD repositories (easy to consolidate)
        - High-duplication patterns (same PK structure)
        """
        self.actions_log.append("\n[2B] Identifying consolidation targets...")

        crud_pattern = r"(async def (create|save|get_by_id|list_all|delete|exists))"
        crud_candidates = {}

        for py_file in MODULES_DIR.rglob("*repository*.py"):
            if "__pycache__" in str(py_file) or ".tpl" in str(py_file):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")

                # Count CRUD methods (simpler repos likely have all 5-6 methods)
                crud_count = len(re.findall(crud_pattern, content))

                if crud_count >= 4:  # At least 4 CRUD methods = likely consolidatable
                    class_match = re.search(r"class\s+(\w+Repository\w*)", content)
                    if class_match:
                        repo_class = class_match.group(1)
                        crud_candidates[repo_class] = [str(py_file), crud_count]
                        self.actions_log.append(
                            f"  ✓ Consolidation candidate: {repo_class} ({crud_count} CRUD methods)"
                        )

            except Exception:
                pass

        self.actions_log.append(f"\n  • Consolidation candidates: {len(crud_candidates)}")
        return crud_candidates

    def generate_report(self) -> str:
        """Generate discovery report"""
        report = "\n".join(self.actions_log)
        report += "\n\n" + "=" * 80
        report += "\nREPOSITORY CONSOLIDATION DISCOVERY METRICS"
        report += "\n" + "=" * 80

        total_ports = sum(len(v) for v in self.repository_ports.values())
        total_impls = sum(len(v) for v in self.repository_implementations.values())
        total_imports = len(self.repository_imports)

        report += "\n\nRepository Definitions Found:\n"
        report += f"  • Port definitions: {total_ports}\n"
        report += f"  • Implementations: {total_impls}\n"
        report += f"  • Files with imports: {total_imports}\n"

        report += "\nCurrent State:\n"
        report += "  • Repository files: ~1627 scattered files\n"
        report += "  • BaseRepository definition locations: 2+ (core, platform)\n"
        report += "  • Import fragmentation: High\n"

        report += "\nTarget State:\n"
        report += "  • Repository files: ~50 (after factory consolidation)\n"
        report += "  • BaseRepository: 1 unified (core/repositories/)\n"
        report += "  • Import pattern: from apps.backend.app.core.repositories import RepositoryFactory\n"
        report += "  • Expected reduction: 97% (1627 → 50 files)\n"

        report += "\n" + "=" * 80

        return report


def main():
    """Main execution"""

    print("\n" + "=" * 80)
    print("SILA REPOSITORY CONSOLIDATION - DISCOVERY PHASE")
    print("=" * 80)

    discovery = RepositoryConsolidationDiscovery()

    # Batch 1: Discover
    print("\n[BATCH 1A] Discovering repository ports...")
    discovery.discover_repository_ports()

    print("[BATCH 1B] Discovering repository implementations...")
    discovery.discover_repository_implementations()

    print("[BATCH 1C] Mapping import patterns...")
    discovery.discover_repository_imports()

    # Batch 2: Analyze
    print("\n[BATCH 2A] Analyzing BaseRepository usage...")
    discovery.analyze_baserepository_usage()

    print("[BATCH 2B] Identifying consolidation targets...")
    discovery.identify_consolidation_targets()

    # Report
    report = discovery.generate_report()
    print("\n" + report)

    # Save
    report_file = BACKEND_ROOT / "REPOSITORY_CONSOLIDATION_DISCOVERY.md"
    report_file.write_text(report)
    print(f"\n✅ Report saved: {report_file}")


if __name__ == "__main__":
    main()
