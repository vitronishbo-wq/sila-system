# test_simple_import.py
"""Teste simplificado de importação"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("1. Importando Base...")
try:
    from config.database import Base
    print("   ✓ Base OK")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n2. Importando role_permissions...")
try:
    from modules.identity.models.role_permission import role_permissions
    print("   ✓ role_permissions OK")
    print(f"   - Tabela: {role_permissions.name}")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Importando Role...")
try:
    from modules.identity.models.role import Role
    print("   ✓ Role OK")
    print(f"   - Tabela: {Role.__tablename__}")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Importando Permission...")
try:
    from modules.identity.models.permission import Permission
    print("   ✓ Permission OK")
    print(f"   - Tabela: {Permission.__tablename__}")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ TODOS OS IMPORTS FUNCIONARAM!")

