"""Sanity tests - VERIFICAÇÃO SIMPLES"""
import sys

def test_imports():
    """Testa imports críticos"""
    try:
        # Core
        from app.core.db import get_db, AsyncSessionLocal, importAsyncSessionLocal
        assert importAsyncSessionLocal is not None
        print("✅ app.core.db imports OK")
        
        # Territory FK fix
        from app.core.territory.models.territory import Territory
        print("✅ Territory FK fixed")
        
        # Identity
        from modules.identity.models.user import User
        print("✅ Identity User model OK")
        
        print("\n✅ ALL CRITICAL IMPORTS OK")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

