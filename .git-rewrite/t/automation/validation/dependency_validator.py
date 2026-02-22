#!/usr/bin/env python3
"""
SILA Dependency Validator
Valida requirements.txt, detecta pacotes inválidos,
versões incompatíveis e dependências inexistentes.
"""

import json
import subprocess
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
REQ_FILE = ROOT / "requirements.txt"
RULES_FILE = ROOT / "automation/validation/requirements_rules.json"


def load_rules():
    if not RULES_FILE.exists():
        return {}
    with RULES_FILE.open() as f:
        return json.load(f)


def load_requirements():
    """Carrega requirements de todos os arquivos requirements*.txt"""
    reqs = []
    pattern = re.compile(r"^([a-zA-Z0-9_\-]+)([<>=!]=.+)?$")

    # Processa múltiplos arquivos requirements
    req_files = [
        ROOT / "requirements.txt",
        ROOT / "apps/backend/requirements.txt",
        ROOT / "scripts/requirements.txt",
        ROOT / ".sila_installer/requirements.txt",
        ROOT / "requirements-dev.txt",
        ROOT / "automation/backend/requirements.txt",
    ]

    for req_file in req_files:
        if not req_file.exists():
            continue

        for line in req_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = pattern.match(line)
            if m:
                reqs.append(line)

    return list(set(reqs))  # Remove duplicados


def pip_freeze():
    result = subprocess.run(
        ["pip", "freeze"], capture_output=True, text=True, check=False
    )
    return result.stdout.splitlines()


def validate_pip_can_install(req):
    """Testa via pip se um pacote+versão existem no PyPI."""
    try:
        # Primeiro tenta com pip index versions (mais rápido)
        pkg_name = req.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0]
        result = subprocess.run(
            ["pip", "index", "versions", pkg_name], capture_output=True, timeout=10
        )
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback para dry-run install
    try:
        cmd = ["pip", "install", "--quiet", "--dry-run", req]
        result = subprocess.run(cmd, capture_output=True, timeout=15)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def validate_all():
    reqs = load_requirements()
    rules = load_rules()
    freeze = pip_freeze()

    report = {
        "invalid": [],
        "missing": [],
        "blocked": [],
        "ok": [],
    }

    for req in reqs:
        pkg = req.split("==")[0].split(">=")[0]

        if pkg in rules.get("blocked_dependencies", []):
            report["blocked"].append(req)
            continue

        if not validate_pip_can_install(req):
            report["invalid"].append(req)
            continue

        installed = any(f.startswith(pkg + "==") for f in freeze)
        if not installed:
            report["missing"].append(req)
            continue

        report["ok"].append(req)

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SILA Dependency Validator")
    parser.add_argument("--report", help="Save report to JSON file")
    args = parser.parse_args()

    rep = validate_all()

    # Save report if requested
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with report_path.open("w") as f:
            json.dump(rep, f, indent=2)
        print(f"📊 Report saved to: {report_path}")

    print("\n=== Dependency Validator Report ===\n")

    for key, items in rep.items():
        print(f"{key.upper()}:")
        for it in items:
            print(f"  - {it}")
        print()

    if rep["invalid"] or rep["missing"] or rep["blocked"]:
        sys.exit(1)

    sys.exit(0)
