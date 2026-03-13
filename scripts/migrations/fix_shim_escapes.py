from pathlib import Path

ROOT = Path("apps/backend/app/modules/justice")


def run() -> None:
    updated = 0
    for path in ROOT.rglob("*.py"):
        text = path.read_text()
        if "\\1\\n" in text:
            path.write_text(text.replace("\\1\\n", ""))
            updated += 1
    print(f"Fixed files: {updated}")


if __name__ == "__main__":
    run()
