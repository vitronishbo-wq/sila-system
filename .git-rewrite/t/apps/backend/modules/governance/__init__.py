"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

# governance module
# Este modulo foi gerado automaticamente pelo script fix_module_structure.ps1


# Serviço: Auditoria de Log / Audit Logging

# Serviço: Controle de Versão / Version Control

# Serviço: Política de Segurança / Security Policy

# Serviço: Gestão de Risco / Risk Management
