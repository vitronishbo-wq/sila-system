"""Social module."""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

__all__ = ["models", "schemas", "crud", "services", "endpoints"]


# Serviço: Auxílio Social / Social Assistance

# Serviço: Bolsa Família Municipal / Municipal Family Grant

# Serviço: Programa do Idoso / Elderly Program

# Serviço: Proteção ao Menor / Child Protection

# Serviço: Assistência à Mulher / Women's Assistance

# Serviço: Reabilitação Social / Social Rehabilitation

# Serviço: Inclusão Digital / Digital Inclusion

# Serviço: Capacitação Profissional / Professional Training

# Serviço: Habitação Social / Social Housing

# Serviço: Segurança Alimentar / Food Security
