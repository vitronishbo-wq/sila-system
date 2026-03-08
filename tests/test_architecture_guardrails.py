from __future__ import annotations

import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_APP = REPO_ROOT / "apps" / "backend" / "app"
MODULES_ROOT = BACKEND_APP / "modules"
TEST_ROOTS = (
    REPO_ROOT / "tests",
    REPO_ROOT / "apps" / "backend" / "tests",
    REPO_ROOT / "apps" / "backend" / "app" / "modules",
)
ALLOWED_LEGACY_APP_CITIZEN_IMPORTS_IN_TESTS = set()


ALLOWED_CROSS_MODULE_IMPORTS: set[tuple[str, str, str]] = set()


def _iter_python_files(root: Path):
    for path in root.rglob("*.py"):
        # Guardrails should enforce production code boundaries.
        if "/tests/" in path.as_posix():
            continue
        yield path


def _collect_cross_module_imports() -> set[tuple[str, str, str]]:
    violations: set[tuple[str, str, str]] = set()
    for path in _iter_python_files(MODULES_ROOT):
        owner = path.relative_to(MODULES_ROOT).parts[0]
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("app.modules."):
                parts = node.module.split(".")
                if len(parts) > 2:
                    target = parts[2]
                    if target != owner:
                        rel = path.relative_to(MODULES_ROOT).as_posix()
                        violations.add((rel, owner, target))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if not alias.name.startswith("app.modules."):
                        continue
                    parts = alias.name.split(".")
                    if len(parts) > 2:
                        target = parts[2]
                        if target != owner:
                            rel = path.relative_to(MODULES_ROOT).as_posix()
                            violations.add((rel, owner, target))
    return violations


def test_no_run_sync_in_backend_app():
    hits = []
    for path in _iter_python_files(BACKEND_APP):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "run_sync(" in text:
            hits.append(path.relative_to(BACKEND_APP).as_posix())

    assert not hits, f"run_sync found in backend app: {hits}"


def test_no_sync_session_in_workflow_and_operations():
    targets = [
        MODULES_ROOT / "workflow",
        MODULES_ROOT / "operations",
    ]
    hits = []
    for target in targets:
        for path in _iter_python_files(target):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "from sqlalchemy.orm import Session" in text:
                hits.append(path.relative_to(BACKEND_APP).as_posix())
    assert not hits, f"Synchronous SQLAlchemy Session import found: {hits}"


def test_no_legacy_app_citizen_imports_in_backend_app():
    hits = []
    for path in _iter_python_files(BACKEND_APP):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "from app.citizen" in text or "import app.citizen" in text:
            hits.append(path.relative_to(BACKEND_APP).as_posix())
    assert not hits, f"Legacy app.citizen imports found: {hits}"


def test_no_legacy_app_citizen_imports_in_tests():
    hits = set()
    for root in TEST_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("app.citizen"):
                    hits.add(path.relative_to(REPO_ROOT).as_posix())
                elif isinstance(node, ast.Import):
                    if any(alias.name.startswith("app.citizen") for alias in node.names):
                        hits.add(path.relative_to(REPO_ROOT).as_posix())
    unexpected = sorted(hits - ALLOWED_LEGACY_APP_CITIZEN_IMPORTS_IN_TESTS)
    assert not unexpected, (
        "New legacy app.citizen imports found in tests/modules: "
        f"{unexpected}"
    )


def test_cross_module_imports_do_not_expand():
    current = _collect_cross_module_imports()
    unexpected = sorted(current - ALLOWED_CROSS_MODULE_IMPORTS)
    assert not unexpected, (
        "New cross-module imports detected; route dependencies through core abstractions: "
        f"{unexpected}"
    )


def test_identity_consolidation_blocks_direct_citizen_imports_from_identity():
    allowed_files = {
        (BACKEND_APP / "core" / "bridges" / "civil_identity_bridge.py").resolve(),
    }
    blocked_modules = (
        "app.modules.justice.civil_registry.application.services.citizen_service",
        "app.modules.justice.civil_registry.domain.models.citizen",
        "app.modules.justice.civil_registry.infrastructure.models.citizen_model",
        "app.modules.justice.civil_registry.infrastructure.repositories.citizen_repository",
    )
    hits: list[str] = []
    for path in _iter_python_files(BACKEND_APP):
        resolved = path.resolve()
        rel = path.relative_to(BACKEND_APP).as_posix()
        if rel.startswith("modules/justice/civil_registry/"):
            continue
        if resolved in allowed_files:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if any(node.module.startswith(prefix) for prefix in blocked_modules):
                    hits.append(rel)
            elif isinstance(node, ast.Import):
                if any(
                    any(alias.name.startswith(prefix) for prefix in blocked_modules)
                    for alias in node.names
                ):
                    hits.append(rel)
    assert not hits, (
        "Identity consolidation violated: direct imports from "
        "identity citizen internals found outside bridge/module: "
        f"{sorted(set(hits))}"
    )


def test_compat_citizen_repositories_delegate_to_canonical_identity_adapter():
    compatibility_files = [
        BACKEND_APP / "modules" / "identity" / "infrastructure" / "repositories" / "citizen_repository.py",
        BACKEND_APP / "infrastructure" / "repositories" / "citizen_repository.py",
    ]
    canonical_import = "from app.core.bridges.citizen_repository_bridge import CitizenRepository as CanonicalCitizenRepository"
    for path in compatibility_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(BACKEND_APP).as_posix()
        assert canonical_import in text, (
            f"{rel} must delegate to canonical identity citizen repository adapter"
        )
        assert "select(" not in text, (
            f"{rel} contains direct SQL logic; keep SQL only in canonical identity adapter"
        )
