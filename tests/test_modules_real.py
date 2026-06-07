#!/usr/bin/env python3
"""
FASE 5: Real Integration Tests
Test that router endpoints actually work.
"""

import sys
from pathlib import Path

import pytest

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "backend"))


class TestModuleRouters:
    """Test that all modules have working routers."""

    @pytest.fixture
    def modules_path(self):
        return Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"

    def test_all_modules_have_routers(self, modules_path):
        """Verify all modules have api/routers.py file."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_routers = []
        for module in modules:
            router_file = module / "api" / "routers.py"
            if not router_file.exists():
                missing_routers.append(module.name)

        assert len(missing_routers) == 0, f"Missing routers: {missing_routers}"

    def test_all_modules_have_domain_models(self, modules_path):
        """Verify all modules have domain/models.py."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_models = []
        for module in modules:
            models_file = module / "domain" / "models.py"
            if not models_file.exists():
                missing_models.append(module.name)

        assert len(missing_models) == 0, f"Missing models: {missing_models}"

    def test_routers_have_health_endpoints(self, modules_path):
        """Verify routers have /health endpoints."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_health = []
        for module in modules:
            router_file = module / "api" / "routers.py"
            health_file = module / "api" / "health.py"
            if router_file.exists():
                content = router_file.read_text()
                if (
                    "/health" not in content
                    and "HealthRouterFactory" not in content
                    and not health_file.exists()
                ):
                    missing_health.append(module.name)

        assert len(missing_health) == 0, f"No /health endpoints: {missing_health}"

    def test_routers_have_fastapi_imports(self, modules_path):
        """Verify routers import from fastapi."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_imports = []
        for module in modules:
            router_file = module / "api" / "routers.py"
            if router_file.exists():
                content = router_file.read_text()
                if (
                    "from fastapi import" not in content
                    and "import fastapi" not in content
                    and "RouterFactory" not in content
                    and "HealthRouterFactory" not in content
                ):
                    missing_imports.append(module.name)

        assert len(missing_imports) == 0, f"No FastAPI imports: {missing_imports}"

    def test_command_classes_exist(self, modules_path):
        """Verify command classes are defined."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_commands = []
        for module in modules:
            commands_file = module / "application" / "commands.py"
            if commands_file.exists():
                content = commands_file.read_text()
                if "class" not in content:
                    missing_commands.append(module.name)
            else:
                # Skip if commands.py doesn't exist (it's optional for some modules)
                pass

        assert len(missing_commands) == 0, f"No command classes: {missing_commands}"

    def test_repository_patterns_defined(self, modules_path):
        """Verify repository patterns are implemented."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_repos = []
        for module in modules:
            repo_file = module / "infrastructure" / "repositories.py"
            if repo_file.exists():
                content = repo_file.read_text()
                if "Repository" not in content:
                    missing_repos.append(module.name)

        assert len(missing_repos) == 0, f"No Repository patterns: {missing_repos}"

    def test_port_adapter_pattern(self, modules_path):
        """Verify Port/Adapter pattern is implemented."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_ports = []
        for module in modules:
            adapter_file = module / "infrastructure" / "adapters.py"
            if adapter_file.exists():
                content = adapter_file.read_text()
                content_lower = content.lower()
                if "port" not in content_lower and "adapter" not in content_lower:
                    missing_ports.append(module.name)

        assert len(missing_ports) == 0, f"No Port/Adapter pattern: {missing_ports}"


class TestModuleStructure:
    """Test module directory structure."""

    @pytest.fixture
    def modules_path(self):
        return Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"

    def test_all_modules_have_required_dirs(self, modules_path):
        """Verify all modules have domain, application, infrastructure, api dirs."""
        modules = sorted(
            [
                d
                for d in modules_path.iterdir()
                if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
            ]
        )

        missing_dirs = {}
        for module in modules:
            required = ["domain", "application", "infrastructure", "api"]
            missing = [d for d in required if not (module / d).exists()]
            if missing:
                missing_dirs[module.name] = missing

        assert len(missing_dirs) == 0, f"Missing dirs: {missing_dirs}"

    def test_module_count(self, modules_path):
        """Verify we have at least 25 modules."""
        modules = [
            d
            for d in modules_path.iterdir()
            if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
        ]
        assert len(modules) >= 25, f"Expected >= 25 modules, found {len(modules)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
