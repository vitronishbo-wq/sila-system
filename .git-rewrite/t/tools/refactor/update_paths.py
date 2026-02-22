#!/usr/bin/env python3
"""🔁 SILA Path Refactor Orchestrator

Aplica, de forma segura, as regras definidas em migration/refactor_paths_v1.json
sobre o monorepo, com suporte a dry-run, logging e relatório consolidado.

Uso:
    python tools/refactor/update_paths.py --dry-run
    python tools/refactor/update_paths.py --apply
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
MIGRATION_FILE = ROOT / "migration" / "refactor_paths_v1.json"
REPORT_DIR = ROOT / "reports" / "refactor"


@dataclass
class Rule:
    id: str
    type: str  # "path_rewrite" | "text_replace"
    enabled: bool
    from_: str
    to: str
    scope: List[str]


def load_config() -> Dict[str, Any]:
    if not MIGRATION_FILE.exists():
        raise SystemExit(f"❌ Arquivo de migração não encontrado: {MIGRATION_FILE}")
    with MIGRATION_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_rules(cfg: Dict[str, Any]) -> List[Rule]:
    rules: List[Rule] = []
    for raw in cfg.get("rules", []):
        if not raw.get("enabled", True):
            continue
        rules.append(
            Rule(
                id=raw["id"],
                type=raw["type"],
                enabled=True,
                from_=raw["from"],
                to=raw["to"],
                scope=raw.get("scope", ["text"]),
            )
        )
    return rules


def iter_files(
    include_globs: Iterable[str], exclude_globs: Iterable[str]
) -> Iterable[Path]:
    all_files = ROOT.rglob("*")
    include_patterns = list(include_globs)
    exclude_patterns = list(exclude_globs)

    for path in all_files:
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        rel_str = str(rel)

        # Excluir primeiro
        if any(rel.match(pattern.replace("**/", "")) for pattern in exclude_patterns):
            continue

        # Incluir apenas se bater com algum include
        for pattern in include_patterns:
            if rel.match(pattern.replace("**/", "")) or rel_str.endswith(
                pattern.lstrip("*")
            ):
                yield path
                break


def apply_text_rules(
    path: Path, rules: List[Rule], dry_run: bool, report: Dict[str, Any]
) -> None:
    original = path.read_text(encoding="utf-8", errors="ignore")
    content = original
    file_changes: List[Dict[str, Any]] = []

    for rule in rules:
        if "text" not in rule.scope:
            continue
        if rule.from_ not in content:
            continue

        new_content, count = re.subn(re.escape(rule.from_), rule.to, content)
        if count:
            file_changes.append(
                {
                    "rule_id": rule.id,
                    "type": rule.type,
                    "occurrences": count,
                }
            )
            content = new_content

    if not file_changes:
        return

    rel = str(path.relative_to(ROOT))
    report.setdefault("files", {})[rel] = file_changes

    if not dry_run and content != original:
        path.write_text(content, encoding="utf-8")


def run(dry_run: bool) -> int:
    cfg = load_config()
    rules = build_rules(cfg)
    include_globs = cfg.get("include_globs", [])
    exclude_globs = cfg.get("exclude_globs", [])

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    summary: Dict[str, Any] = {
        "dry_run": dry_run,
        "rules_applied": [r.id for r in rules],
        "files": {},
    }

    print("🔁 SILA Path Refactor Orchestrator")
    print("=" * 60)
    print(f"📂 Raiz: {ROOT}")
    print(f"🧪 Dry-run: {dry_run}")
    print(f"📜 Regras ativas: {len(rules)}")

    files = list(iter_files(include_globs, exclude_globs))
    print(f"📁 Arquivos alvo: {len(files)}\n")

    for idx, path in enumerate(files, start=1):
        rel = path.relative_to(ROOT)
        print(f"[{idx}/{len(files)}] 🔍 {rel}")
        apply_text_rules(path, rules, dry_run, summary)

    # Persistir relatório
    report_file = REPORT_DIR / (
        "refactor_paths_v1.dryrun.json" if dry_run else "refactor_paths_v1.apply.json"
    )
    with report_file.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    changed_files = len(summary.get("files", {}))
    print("\n📊 Resumo:")
    print(f"   • Arquivos com alterações: {changed_files}")
    print(f"   • Relatório: {report_file}")

    if not changed_files:
        print("✅ Nenhuma alteração necessária para as regras configuradas.")
        return 0

    if dry_run:
        print("ℹ️  Nenhum arquivo foi modificado (dry-run). Use --apply para aplicar.")
    else:
        print("✅ Refactor aplicado. Revise com 'git diff' antes de commitar.")

    return 0


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="🔁 Aplica regras de refactor de paths definidas em migration/refactor_paths_v1.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula as alterações sem escrever em disco",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica efetivamente as alterações em disco",
    )

    args = parser.parse_args(argv)

    if not args.dry_run and not args.apply:
        print("⚠️  Nenhuma ação especificada. Use --dry-run ou --apply.")
        parser.print_help()
        raise SystemExit(1)

    dry_run = bool(args.dry_run and not args.apply)
    code = run(dry_run=dry_run)
    raise SystemExit(code)


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
