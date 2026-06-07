import re
from pathlib import Path

ROOT = Path("apps/backend/app/modules/justice")
PATTERN = re.compile(r'("""[^"]*""")\s+from ')


def run() -> None:
    updated = 0
    for path in ROOT.rglob("*.py"):
        text = path.read_text()
        new_text = PATTERN.sub(r"\\1\\nfrom ", text)
        if new_text != text:
            path.write_text(new_text)
            updated += 1
    print(f"Fixed files: {updated}")


if __name__ == "__main__":
    run()
