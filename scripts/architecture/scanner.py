"""Module scanner for SILA architecture analysis."""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

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
REQUIRED_LAYERS = ("api", "application", "domain", "infrastructure")
MODULE_IMPORT_RE = re.compile(r"^app\.modules\.([a-zA-Z0-9_]+)")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


@dataclass(frozen=True)
class ImportEdge:
    source: str
    target: str
    count: int
    evidence: list[str]


@dataclass
class ModuleScan:
    name: str
    path: str
    layers_present: dict[str, bool]
    files_scanned: int = 0
    entities: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    repositories: list[str] = field(default_factory=list)
    routers: list[str] = field(default_factory=list)
    concept_tokens: list[str] = field(default_factory=list)
    imports_out: dict[str, int] = field(default_factory=dict)
    import_evidence: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["entities"] = sorted(set(self.entities))
        payload["services"] = sorted(set(self.services))
        payload["repositories"] = sorted(set(self.repositories))
        payload["routers"] = sorted(set(self.routers))
        payload["concept_tokens"] = sorted(set(self.concept_tokens))
        payload["imports_out"] = dict(sorted(self.imports_out.items()))
        payload["import_evidence"] = {
            key: sorted(values) for key, values in sorted(self.import_evidence.items())
        }
        return payload


def _is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def _module_dirs(modules_root: Path) -> list[Path]:
    if not modules_root.is_dir():
        return []
    dirs: list[Path] = []
    for child in sorted(modules_root.iterdir()):
        if child.is_dir() and child.name not in IGNORED_DIRS and not child.name.startswith("."):
            dirs.append(child)
    return dirs


def _extract_import_target(import_path: str) -> str | None:
    match = MODULE_IMPORT_RE.match(import_path)
    if not match:
        return None
    return match.group(1)


def _safe_parse(path: Path) -> ast.AST | None:
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    try:
        return ast.parse(content, filename=str(path))
    except SyntaxError:
        return None


def _layer_for_file(rel_path: Path) -> str | None:
    if not rel_path.parts:
        return None
    top = rel_path.parts[0]
    return top if top in REQUIRED_LAYERS else None


def _is_entity_file(rel_path: Path) -> bool:
    text = rel_path.as_posix()
    return text.startswith("domain/") and (
        "/entities/" in text or text.endswith("entities.py") or "/models/" in text
    )


def _is_service_file(rel_path: Path) -> bool:
    text = rel_path.as_posix()
    return (
        text.startswith("application/")
        and ("/services/" in text or text.endswith("services.py") or text.endswith("service.py"))
    ) or text.startswith("domain/services")


def _is_repository_file(rel_path: Path) -> bool:
    text = rel_path.as_posix()
    return (
        "/repositories/" in text
        or text.endswith("repository.py")
        or text.endswith("repositories.py")
    )


def _is_router_file(rel_path: Path) -> bool:
    text = rel_path.as_posix()
    name = rel_path.name
    return text.startswith("api/") and (
        name == "router.py" or name.endswith("_router.py") or name.endswith("routers.py")
    )


def _tokenize_identifier(identifier: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(identifier) if token]


def _scan_module(module_dir: Path, modules_root: Path) -> ModuleScan:
    rel_module = module_dir.relative_to(modules_root)
    layers_present = {layer: (module_dir / layer).is_dir() for layer in REQUIRED_LAYERS}
    scan = ModuleScan(name=module_dir.name, path=str(rel_module), layers_present=layers_present)

    imports_counter: dict[str, int] = {}
    import_evidence: dict[str, list[str]] = {}

    for py_file in sorted(module_dir.rglob("*.py")):
        rel_path = py_file.relative_to(module_dir)
        if _is_ignored(rel_path):
            continue

        tree = _safe_parse(py_file)
        if tree is None:
            continue

        scan.files_scanned += 1
        is_entity_file = _is_entity_file(rel_path)
        is_service_file = _is_service_file(rel_path)
        is_repo_file = _is_repository_file(rel_path)
        is_router_file = _is_router_file(rel_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                scan.concept_tokens.extend(_tokenize_identifier(node.name))

                if is_entity_file or node.name.endswith(("Entity", "Aggregate", "ValueObject")):
                    scan.entities.append(node.name)

                if is_repo_file or node.name.endswith("Repository"):
                    scan.repositories.append(node.name)

                if is_service_file or node.name.endswith("Service"):
                    scan.services.append(node.name)

                if is_router_file and node.name.endswith("Router"):
                    scan.routers.append(node.name)

            elif isinstance(node, ast.FunctionDef):
                scan.concept_tokens.extend(_tokenize_identifier(node.name))
                if is_service_file and node.name.startswith(
                    ("create", "update", "delete", "list", "get")
                ):
                    scan.services.append(node.name)

            elif isinstance(node, ast.AsyncFunctionDef):
                scan.concept_tokens.extend(_tokenize_identifier(node.name))
                if is_router_file:
                    scan.routers.append(node.name)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    target = _extract_import_target(alias.name)
                    if not target or target == scan.name:
                        continue
                    imports_counter[target] = imports_counter.get(target, 0) + 1
                    import_evidence.setdefault(target, [])
                    if len(import_evidence[target]) < 5:
                        import_evidence[target].append(
                            f"{rel_path}:{node.lineno} import {alias.name}"
                        )

            elif isinstance(node, ast.ImportFrom):
                if not node.module:
                    continue
                target = _extract_import_target(node.module)
                if not target or target == scan.name:
                    continue
                imports_counter[target] = imports_counter.get(target, 0) + 1
                import_evidence.setdefault(target, [])
                if len(import_evidence[target]) < 5:
                    import_evidence[target].append(
                        f"{rel_path}:{node.lineno} from {node.module} import ..."
                    )

    scan.imports_out = imports_counter
    scan.import_evidence = import_evidence
    scan.concept_tokens.extend(_tokenize_identifier(scan.name))

    return scan


def scan_modules(modules_root: Path) -> dict[str, ModuleScan]:
    module_dirs = _module_dirs(modules_root)
    scans = {_dir.name: _scan_module(_dir, modules_root) for _dir in module_dirs}
    return dict(sorted(scans.items()))


def collect_edges(scans: dict[str, ModuleScan]) -> list[ImportEdge]:
    edges: list[ImportEdge] = []
    module_names = set(scans)
    for source, scan in sorted(scans.items()):
        for target, count in sorted(scan.imports_out.items()):
            if target not in module_names:
                continue
            evidence = scan.import_evidence.get(target, [])
            edges.append(ImportEdge(source=source, target=target, count=count, evidence=evidence))
    return edges
