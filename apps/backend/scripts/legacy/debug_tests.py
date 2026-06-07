import os
import sys

import pytest

# Ensure we are in the right directory
os.chdir("/app")
sys.path.insert(0, "/app")

if __name__ == "__main__":
    # Run pytest and capture everything
    retcode = pytest.main(["tests/integration/test_users.py", "-vv", "--tb=long"])
    print(f"Pytest exited with code {retcode}")
