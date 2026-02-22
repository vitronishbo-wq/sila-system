"""Compatibility shim — arquivo movido para backend/archived_duplicates/modules/auth.py

Este arquivo foi arquivado. Atualize as importações para usar o pacote
'apps.backend.modules.auth'.
"""

import warnings

warnings.warn(
    "Compat shim: 'apps.backend.modules.auth' foi arquivado em backend/archived_duplicates/modules/auth.py; "
    "por favor atualize suas importações para o package 'apps.backend.modules.auth'.",
    DeprecationWarning,
)
try:
    pass
except Exception:
    pass
