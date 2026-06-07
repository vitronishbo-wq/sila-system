#!/usr/bin/env python3
"""
Find modules missing application layer components
"""

from pathlib import Path

modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
modules = sorted(
    [
        d
        for d in modules_path.iterdir()
        if d.is_dir() and not d.name.startswith("_") and d.name != "tests"
    ]
)

print(f"Total modules: {len(modules)}\n")

missing = []
for module in modules:
    app_dir = module / "application"
    if not app_dir.exists():
        missing.append(module.name)
        print(f"✗ {module.name}: NO application directory")
    else:
        has_commands = (app_dir / "commands.py").exists()
        has_handlers = (app_dir / "event_handlers.py").exists()

        if not has_commands:
            print(f"  {module.name}: missing commands.py")
        if not has_handlers:
            print(f"  {module.name}: missing event_handlers.py")

        if has_commands and has_handlers:
            print(f"✓ {module.name}: OK")

print(f"\nModules with complete application layer: {len(modules) - len(missing)}/{len(modules)}")
if missing:
    print(f"Missing application directory: {', '.join(missing)}")
