#!/usr/bin/env python3

import re
import subprocess


def pip_can_install(req: str) -> bool:
    proc = subprocess.run(
        ["pip", "install", "--dry-run", "--quiet", req],
        capture_output=True,
    )
    return proc.returncode == 0


def validate_requirement_line(line: str) -> dict:
    line = line.strip()

    if not line or line.startswith("#"):
        return {"line": line, "status": "skip"}

    pattern = r"^([a-zA-Z0-9_\-]+)([<>=!]=.+)?$"
    if not re.match(pattern, line):
        return {"line": line, "status": "invalid-format"}

    if not pip_can_install(line):
        return {"line": line, "status": "not-installable"}

    return {"line": line, "status": "ok"}
