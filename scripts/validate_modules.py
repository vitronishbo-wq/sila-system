#!/usr/bin/env python3
"""
FASE 5: Real Module Validation Tests
Direct validation - no external dependencies.
"""

import sys
from pathlib import Path


class ModuleValidator:
    def __init__(self, modules_path):
        self.modules_path = Path(modules_path)
        self.tests_passed = 0
        self.tests_failed = 0
        self.failed_tests = []

    def validate_all(self):
        """Run all validation tests."""
        modules = sorted(
            [
                d
                for d in self.modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        print(f"\n{'=' * 80}")
        print(f"[VALIDATING {len(modules)} MODULES]")
        print(f"{'=' * 80}\n")

        self._test_all_modules_have_routers(modules)
        self._test_all_modules_have_models(modules)
        self._test_all_modules_have_exceptions(modules)
        self._test_routers_have_health(modules)
        self._test_routers_have_fastapi(modules)
        self._test_port_adapter_pattern(modules)
        self._test_repository_pattern(modules)
        self._test_required_directories(modules)

        self._print_summary()

    def _test_all_modules_have_routers(self, modules):
        """Test all modules have routers.py"""
        missing = [m.name for m in modules if not (m / "api" / "routers.py").exists()]
        if not missing:
            print("[PASS] All modules have api/routers.py")
            self.tests_passed += 1
        else:
            print(f"[FAIL] Missing routers: {missing}")
            self.tests_failed += 1
            self.failed_tests.append(f"routers missing in {len(missing)} modules")

    def _test_all_modules_have_models(self, modules):
        """Test all modules have models.py"""
        missing = [m.name for m in modules if not (m / "domain" / "models.py").exists()]
        if not missing:
            print("[PASS] All modules have domain/models.py")
            self.tests_passed += 1
        else:
            print(f"[FAIL] Missing models: {missing}")
            self.tests_failed += 1
            self.failed_tests.append(f"models missing in {len(missing)} modules")

    def _test_all_modules_have_exceptions(self, modules):
        """Test all modules have exceptions.py"""
        missing = [m.name for m in modules if not (m / "domain" / "exceptions.py").exists()]
        if not missing:
            print("[PASS] All modules have domain/exceptions.py")
            self.tests_passed += 1
        else:
            print(f"[FAIL] Missing exceptions: {missing}")
            self.tests_failed += 1
            self.failed_tests.append(f"exceptions missing in {len(missing)} modules")

    def _test_routers_have_health(self, modules):
        """Test routers have /health endpoints"""
        missing = []
        for module in modules:
            router_file = module / "api" / "routers.py"
            if router_file.exists():
                content = router_file.read_text()
                if "/health" not in content:
                    missing.append(module.name)

        if not missing:
            print("[PASS] All routers have /health endpoints")
            self.tests_passed += 1
        else:
            print(f"[FAIL] No /health endpoints: {missing[:5]}...")
            self.tests_failed += 1
            self.failed_tests.append(f"/health missing in {len(missing)} routers")

    def _test_routers_have_fastapi(self, modules):
        """Test routers import FastAPI"""
        missing = []
        for module in modules:
            router_file = module / "api" / "routers.py"
            if router_file.exists():
                content = router_file.read_text()
                if "from fastapi" not in content:
                    missing.append(module.name)

        if not missing:
            print("[PASS] All routers import FastAPI")
            self.tests_passed += 1
        else:
            print(f"[FAIL] No FastAPI imports: {missing[:5]}...")
            self.tests_failed += 1
            self.failed_tests.append(f"FastAPI imports missing in {len(missing)} routers")

    def _test_port_adapter_pattern(self, modules):
        """Test Port/Adapter pattern"""
        missing = []
        for module in modules:
            adapter_file = module / "infrastructure" / "adapters.py"
            if adapter_file.exists():
                content = adapter_file.read_text()
                if "Port" not in content or "Adapter" not in content:
                    missing.append(module.name)

        if not missing:
            print("[PASS] Port/Adapter pattern implemented")
            self.tests_passed += 1
        else:
            print(f"[FAIL] Port/Adapter missing: {missing[:5]}...")
            self.tests_failed += 1
            self.failed_tests.append(f"Port/Adapter pattern incomplete in {len(missing)} modules")

    def _test_repository_pattern(self, modules):
        """Test Repository pattern"""
        missing = []
        for module in modules:
            repo_file = module / "infrastructure" / "repositories.py"
            if repo_file.exists():
                content = repo_file.read_text()
                if "Repository" not in content:
                    missing.append(module.name)

        if not missing:
            print("[PASS] Repository pattern implemented")
            self.tests_passed += 1
        else:
            print(f"[FAIL] Repository pattern missing: {missing[:5]}...")
            self.tests_failed += 1
            self.failed_tests.append(f"Repository pattern incomplete in {len(missing)} modules")

    def _test_required_directories(self, modules):
        """Test required directories exist"""
        missing_dirs = {}
        for module in modules:
            required = ["domain", "application", "infrastructure", "api"]
            missing = [d for d in required if not (module / d).exists()]
            if missing:
                missing_dirs[module.name] = missing

        if not missing_dirs:
            print("[PASS] All modules have required directories")
            self.tests_passed += 1
        else:
            print(f"[FAIL] Missing directories in {len(missing_dirs)} modules")
            self.tests_failed += 1
            self.failed_tests.append(f"directories missing in {len(missing_dirs)} modules")

    def _print_summary(self):
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed * 100) // total if total > 0 else 0

        print(f"\n{'=' * 80}")
        print(f"RESULTS: {self.tests_passed} PASSED, {self.tests_failed} FAILED ({percentage}%)")
        print(f"{'=' * 80}\n")

        if self.failed_tests:
            print("FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  - {test}")
            print()


if __name__ == "__main__":
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"

    if not modules_path.exists():
        print(f"[ERROR] Modules path not found: {modules_path}")
        sys.exit(1)

    validator = ModuleValidator(modules_path)
    validator.validate_all()
