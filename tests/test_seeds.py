import subprocess
import sys
from pathlib import Path


def test_no_hardcoded_users_in_seeds():
    repo_root = Path(__file__).resolve().parents[1]
    checker = repo_root / "scripts" / "ci" / "check_no_hardcoded_users.py"
    assert checker.exists(), "CI checker script missing"
    res = subprocess.run([sys.executable, str(checker)], capture_output=True, text=True)
    # Expect exit code 0
    assert res.returncode == 0, f"Found hardcoded users in seeds:\n{res.stdout}\n{res.stderr}"
