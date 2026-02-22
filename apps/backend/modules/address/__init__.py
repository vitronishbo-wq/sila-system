"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

# address package

# Serviço: Geocodificação de Endereço / Address Geocoding

# Serviço: Validação de CEP / ZIP Code ValidationErrorn

# Serviço: Normalização de Endereço / Address Normalization
