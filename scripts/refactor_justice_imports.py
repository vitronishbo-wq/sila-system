#!/usr/bin/env python3
import pathlib

ROOT = pathlib.Path("/home/dev03wsl/sila-system/apps/backend/app/modules")

REPLACEMENTS = {
    "from apps.backend.app.modules.justice.civil_registry.application.ports.": "from apps.backend.app.modules.justice.bounded_contexts.application.ports.",
    "from apps.backend.app.modules.justice.civil_registry.domain.": "from apps.backend.app.modules.justice.bounded_contexts.domain.",
    "from apps.backend.app.modules.justice.civil_registry.infrastructure.": "from apps.backend.app.modules.justice.bounded_contexts.infrastructure.",
    "from apps.backend.app.modules.justice.civil_registry.permissions.": "from apps.backend.app.modules.justice.bounded_contexts.permissions.",
}

modified = 0
for f in ROOT.rglob("*.py"):
    text = f.read_text()
    orig = text
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    if text != orig:
        f.write_text(text)
        modified += 1
        print(f"✔ {f.relative_to(ROOT)}")

print(f"Total modified: {modified}")
