#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
# also make the backend app package importable as tests do
sys.path.insert(0, str(ROOT / 'apps' / 'backend'))

try:
    from apps.backend.app.core.db import AsyncSessionLocal, Base, db
    print('Imported AsyncSessionLocal:', AsyncSessionLocal)
    print('Is callable:', callable(AsyncSessionLocal))
    print('Base present:', Base is not None)
    print('db present:', db is not None)
except Exception as e:
    print('IMPORT_ERROR', repr(e))
    raise
