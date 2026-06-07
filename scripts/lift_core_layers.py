from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "apps" / "backend" / "app" / "modules"
REPORT_DIR = ROOT / "reports"

LAYERS = ("api", "application", "domain", "infrastructure", "tests")


@dataclass
class MoveAction:
    module: str
    layer: str
    moved_items: list[str]


def is_effectively_empty(path: Path) -> bool:
    if not path.exists():
        return True
    for child in path.iterdir():
        if child.name in {"__pycache__", "__init__.py"}:
            continue
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Move core/* into DDD layers when safe.")
    parser.add_argument("--apply", action="store_true", help="Apply moves.")
    args = parser.parse_args()

    actions: list[MoveAction] = []
    for module_path in sorted(MODULES_DIR.iterdir()):
        if not module_path.is_dir():
            continue
        core_dir = module_path / "core"
        if not core_dir.exists():
            continue
        for layer in LAYERS:
            src = core_dir / layer
            if not src.exists():
                continue
            dest = module_path / layer
            if not is_effectively_empty(src):
                if is_effectively_empty(dest):
                    if args.apply:
                        dest.mkdir(parents=True, exist_ok=True)
                        moved: list[str] = []
                        for item in src.iterdir():
                            target = dest / item.name
                            shutil.move(str(item), str(target))
                            moved.append(str(target))
                        actions.append(MoveAction(module_path.name, layer, moved))
                # else: skip to avoid overwriting existing structure
        if args.apply and is_effectively_empty(core_dir):
            try:
                core_dir.rmdir()
            except OSError:
                pass

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"lift_core_layers_{stamp}.json"
    json_path.write_text(json.dumps([asdict(a) for a in actions], indent=2), encoding="utf-8")
    md_path = REPORT_DIR / f"lift_core_layers_{stamp}.md"
    lines = [
        "# Lift Core Layers - Relatorio",
        "",
        f"- Timestamp (UTC): {datetime.utcnow().isoformat()}",
        f"- Acoes executadas: {len(actions)}",
        "",
        "| Modulo | Layer | Itens movidos |",
        "| --- | --- | --- |",
    ]
    for action in actions:
        lines.append(f"| {action.module} | {action.layer} | {len(action.moved_items)} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
