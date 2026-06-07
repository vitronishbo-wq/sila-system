#!/usr/bin/env python3
import os
import sys

import pytest

os.environ.setdefault('REDIS_URL', 'redis://127.0.0.1:6379/0')

if __name__ == '__main__':
    rc = pytest.main(["-q", "tests/educacao/test_race_condition.py"]) 
    print('\nPYTEST_RETURN_CODE:', rc)
    sys.exit(rc)
