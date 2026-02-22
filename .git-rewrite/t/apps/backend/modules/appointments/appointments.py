"""Compatibility shim — arquivo movido para backend/archived_duplicates/modules/appointments.py

Este arquivo foi arquivado. Atualize as importações para usar o pacote
'backend.modules.appointments'.
"""

import warnings

warnings.warn(
    "Compat shim: 'backend.modules.appointments' foi arquivado em backend/archived_duplicates/modules/appointments.py; "
    "por favor atualize suas importações para o package 'backend.modules.appointments'.",
    DeprecationWarning,
)
try:
    pass
except Exception:
    pass
