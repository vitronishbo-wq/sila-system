#!/usr/bin/env python3
"""Guardrail: ensure AI bootstrap/context stack exists and is scoped correctly."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_FILES = (
    "docs/tree.md",
    "docs/AI_BOOTSTRAP_PROMPT.md",
    "docs/AI_CONTEXT.md",
    "docs/architecture/domain_dependency_policy.yaml",
    "docs/architecture/REPOSITORY_MAP.yaml",
    "docs/architecture/entrypoints/SYSTEM_OVERVIEW.md",
    "docs/architecture/entrypoints/BACKEND_ARCHITECTURE.md",
    "docs/architecture/entrypoints/DOMAIN_MAP.md",
    "docs/architecture/entrypoints/API_ENTRYPOINTS.md",
    "docs/architecture/entrypoints/DATA_FLOW.md",
    "docs/architecture/domains/governance/ARCHITECTURE.md",
    "docs/architecture/domains/economy/ARCHITECTURE.md",
    "docs/architecture/domains/social/ARCHITECTURE.md",
    "docs/architecture/domains/infrastructure/ARCHITECTURE.md",
    "docs/architecture/domains/environment/ARCHITECTURE.md",
    "docs/architecture/domains/security/ARCHITECTURE.md",
    "docs/architecture/domains/identity/ARCHITECTURE.md",
    "docs/architecture/domains/core_system/ARCHITECTURE.md",
    "ARCHITECTURE_INDEX.yaml",
    "ARCHITECTURE_DEPENDENCIES.yaml",
    "API_MAP.yaml",
    "AI_ENTRYPOINTS.yaml",
    "docs/AI_ARCHITECTURE_GRAPH.yaml",
    "docs/AI_DOMAIN_KERNEL.md",
    "reports/ai_architecture_graph_visual_report.md",
    "reports/ai_domain_kernel_visual_report.md",
    "reports/module_architecture_docs_visual_report.md",
    "scripts/ai/bootstrap_context.sh",
    "scripts/ai/generate_module_architecture_docs.py",
    "scripts/ai/generate_architecture_graph.py",
    "scripts/ai/generate_ai_domain_kernel.py",
    "scripts/guardrails/check_domain_dependencies.py",
    "scripts/arch_compiler.py",
    "scripts/guardrails/run_all_guardrails.sh",
    "AI_FILE_SCOPE.yaml",
)

REQUIRED_SCOPE_INCLUDE = (
    "docs/tree.md",
    "docs/AI_BOOTSTRAP_PROMPT.md",
    "docs/AI_CONTEXT.md",
    "docs/architecture/**",
    "ARCHITECTURE_INDEX.yaml",
    "ARCHITECTURE_DEPENDENCIES.yaml",
    "API_MAP.yaml",
    "AI_ENTRYPOINTS.yaml",
    "docs/AI_ARCHITECTURE_GRAPH.yaml",
    "docs/AI_DOMAIN_KERNEL.md",
    "scripts/architecture/**",
    "scripts/arch_compiler.py",
    "scripts/guardrails/**",
    "scripts/ai/bootstrap_context.sh",
    "scripts/ai/generate_module_architecture_docs.py",
    "scripts/ai/generate_architecture_graph.py",
    "scripts/ai/generate_ai_domain_kernel.py",
    "apps/backend/app/modules/*/ARCHITECTURE.md",
)

DISALLOWED_REDUNDANT_FILES = (
    "docs/architecture/SILA_DOMAIN_MAP.md",
)


def parse_list_lines(lines: list[str], key: str) -> list[str]:
    values: list[str] = []
    in_key = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            in_key = (line[:-1] == key)
            continue
        if in_key and line.lstrip().startswith("- "):
            values.append(line.split("- ", 1)[1].strip())
        elif in_key and not line.startswith(" "):
            in_key = False
    return values


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate AI bootstrap/context artifacts and scope include list."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    modules_root = repo_root / "apps" / "backend" / "app" / "modules"
    missing_files: list[str] = []
    empty_files: list[str] = []
    for rel in REQUIRED_FILES:
        path = repo_root / rel
        if not path.exists():
            missing_files.append(rel)
            continue
        if path.is_file() and path.stat().st_size == 0:
            empty_files.append(rel)

    missing_module_arch_docs: list[str] = []
    missing_module_manifests: list[str] = []
    if modules_root.exists():
        for module_dir in sorted(modules_root.iterdir(), key=lambda p: p.name):
            if not module_dir.is_dir() or module_dir.name.startswith("__"):
                continue
            arch_doc = module_dir / "ARCHITECTURE.md"
            module_manifest = module_dir / "module.yaml"
            if not module_manifest.exists():
                missing_module_manifests.append(
                    f"apps/backend/app/modules/{module_dir.name}/module.yaml"
                )
            if not arch_doc.exists():
                missing_module_arch_docs.append(
                    f"apps/backend/app/modules/{module_dir.name}/ARCHITECTURE.md"
                )
            elif arch_doc.stat().st_size == 0:
                empty_files.append(
                    f"apps/backend/app/modules/{module_dir.name}/ARCHITECTURE.md"
                )

    scope_file = repo_root / "AI_FILE_SCOPE.yaml"
    missing_scope_items: list[str] = []
    if scope_file.exists():
        content = scope_file.read_text(encoding="utf-8")
        include_values = parse_list_lines(content.splitlines(), "include")
        include_set = set(include_values)
        for item in REQUIRED_SCOPE_INCLUDE:
            if item not in include_set:
                missing_scope_items.append(item)
    else:
        missing_scope_items.extend(REQUIRED_SCOPE_INCLUDE)

    redundant_files = [
        rel for rel in DISALLOWED_REDUNDANT_FILES if (repo_root / rel).exists()
    ]

    if (
        not missing_files
        and not empty_files
        and not missing_scope_items
        and not redundant_files
        and not missing_module_arch_docs
        and not missing_module_manifests
    ):
        print("OK: AI bootstrap/context stack is complete and scoped.")
        return 0

    print("AI bootstrap/context stack issues detected:")
    if missing_files:
        print("- Missing files:")
        for item in missing_files:
            print(f"  - {item}")
    if empty_files:
        print("- Empty files:")
        for item in empty_files:
            print(f"  - {item}")
    if missing_scope_items:
        print("- Missing include entries in AI_FILE_SCOPE.yaml:")
        for item in missing_scope_items:
            print(f"  - {item}")
    if missing_module_arch_docs:
        print("- Missing module architecture docs:")
        for item in missing_module_arch_docs:
            print(f"  - {item}")
    if missing_module_manifests:
        print("- Missing module manifests:")
        for item in missing_module_manifests:
            print(f"  - {item}")
    if redundant_files:
        print("- Redundant files detected (remove to avoid duplicate architecture sources):")
        for item in redundant_files:
            print(f"  - {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
