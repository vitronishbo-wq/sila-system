#!/usr/bin/env python3

from pathlib import Path

bridge_path = Path("apps/backend/app/core/bridges/identity_bridge.py")
content = bridge_path.read_text()

old_import = "app.modules.justice.bounded_contexts.civil_registry_core.application.services.models"
new_import = "app.modules.justice.bounded_contexts.civil_registry_core.domain.entities.citizen"

if old_import in content:
    print("Substituting obsolete import in identity_bridge.py...")
    content = content.replace(old_import, new_import)
    bridge_path.write_text(content)

print("Healing complete.")
