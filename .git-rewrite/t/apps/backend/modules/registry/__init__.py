"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

# registry module
# Este modulo foi gerado automaticamente pelo script fix_module_structure.ps1


# Serviço: Registo Civil / Civil Registry

# Serviço: Registo de Nascimento / Birth Registration

# Serviço: Registo de Casamento / Marriage Registration

# Serviço: Registo de Óbito / Death Registration

# Serviço: Adoção de Menor / Child Adoption

# Serviço: Tutela de Menor / Child Guardianship

# Serviço: Reconhecimento de Paternidade / Paternity Recognition

# Serviço: Retificação de Registro / Record Rectification

# Serviço: Certidão Negativa / Negative Certificate

# Serviço: Registo de Imóvel / Property Registration
