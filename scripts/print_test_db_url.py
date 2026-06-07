#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from apps.backend.app.core.settings import settings
except Exception as e:
    print('IMPORT_ERROR', e)
    raise

print('DATABASE_URL=', settings.DATABASE_URL)
print('REDIS_URL=', settings.REDIS_URL)
print('ENV_FILE_USED=.env in apps/backend')
print('Settings module:', settings.__class__)
