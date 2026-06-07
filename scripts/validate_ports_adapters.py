#!/usr/bin/env python3
"""
FASE 5: Rigorous Port & Adapter Validation
Validates Port/Adapter pattern implementation quality.
"""

import ast
import sys
from pathlib import Path


class PortAdapterValidator:
    """Validates Port/Adapter pattern compliance."""

    def __init__(self, modules_path):
        self.modules_path = Path(modules_path)
        self.issues = []
        self.passed = 0
        self.failed = 0

    def validate_all(self):
        """Validate all modules' Port/Adapter patterns."""
        modules = sorted(
            [
                d
                for d in self.modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        print(f"\n{'=' * 80}")
        print(f"[VALIDATING PORT/ADAPTER PATTERNS - {len(modules)} MODULES]")
        print(f"{'=' * 80}\n")

        for module in modules:
            self._validate_module(module)

        self._print_results()

    def _validate_module(self, module_path):
        """Validate a single module's Port/Adapter."""
        module_name = module_path.name
        adapter_file = module_path / "infrastructure" / "adapters.py"

        if not adapter_file.exists():
            return

        try:
            content = adapter_file.read_text()
            tree = ast.parse(content)

            # Extract class definitions
            classes = self._extract_classes(tree)

            if not classes:
                self.issues.append(f"[{module_name}] No classes defined")
                self.failed += 1
                return

            # Find Port and Adapter classes
            port_names = [c for c in classes if "Port" in c]
            adapter_names = [c for c in classes if "Adapter" in c]

            if not port_names:
                self.issues.append(f"[{module_name}] No Port class found")
                self.failed += 1
                return

            if not adapter_names:
                self.issues.append(f"[{module_name}] No Adapter class found")
                self.failed += 1
                return

            # Validate Port is ABC
            port_name = port_names[0]
            port_class = self._find_class(tree, port_name)

            if not self._is_abc_class(port_class):
                self.issues.append(f"[{module_name}] {port_name} doesn't inherit from ABC")
                self.failed += 1
                return

            # Validate Adapter inherits from Port
            adapter_name = adapter_names[0]
            adapter_class = self._find_class(tree, adapter_name)

            if not self._inherits_from(adapter_class, port_name):
                self.issues.append(
                    f"[{module_name}] {adapter_name} doesn't inherit from {port_name}"
                )
                self.failed += 1
                return

            # Validate Port has abstract methods
            port_methods = self._get_abstract_methods(port_class)
            if not port_methods:
                self.issues.append(f"[{module_name}] {port_name} has no abstract methods")
                self.failed += 1
                return

            # Validate Adapter implements all abstract methods
            adapter_methods = self._get_implemented_methods(adapter_class)
            missing = port_methods - adapter_methods

            if missing:
                self.issues.append(f"[{module_name}] {adapter_name} missing: {', '.join(missing)}")
                self.failed += 1
                return

            # All checks passed
            print(f"[OK] {module_name} - Port/Adapter pattern correct")
            self.passed += 1

        except Exception as e:
            self.issues.append(f"[{module_name}] Parse error: {str(e)[:50]}")
            self.failed += 1

    def _extract_classes(self, tree: ast.AST) -> list[str]:
        """Extract all class names from AST."""
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    def _find_class(self, tree: ast.AST, name: str):
        """Find a specific class definition."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == name:
                return node
        return None

    def _is_abc_class(self, class_def) -> bool:
        """Check if class inherits from ABC."""
        if not class_def:
            return False
        for base in class_def.bases:
            if isinstance(base, ast.Name) and base.id == "ABC":
                return True
        return False

    def _inherits_from(self, class_def, parent_name: str) -> bool:
        """Check if class inherits from parent."""
        if not class_def:
            return False
        for base in class_def.bases:
            if isinstance(base, ast.Name) and base.id == parent_name:
                return True
        return False

    def _get_abstract_methods(self, class_def) -> set[str]:
        """Get abstract method names (public methods only)."""
        methods = set()
        if not class_def:
            return methods

        for node in class_def.body:
            # Handle both FunctionDef and AsyncFunctionDef
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef)
            ) and not node.name.startswith("_"):
                # Check if has @abstractmethod decorator
                has_abstract = False
                for decorator in node.decorator_list:
                    dec_name = None
                    if isinstance(decorator, ast.Name):
                        dec_name = decorator.id
                    elif isinstance(decorator, ast.Attribute):
                        dec_name = decorator.attr

                    if dec_name and "abstract" in dec_name.lower():
                        has_abstract = True
                        break

                if has_abstract:
                    methods.add(node.name)

        return methods

    def _get_implemented_methods(self, class_def) -> set[str]:
        """Get implemented method names (public methods only)."""
        methods = set()
        if not class_def:
            return methods

        for node in class_def.body:
            # Handle both FunctionDef and AsyncFunctionDef
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef)
            ) and not node.name.startswith("_"):
                methods.add(node.name)

        return methods

    def _print_results(self):
        """Print validation results."""
        total = self.passed + self.failed
        percentage = (self.passed * 100) // total if total > 0 else 0

        print(f"\n{'=' * 80}")
        print(f"RESULTS: {self.passed}/{total} PASSED ({percentage}%)")
        print(f"{'=' * 80}\n")

        if self.issues:
            print("ISSUES FOUND:")
            for issue in self.issues[:20]:  # Show first 20
                print(f"  {issue}")
            if len(self.issues) > 20:
                print(f"  ... and {len(self.issues) - 20} more")
            print()
        else:
            print("NO ISSUES - All Port/Adapter patterns are correct!\n")


if __name__ == "__main__":
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"

    if not modules_path.exists():
        print(f"[ERROR] Modules path not found: {modules_path}")
        sys.exit(1)

    validator = PortAdapterValidator(modules_path)
    validator.validate_all()
