"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

# Serviço: Gestão de Usuários / User Management

# Serviço: Controle de Acesso / Access Control

# Serviço: Autenticação Multifator / Multi-factor Authentication

# Serviço: Sessão Segura / Secure Session
