"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

__all__ = ["models", "schemas", "crud", "services", "endpoints"]

# Serviço: Abertura Processo


# Serviço: Alvará Comercial / Commercial License

# Serviço: Registo de Empresa / Business Registration

# Serviço: Licença Industrial / Industrial License

# Serviço: Certificação de Origem / Origin Certification

# Serviço: Inspeção Sanitária / Sanitary Inspection

# Serviço: Registo de Marca / Trademark Registration

# Serviço: Licença de Importação / Import License

# Serviço: Fiscalização de Mercado / Market Inspection

# Serviço: Taxa Comercial / Commercial Tax

# Serviço: Contrato Público / Public Contract
