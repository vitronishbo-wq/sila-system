#!/usr/bin/env python3
"""Lightweight verifier for AGENT_RULES.md used by CI and local checks.

Exits 0 when frontmatter contains `enforce: true`, otherwise exits 2 and
prints the mandatory failure payload required by project governance.
"""
import sys
from pathlib import Path
import hashlib


def main() -> int:
    p = Path("AGENT_RULES.md")
    if not p.exists():
        print("STATUS: BLOQUEADO")
        print("MOTIVO: AGENT_RULES_UNAVAILABLE")
        return 2
    txt = p.read_text(encoding="utf-8")
    meta = {}
    rest = txt
    if txt.lstrip().startswith("---"):
        parts = txt.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            rest = parts[2]
            for line in fm.strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    if meta.get("enforce", "").lower() not in ("true", "1", "yes"):
        print("STATUS: BLOQUEADO")
        print("MOTIVO: AGENT_RULES_UNAVAILABLE")
        print("REASON: missing/invalid frontmatter 'enforce: true'")
        return 2
    h = hashlib.sha256(rest.encode("utf-8")).hexdigest()
    print("STATUS: OK")
    print("AGENT_RULES_ENFORCED:", meta.get("enforce"))
    print("SHA256:", h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
