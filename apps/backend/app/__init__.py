"""
Módulo app - Tradução de imports
Permite que os módulos usem 'from config import settings'
"""

import sys
from types import ModuleType

# Importações do novo sistema de configuração
from config import settings

# Tradução de módulos
core_module = ModuleType("core")
core_module.config = sys.modules["config"]
core_module.db = sys.modules.get("core.db")
core_module.schemas = sys.modules.get("core.schemas")
core_module.services = sys.modules.get("core.services")
core_module.repositories = sys.modules.get("core.repositories")

# Adicionar ao sys.modules
sys.modules["app.core"] = core_module
sys.modules["app"] = sys.modules[__name__]

# Importações específicas (se existirem)
try:
    from core.db.session import get_db_session

    # Database session
    db = type("db", (), {"session": get_db_session})()
except ImportError:
    db = None

# Schemas
try:
    from core.schemas import (
        Token,
        RefreshTokenRequest,
        RefreshTokenResponse,
        UserCreate,
        UserInDB,
    )
except ImportError:
    pass

# Services
try:
    from core.services import AuthService
except ImportError:
    pass

# Repositories
try:
    from core.repositories import user_repo
except ImportError:
    pass
