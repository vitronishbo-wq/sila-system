#!/usr/bin/env python3
"""
Module Dependency Audit
Track imports between modules to detect circular dependencies and isolation violations.
"""

import ast
import sys
from collections import defaultdict
from pathlib import Path


class DependencyAuditor:
    """Audit module dependencies."""

    def __init__(self, modules_path):
        self.modules_path = Path(modules_path)
        self.dependencies = defaultdict(set)  # module -> set of imported modules
        self.violations = []
        self.modules = []

    def audit(self):
        """Run complete dependency audit."""
        self.modules = sorted(
            [
                d.name
                for d in self.modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        print(f"\n{'=' * 80}")
        print(f"[DEPENDENCY AUDIT - {len(self.modules)} MODULES]")
        print(f"{'=' * 80}\n")

        # Scan all imports
        for module_name in self.modules:
            self._scan_module_imports(module_name)

        # Check for issues
        self._check_circular_dependencies()
        self._check_isolation_violations()
        self._check_infrastructure_coupling()

        # Print results
        self._print_results()

    def _scan_module_imports(self, module_name: str):
        """Scan a module for imports."""
        module_path = self.modules_path / module_name

        # Scan all Python files
        for py_file in module_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                tree = ast.parse(content)

                # Extract imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            # Extract module base name
                            imported = self._extract_module_name(node.module)
                            if imported in self.modules and imported != module_name:
                                self.dependencies[module_name].add(imported)

                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            imported = self._extract_module_name(alias.name)
                            if imported in self.modules and imported != module_name:
                                self.dependencies[module_name].add(imported)

            except:
                pass

    def _extract_module_name(self, import_path: str) -> str:
        """Extract module name from import path."""
        # Handle 'apps.backend.app.modules.identity.domain' -> 'identity'
        parts = import_path.split(".")

        # Find first 'modules' and get next part
        try:
            idx = parts.index("modules")
            if idx + 1 < len(parts):
                return parts[idx + 1]
        except ValueError:
            pass

        return import_path.split(".")[0]

    def _check_circular_dependencies(self):
        """Detect circular dependencies."""
        visited = set()
        rec_stack = set()
        cycles = []

        def has_cycle(node, path):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.dependencies.get(node, set()):
                if neighbor not in visited:
                    if has_cycle(neighbor, path + [neighbor]):
                        return True
                elif neighbor in rec_stack:
                    cycles.append(path + [neighbor])
                    return True

            rec_stack.remove(node)
            return False

        for module in self.modules:
            if module not in visited:
                has_cycle(module, [module])

        if cycles:
            for cycle in cycles:
                self.violations.append(f"CIRCULAR: {' -> '.join(cycle)}")
        else:
            print("[PASS] No circular dependencies detected")

    def _check_isolation_violations(self):
        """Check if domain layer imports from application/infrastructure."""
        violations_found = False

        for module_name in self.modules:
            module_path = self.modules_path / module_name / "domain"

            if not module_path.exists():
                continue

            for py_file in module_path.rglob("*.py"):
                if "__pycache__" in str(py_file):
                    continue

                try:
                    content = py_file.read_text()

                    # Domain should NOT import from application or infrastructure
                    if (
                        "from apps.backend.app.modules" in content
                        or "from ..application" in content
                        or "from ..infrastructure" in content
                    ):
                        self.violations.append(
                            f"ISOLATION: {module_name}/domain imports from application/infrastructure"
                        )
                        violations_found = True

                except:
                    pass

        if not violations_found:
            print("[PASS] Domain layer properly isolated")

    def _check_infrastructure_coupling(self):
        """Check for cross-infrastructure imports."""
        violations_found = False

        for module_name in self.modules:
            module_path = self.modules_path / module_name / "infrastructure"

            if not module_path.exists():
                continue

            for py_file in module_path.rglob("*.py"):
                if "__pycache__" in str(py_file):
                    continue

                try:
                    content = py_file.read_text()

                    # Infrastructure of one module shouldn't import infrastructure of another
                    for other_module in self.modules:
                        if other_module != module_name:
                            pattern = f"from apps.backend.app.modules.{other_module}.infrastructure"
                            if pattern in content:
                                self.violations.append(
                                    f"COUPLING: {module_name}/infrastructure imports from {other_module}/infrastructure"
                                )
                                violations_found = True

                except:
                    pass

        if not violations_found:
            print("[PASS] Infrastructure layers properly decoupled")

    def _print_results(self):
        """Print audit results."""
        print(f"\n{'=' * 80}")
        print("[DEPENDENCY ANALYSIS]")
        print(f"{'=' * 80}\n")

        # Only show top 5 modules with most dependencies
        modules_with_deps = {m: len(deps) for m, deps in self.dependencies.items() if deps}

        if modules_with_deps:
            top_5 = sorted(modules_with_deps.items(), key=lambda x: -x[1])[:5]
            if top_5:
                print("TOP MODULES WITH DEPENDENCIES:")
                for module, count in top_5:
                    print(f"  {module}: {count} dependencies")
                print()

        # Violations
        print(f"[VIOLATIONS: {len(self.violations)}]")
        if self.violations:
            for violation in self.violations:
                print(f"  {violation}")
        else:
            print("  None - Clean architecture!")

        print(f"\n{'=' * 80}")
        if not self.violations:
            print("RESULT: PASSED - Module dependencies are healthy")
        else:
            print(f"RESULT: {len(self.violations)} violations found")
        print(f"{'=' * 80}\n")


if __name__ == "__main__":
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"

    if not modules_path.exists():
        print(f"[ERROR] Modules path not found: {modules_path}")
        sys.exit(1)

    auditor = DependencyAuditor(modules_path)
    auditor.audit()
