import argparse
import os
import re
from pathlib import Path

DEFAULT_ROOT = Path("apps/backend/app")

REPLACEMENTS = {
    r"from app\.core\.iam\.infrastructure\.repositories": "from apps.backend.app.modules.identity.infrastructure.repositories",
    r"from app\.core\.iam\.infrastructure\.models": "from apps.backend.app.modules.identity.infrastructure.models",
    r"from app\.core\.iam\.domain\.entities": "from apps.backend.app.modules.identity.bounded_contexts.iam.domain.entities",
    r"from app\.core\.iam\.application\.services": "from apps.backend.app.modules.identity.bounded_contexts.iam.application.services",
    r"from app\.core\.iam\.domain\.value_objects": "from apps.backend.app.modules.identity.bounded_contexts.credential_management.domain.value_objects",
    r"import app\.core\.iam": "import apps.backend.app.modules.identity",
    r"from app\.core\.iam": "from apps.backend.app.modules.identity",
}


def fix_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8", errors="surrogateescape")
    original = content
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)
    if content != original:
        path.write_text(content, encoding="utf-8", errors="surrogateescape")
        return True
    return False


def run(root: Path) -> None:
    for file in root.rglob("*.py"):
        path_str = str(file)
        if "venv" in path_str or "__pycache__" in path_str:
            continue
        if fix_file(file):
            print(f"UPDATED: {file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix identity import paths.")
    parser.add_argument(
        "--root",
        default=os.getenv("FIX_IDENTITY_ROOT", str(DEFAULT_ROOT)),
        help="Root directory to scan for python files.",
    )
    args = parser.parse_args()
    run(Path(args.root))
