from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from scripts.seed_all_users import seed_all_users


def main() -> None:
    """
    Legacy wrapper.
    Standardized on iam_users via scripts/seed_all_users.py.
    Use seed_founding_users_with_territories.py for territory assignment.
    """
    seed_all_users()


if __name__ == "__main__":
    main()
