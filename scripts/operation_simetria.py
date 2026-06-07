from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES_DIR = ROOT / "apps" / "backend" / "app" / "modules"
REPORT_DIR = ROOT / "reports"

DDD_DIRS = ("api", "application", "domain", "infrastructure", "tests")
LIFECYCLE_STUB = """

HealthStatus = dict


async def startup() -> None:
    return None


async def shutdown() -> None:
    return None


def health_check() -> HealthStatus:
    return {"status": "ok"}
""".lstrip("\n")

API_ROUTER_STUB = """from fastapi import APIRouter
from .health import router as health_router

router = APIRouter(prefix="/{module}", tags=["{module_cap}"])
router.include_router(health_router)
"""

API_HEALTH_STUB = """from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {{"status": "ok", "module": "{module}"}}
"""


@dataclass
class ModuleReport:
    name: str
    had_core_only: bool
    created_dirs: list[str]
    created_files: list[str]
    lifecycle_added: bool


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_file(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def ensure_lifecycle_hooks(init_path: Path) -> bool:
    if not init_path.exists():
        init_path.write_text(LIFECYCLE_STUB, encoding="utf-8")
        return True
    content = init_path.read_text(encoding="utf-8")
    needs = []
    if "async def startup" not in content:
        needs.append("startup")
    if "async def shutdown" not in content:
        needs.append("shutdown")
    if "def health_check" not in content:
        needs.append("health_check")
    if "HealthStatus" not in content:
        needs.append("HealthStatus")
    if not needs:
        return False
    init_path.write_text(content.rstrip() + "\n\n" + LIFECYCLE_STUB, encoding="utf-8")
    return True


def is_core_only(module_path: Path) -> bool:
    if not (module_path / "core").exists():
        return False
    return all(not (module_path / d).exists() for d in DDD_DIRS)


def create_ddd_skeleton(module_path: Path, module_name: str) -> tuple[list[str], list[str]]:
    created_dirs: list[str] = []
    created_files: list[str] = []
    for ddd_dir in DDD_DIRS:
        dir_path = module_path / ddd_dir
        if not dir_path.exists():
            ensure_dir(dir_path)
            created_dirs.append(str(dir_path))
        init_file = dir_path / "__init__.py"
        if ensure_file(init_file, f'"""{module_name} {ddd_dir} package."""\n'):
            created_files.append(str(init_file))
    # API stubs
    api_dir = module_path / "api"
    if api_dir.exists():
        router_path = api_dir / "router.py"
        health_path = api_dir / "health.py"
        module_cap = module_name.replace("_", " ").title().replace(" ", "")
        if ensure_file(
            router_path, API_ROUTER_STUB.format(module=module_name, module_cap=module_cap)
        ):
            created_files.append(str(router_path))
        if ensure_file(health_path, API_HEALTH_STUB.format(module=module_name)):
            created_files.append(str(health_path))
    # Tests structure
    tests_dir = module_path / "tests"
    for sub in ("unit", "integration"):
        sub_dir = tests_dir / sub
        if not sub_dir.exists():
            ensure_dir(sub_dir)
            created_dirs.append(str(sub_dir))
        init_file = sub_dir / "__init__.py"
        if ensure_file(init_file, f'"""{module_name} {sub} tests."""\n'):
            created_files.append(str(init_file))
    return created_dirs, created_files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Operacao Simetria - DDD skeleton + lifecycle hooks."
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes.")
    args = parser.parse_args()

    report: list[ModuleReport] = []
    skip_names = {"__pycache__", "api"}
    for module_path in sorted(MODULES_DIR.iterdir()):
        if not module_path.is_dir():
            continue
        if module_path.name in skip_names or module_path.name.startswith("."):
            continue
        if not (module_path / "module.yaml").exists():
            if not any(
                (module_path / d).exists()
                for d in ("api", "application", "domain", "infrastructure", "core")
            ):
                continue
        module_name = module_path.name
        core_only = is_core_only(module_path)
        created_dirs: list[str] = []
        created_files: list[str] = []
        lifecycle_added = False
        if args.apply and core_only:
            created_dirs, created_files = create_ddd_skeleton(module_path, module_name)
        if args.apply:
            init_path = module_path / "__init__.py"
            lifecycle_added = ensure_lifecycle_hooks(init_path)
        report.append(
            ModuleReport(
                name=module_name,
                had_core_only=core_only,
                created_dirs=created_dirs,
                created_files=created_files,
                lifecycle_added=lifecycle_added,
            )
        )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    json_path = REPORT_DIR / f"operation_simetria_{stamp}.json"
    json_path.write_text(json.dumps([asdict(r) for r in report], indent=2), encoding="utf-8")
    md_path = REPORT_DIR / f"operation_simetria_{stamp}.md"
    lines = [
        "# Operacao Simetria - Relatorio",
        "",
        f"- Timestamp (UTC): {datetime.utcnow().isoformat()}",
        f"- Modulos analisados: {len(report)}",
        f"- Core-only detectados: {sum(1 for r in report if r.had_core_only)}",
        f"- Lifecycle hooks adicionados: {sum(1 for r in report if r.lifecycle_added)}",
        "",
        "| Modulo | Core-only | Lifecycle hooks | Dirs criados | Files criados |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in report:
        lines.append(
            f"| {r.name} | {'yes' if r.had_core_only else 'no'} | {'yes' if r.lifecycle_added else 'no'} | {len(r.created_dirs)} | {len(r.created_files)} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
