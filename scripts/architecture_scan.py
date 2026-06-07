#!/usr/bin/env python3
"""Architecture scanner for SILA DDD/Clean Architecture modules."""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_ROOTS = ("apps/backend/app/modules",)
REQUIRED_LAYERS = ("application", "domain", "infrastructure")
PRESENTATION_LAYERS = ("api", "presentation")
IGNORED_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}


@dataclass(frozen=True)
class Violation:
    kind: str
    module: str
    path: str
    detail: str
    line: int | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan backend modules for DDD/Clean Architecture violations.",
    )
    parser.add_argument(
        "--roots",
        nargs="+",
        default=list(DEFAULT_ROOTS),
        help="Module roots to scan.",
    )
    parser.add_argument(
        "--json-out",
        default="reports/architecture_scan_report.json",
        help="Path for JSON report.",
    )
    parser.add_argument(
        "--fail-on-violations",
        action="store_true",
        help="Return exit code 1 if at least one violation is found.",
    )
    parser.add_argument(
        "--include-type-checking",
        action="store_true",
        help="Count imports guarded by TYPE_CHECKING as violations.",
    )
    return parser.parse_args()


def is_ignored_dir(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def iter_module_dirs(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    module_dirs: list[Path] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in IGNORED_DIRS:
            continue
        module_dirs.append(child)
    return module_dirs


def is_forbidden_import(target: str) -> bool:
    if not target:
        return False
    if target == "infrastructure" or target.startswith("infrastructure."):
        return True
    if target.endswith(".infrastructure") or ".infrastructure." in target:
        return True
    return False


def build_parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return parent_map


def is_type_checking_expr(expr: ast.AST) -> bool:
    if isinstance(expr, ast.Name):
        return expr.id == "TYPE_CHECKING"
    if isinstance(expr, ast.Attribute):
        return (
            isinstance(expr.value, ast.Name)
            and expr.value.id == "typing"
            and expr.attr == "TYPE_CHECKING"
        )
    return False


def is_guarded_by_type_checking(node: ast.AST, parent_map: dict[ast.AST, ast.AST]) -> bool:
    current: ast.AST | None = node
    while current in parent_map:
        parent = parent_map[current]
        if (
            isinstance(parent, ast.If)
            and current in parent.body
            and is_type_checking_expr(parent.test)
        ):
            return True
        current = parent
    return False


def import_targets(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        base = node.module or ""
        return [base]
    return []


def scan_domain_imports(
    module_dir: Path,
    repo_root: Path,
    include_type_checking: bool,
) -> list[Violation]:
    violations: list[Violation] = []
    domain_dir = module_dir / "domain"
    if not domain_dir.is_dir():
        return violations

    for py_file in sorted(domain_dir.rglob("*.py")):
        if is_ignored_dir(py_file):
            continue
        try:
            source = py_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            violations.append(
                Violation(
                    kind="invalid_python",
                    module=module_dir.name,
                    path=str(py_file.relative_to(repo_root)),
                    detail=f"Syntax error: {exc.msg}",
                    line=exc.lineno,
                )
            )
            continue

        parent_map = build_parent_map(tree)
        lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue

            if not include_type_checking and is_guarded_by_type_checking(node, parent_map):
                continue

            for target in import_targets(node):
                if not is_forbidden_import(target):
                    continue
                lineno = getattr(node, "lineno", None)
                excerpt = ""
                if lineno is not None and 1 <= lineno <= len(lines):
                    excerpt = lines[lineno - 1].strip()
                violations.append(
                    Violation(
                        kind="domain_imports_infrastructure",
                        module=module_dir.name,
                        path=str(py_file.relative_to(repo_root)),
                        detail=excerpt or f"forbidden import target '{target}'",
                        line=lineno,
                    )
                )
    return violations


def scan_module_structure(module_dir: Path, repo_root: Path) -> list[Violation]:
    violations: list[Violation] = []

    # Check fixed required layers
    for layer in REQUIRED_LAYERS:
        layer_path = module_dir / layer
        if not layer_path.is_dir():
            violations.append(
                Violation(
                    kind="missing_layer",
                    module=module_dir.name,
                    path=str(module_dir.relative_to(repo_root)),
                    detail=f"missing {layer}",
                    line=None,
                )
            )

    # Check at least one presentation layer exists
    has_presentation = any((module_dir / p).is_dir() for p in PRESENTATION_LAYERS)
    if not has_presentation:
        violations.append(
            Violation(
                kind="missing_layer",
                module=module_dir.name,
                path=str(module_dir.relative_to(repo_root)),
                detail="missing presentation layer (expected 'api' or 'presentation')",
                line=None,
            )
        )

    return violations


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    roots = [Path(root).resolve() for root in args.roots]

    module_dirs: list[Path] = []
    existing_roots = [root for root in roots if root.is_dir()]
    for root in existing_roots:
        module_dirs.extend(iter_module_dirs(root))

    violations: list[Violation] = []
    for module_dir in module_dirs:
        violations.extend(scan_module_structure(module_dir, repo_root))
        violations.extend(
            scan_domain_imports(
                module_dir=module_dir,
                repo_root=repo_root,
                include_type_checking=args.include_type_checking,
            )
        )

    violations.sort(key=lambda item: (item.module, item.kind, item.path, item.line or 0))

    print(f"Scanned {len(module_dirs)} modules across {len(existing_roots)} roots.")
    if not violations:
        print("Violations: none")
    else:
        print("Violations:")
        for item in violations:
            location = item.path
            if item.line is not None:
                location = f"{location}:{item.line}"
            print(f"- {item.module}: {item.kind} -> {item.detail} ({location})")

    report = {
        "roots": [str(root.relative_to(repo_root)) for root in existing_roots],
        "modules_scanned": len(module_dirs),
        "required_layers": list(REQUIRED_LAYERS),
        "violations_count": len(violations),
        "violations": [asdict(item) for item in violations],
    }
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report written to {out_path}")

    if args.fail_on_violations and violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
