"""Domain enumerations module"""

import importlib.util
import os as _os
import sys as _sys

from .status_enum import AuditStatus, EntityStatus, LifecycleStatus, ProcessStatus
from .type_enum import (
    DocumentType,
    EntityType,
    NotificationPriority,
    OperationType,
    SortOrder,
    ValidationLevel,
)

# Re-export from sibling enums.py (coexists as module next to this package).
# Standard import paths cannot reach it because `domain.enums` resolves to this
# `enums/` package, shadowing the `enums.py` module file.
_enums_path = _os.path.join(_os.path.dirname(__file__), "..", "enums.py")
_enums_name = "apps.backend.app.modules.public_security.domain.enums_mod"
_enums_spec = importlib.util.spec_from_file_location(_enums_name, _enums_path)
_enums_mod = importlib.util.module_from_spec(_enums_spec)
_sys.modules[_enums_name] = _enums_mod
_enums_spec.loader.exec_module(_enums_mod)

CargoPolicial = _enums_mod.CargoPolicial
Patente = _enums_mod.Patente
PrioridadeOcorrencia = _enums_mod.PrioridadeOcorrencia
StatusAgente = _enums_mod.StatusAgente
StatusCadeiaCustodia = _enums_mod.StatusCadeiaCustodia
StatusInvestigacao = _enums_mod.StatusInvestigacao
StatusLaudo = _enums_mod.StatusLaudo
StatusMandado = _enums_mod.StatusMandado
StatusOcorrencia = _enums_mod.StatusOcorrencia
StatusProva = _enums_mod.StatusProva
StatusUnidadePolicial = _enums_mod.StatusUnidadePolicial
StatusVestigio = _enums_mod.StatusVestigio
TipoAgente = _enums_mod.TipoAgente
TipoEvidencia = _enums_mod.TipoEvidencia
TipoLaudo = _enums_mod.TipoLaudo
TipoMandado = _enums_mod.TipoMandado
TipoOcorrencia = _enums_mod.TipoOcorrencia
TipoProva = _enums_mod.TipoProva
TipoUnidadePolicial = _enums_mod.TipoUnidadePolicial
TipoVestigio = _enums_mod.TipoVestigio
StatusEvidencia = _enums_mod.StatusEvidencia
TipoVinculo = _enums_mod.TipoVinculo

__all__ = [
    "EntityStatus",
    "ProcessStatus",
    "LifecycleStatus",
    "AuditStatus",
    "EntityType",
    "DocumentType",
    "OperationType",
    "SortOrder",
    "NotificationPriority",
    "ValidationLevel",
    "CargoPolicial",
    "Patente",
    "PrioridadeOcorrencia",
    "StatusAgente",
    "StatusCadeiaCustodia",
    "StatusEvidencia",
    "StatusInvestigacao",
    "StatusLaudo",
    "StatusMandado",
    "StatusOcorrencia",
    "StatusProva",
    "StatusUnidadePolicial",
    "StatusVestigio",
    "TipoAgente",
    "TipoEvidencia",
    "TipoLaudo",
    "TipoMandado",
    "TipoOcorrencia",
    "TipoProva",
    "TipoUnidadePolicial",
    "TipoVestigio",
    "TipoVinculo",
]
