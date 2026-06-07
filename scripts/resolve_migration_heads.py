#!/usr/bin/env python3
"""
ALEMBIC MIGRATION CONSOLIDATION
Resolves multiple heads by creating merge migration script
"""

import re
from datetime import datetime
from pathlib import Path


def print_box(title="", width=80, char="="):
    """Print a box with title."""
    if title:
        padding_left = (width - len(title) - 2) // 2
        padding_right = width - len(title) - 2 - padding_left
        print(f"{char * padding_left} {title} {char * padding_right}")
    else:
        print(char * width)


def find_alembic_ini():
    """Find alembic.ini file."""
    workspace = Path(__file__).parent.parent
    candidates = [workspace / "alembic.ini", workspace / "apps" / "backend" / "alembic.ini"]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def find_migration_heads():
    """Find all migration head revisions."""
    workspace = Path(__file__).parent.parent
    migration_paths = [
        workspace / "migrations" / "versions",
        workspace / "apps" / "backend" / "app" / "db" / "migrations" / "versions",
    ]

    migrations = {}
    for path in migration_paths:
        if path.exists():
            for mf in path.glob("*.py"):
                if mf.name != "__init__.py":
                    try:
                        content = mf.read_text(encoding="utf-8", errors="ignore")
                    except:
                        continue

                    # Extract revision
                    rev_match = re.search(r"revision\s*=\s*['\"]([^'\"]*)['\"]", content)
                    revision = rev_match.group(1) if rev_match else None

                    # Extract down_revision
                    down_match = re.search(r"down_revision\s*=\s*['\"]([^'\"]*)['\"]", content)
                    down_revision = down_match.group(1) if down_match else None

                    if revision:
                        migrations[revision] = {
                            "file": mf.name,
                            "down_revision": down_revision,
                            "path": mf,
                        }

    # Find heads (revisions not referenced as down_revision)
    all_revisions = set(migrations.keys())
    all_down_revisions = {m["down_revision"] for m in migrations.values() if m["down_revision"]}

    heads = all_revisions - all_down_revisions

    return heads, migrations


def generate_merge_migration(heads, migrations):
    """Generate merge migration file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    merge_revision = f"{timestamp}_merge_migrations_consolidation"

    heads_list = sorted(list(heads))
    down_revision_str = ", ".join(f'"{h}"' for h in heads_list)

    merge_content = f'''"""Consolidate migration heads - merge {len(heads)} branches into single chain

Revision ID: {merge_revision}
Revises: {down_revision_str}
Create Date: {datetime.now().isoformat()}

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '{merge_revision}'
down_revision = ({down_revision_str},)
branch_labels = None
depends_on = None


def upgrade():
    """
    This is a merge migration that combines {len(heads)} separate migration branches.
    No schema changes are made - this only consolidates the migration history.
    
    Merged heads:
{chr(10).join(f"    - {h} ({migrations[h]["file"]})" for h in heads_list)}
    """
    pass


def downgrade():
    """Downgrade is not supported for merge migrations."""
    raise NotImplementedError('Downgrade is not supported for this merge migration')
'''

    return merge_content, merge_revision


def main():
    print_box("ALEMBIC MIGRATION CONSOLIDATION", width=80)

    # Find heads
    print("\nSTEP 1: Detecting Migration Heads")
    print("-" * 80)

    heads, migrations = find_migration_heads()

    if not heads:
        print("✓ No migration heads detected")
        print("  Your migrations are already consolidated")
        return

    print(f"Found {len(heads)} migration heads:")
    for i, head in enumerate(sorted(heads), 1):
        mig = migrations[head]
        print(f"  {i}. {head}")
        print(f"     File: {mig['file']}")

    # Generate merge migration
    print("\nSTEP 2: Generating Merge Migration")
    print("-" * 80)

    merge_content, merge_revision = generate_merge_migration(heads, migrations)

    # Find where to save it
    alembic_ini = find_alembic_ini()
    if alembic_ini:
        versions_dir = alembic_ini.parent / "migrations" / "versions"
    else:
        versions_dir = (
            Path(__file__).parent.parent
            / "apps"
            / "backend"
            / "app"
            / "db"
            / "migrations"
            / "versions"
        )

    versions_dir.mkdir(parents=True, exist_ok=True)

    merge_file = versions_dir / f"{merge_revision}.py"
    merge_file.write_text(merge_content)

    print("✓ Merge migration created:")
    print(f"  File: {merge_file}")
    print(f"  Revision: {merge_revision}")

    # Display next steps
    print("\nSTEP 3: Next Actions Required")
    print("-" * 80)

    print("\n⚠️  MIGRATION CONSOLIDATION PREPARED")
    print(f"\nAutomatically generated merge migration that consolidates {len(heads)} branches:")
    for head in sorted(heads):
        print(f"  ← {head}")
    print(f"  → {merge_revision}")

    print("\n📝 TO COMPLETE CONSOLIDATION:")
    print("  1. cd /home/dev03wsl/sila-system")
    print("  2. alembic upgrade head")
    print("")
    print("  This will apply the merge and consolidate your migration history")
    print("  into a single linear chain.")

    print("\n⚠️  IMPORTANT:")
    print("  - Backup your database BEFORE running upgrade")
    print("  - The merge migration makes NO schema changes")
    print("  - It only consolidates migration history")
    print("  - After upgrade, all future migrations will be linear")

    print_box()


if __name__ == "__main__":
    main()
