import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from scripts.seed_all_users import seed_all_users  # noqa: E402


def main() -> None:
    """
    Legacy wrapper.
    Standardized on iam_users via scripts/seed_all_users.py.
    """
    seed_all_users()


if __name__ == "__main__":
    main()
