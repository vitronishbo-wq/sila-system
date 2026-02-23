"""Compat layer: fornece `CitizenModel` para compatibilidade com o
restante código do módulo Identidade Civil.

Historicamente havia um modelo local `CitizenModel`. Este projeto unificou
o modelo no FUC central (`app.citizen.core.models.CitizenFUC`). Para evitar
requerer alterações em todo o código, exportamos um alias `CitizenModel`.
"""

from app.citizen.core.models import CitizenFUC

# Alias para compatibilidade com o código existente
CitizenModel = CitizenFUC

__all__ = ["CitizenModel", "CitizenFUC"]
