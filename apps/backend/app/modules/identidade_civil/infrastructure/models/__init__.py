"""Modelos de infraestrutura do módulo de identidade civil."""

# NOTA: CitizenModel foi unificado com CitizenFUC
# Para consistência, use CitizenFUC de app.citizen.core.models
from app.citizen.core.models import CitizenFUC

# Aliás para compatibilidade (opcional)
CitizenModel = CitizenFUC

__all__ = [
    'CitizenModel',
    'CitizenFUC',
]
