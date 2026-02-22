"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from .routes import router

__all__ = ["router", "models", "schemas", "crud", "services"]


# Serviço: Coleta de Lixo / Waste Collection

# Serviço: Limpeza Urbana / Urban Cleaning

# Serviço: Tratamento de Água / Water Treatment

# Serviço: Esgoto Sanitário / Sanitary Sewage

# Serviço: Controle de Vetores / Vector Control

# Serviço: Desinsetização / Pest Control

# Serviço: Educação Ambiental / Environmental Education

# Serviço: Reciclagem de Lixo / Waste Recycling

# Serviço: Agente Sanitário / Sanitary Agent

# Serviço: Monitoramento Ambiental / Environmental Monitoring
