# apps/backend/scripts/debug_mappers.py
import sys
from sqlalchemy.orm import configure_mappers
try:
    configure_mappers()
    print("✅ Mappers configured successfully")
except Exception as e:
    print(f"❌ Mapper configuration failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

