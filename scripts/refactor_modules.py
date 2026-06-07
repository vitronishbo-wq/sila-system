#!/usr/bin/env python3
"""Safe architecture refactors for SILA modules."""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_ROOTS = ("apps/backend/app/modules",)
REQUIRED_LAYERS = ("api", "application", "domain", "infrastructure")
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
class Action:
    kind: str
    path: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply safe, deterministic module architecture refactors.",
    )
    parser.add_argument(
        "--roots",
        nargs="+",
        default=list(DEFAULT_ROOTS),
        help="Module roots to process.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without modifying files.",
    )
    parser.add_argument(
        "--report-out",
        default="reports/architecture_refactor_report.json",
        help="Path for JSON report.",
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


def ensure_path(path: Path, dry_run: bool) -> bool:
    if path.exists():
        return False
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)
    return True


def ensure_file(path: Path, content: str, dry_run: bool) -> bool:
    if path.exists():
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


def build_parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return parent_map


def is_forbidden_target(target: str) -> bool:
    if target == "infrastructure" or target.startswith("infrastructure."):
        return True
    if target.endswith(".infrastructure") or ".infrastructure." in target:
        return True
    return False


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


def module_level_parent(node: ast.AST, parent_map: dict[ast.AST, ast.AST]) -> bool:
    return isinstance(parent_map.get(node), ast.Module)


def has_type_checking_import(lines: list[str]) -> bool:
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("from typing import") and "TYPE_CHECKING" in stripped:
            return True
    return False


def find_import_insertion_index(source: str, lines: list[str]) -> int:
    index = 0
    if lines and lines[0].startswith("#!"):
        index = 1
    if len(lines) > index and "coding" in lines[index]:
        index += 1

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return index

    if tree.body and isinstance(tree.body[0], ast.Expr):
        value = tree.body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            index = max(index, tree.body[0].end_lineno or index)

    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("from __future__ import"):
            index += 1
            continue
        break
    return index


def transform_forbidden_imports(domain_file: Path, dry_run: bool) -> tuple[list[Action], int]:
    actions: list[Action] = []
    try:
        source = domain_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return actions, 0

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        actions.append(
            Action(
                kind="skip_syntax_error",
                path=str(domain_file),
                detail=f"Cannot refactor; syntax error at line {exc.lineno}",
            )
        )
        return actions, 0

    parent_map = build_parent_map(tree)
    lines = source.splitlines()
    replacements: list[tuple[int, int, list[str]]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if not module_level_parent(node, parent_map):
            continue
        if is_guarded_by_type_checking(node, parent_map):
            continue

        targets: list[str] = []
        if isinstance(node, ast.Import):
            targets = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            targets = [node.module or ""]

        if not any(is_forbidden_target(target) for target in targets):
            continue

        start = node.lineno - 1
        end = (node.end_lineno or node.lineno) - 1
        original_block = lines[start : end + 1]
        replacement_block = ["if TYPE_CHECKING:"] + [f"    {line}" for line in original_block]
        replacements.append((start, end, replacement_block))

    if not replacements:
        return actions, 0

    updated_lines = list(lines)
    for start, end, replacement_block in sorted(
        replacements, key=lambda item: item[0], reverse=True
    ):
        updated_lines[start : end + 1] = replacement_block

    if not has_type_checking_import(updated_lines):
        insert_at = find_import_insertion_index(source, updated_lines)
        updated_lines.insert(insert_at, "from typing import TYPE_CHECKING")

    updated_content = "\n".join(updated_lines)
    if source.endswith("\n"):
        updated_content += "\n"

    if updated_content != source:
        if not dry_run:
            domain_file.write_text(updated_content, encoding="utf-8")
        actions.append(
            Action(
                kind="refactor_domain_import",
                path=str(domain_file),
                detail=f"Moved {len(replacements)} infrastructure import(s) under TYPE_CHECKING",
            )
        )
        return actions, len(replacements)

    return actions, 0


def process_module(module_dir: Path, dry_run: bool) -> list[Action]:
    actions: list[Action] = []

    if ensure_file(module_dir / "__init__.py", "", dry_run):
        actions.append(
            Action(
                kind="create_file",
                path=str(module_dir / "__init__.py"),
                detail="Created package marker",
            )
        )

    for layer in REQUIRED_LAYERS:
        layer_path = module_dir / layer
        if ensure_path(layer_path, dry_run):
            actions.append(
                Action(
                    kind="create_dir",
                    path=str(layer_path),
                    detail=f"Created missing layer '{layer}'",
                )
            )
        if ensure_file(layer_path / "__init__.py", "", dry_run):
            actions.append(
                Action(
                    kind="create_file",
                    path=str(layer_path / "__init__.py"),
                    detail="Created package marker",
                )
            )

    domain_dir = module_dir / "domain"
    if domain_dir.is_dir():
        for domain_file in sorted(domain_dir.rglob("*.py")):
            if is_ignored_dir(domain_file):
                continue
            refactor_actions, _ = transform_forbidden_imports(
                domain_file=domain_file, dry_run=dry_run
            )
            actions.extend(refactor_actions)

    return actions


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    roots = [Path(root).resolve() for root in args.roots]
    existing_roots = [root for root in roots if root.is_dir()]

    all_actions: list[Action] = []
    modules_scanned = 0
    for root in existing_roots:
        for module_dir in iter_module_dirs(root):
            modules_scanned += 1
            all_actions.extend(process_module(module_dir, dry_run=args.dry_run))

    print(f"Processed {modules_scanned} modules.")
    if not all_actions:
        print("No refactor actions were necessary.")
    else:
        print(f"Applied {len(all_actions)} refactor actions:")
        for action in all_actions:
            path = Path(action.path)
            pretty_path = (
                str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else action.path
            )
            print(f"- {action.kind}: {pretty_path} ({action.detail})")

    report = {
        "roots": [str(root.relative_to(repo_root)) for root in existing_roots],
        "modules_processed": modules_scanned,
        "dry_run": args.dry_run,
        "actions_count": len(all_actions),
        "actions": [asdict(action) for action in all_actions],
    }
    out_path = Path(args.report_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
