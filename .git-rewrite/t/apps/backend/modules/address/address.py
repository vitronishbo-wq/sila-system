"""Compatibility shim — arquivo movido para backend/archived_duplicates/modules/address.py

Este arquivo foi arquivado. Atualize as importações para usar o pacote
'apps.backend.modules.address'.
"""

import warnings

warnings.warn(
    "Compat shim: 'apps.backend.modules.address' foi arquivado em backend/archived_duplicates/modules/address.py; "
    "por favor atualize suas importações para o package 'apps.backend.modules.address'.",
    DeprecationWarning,
)
try:
    pass
except Exception:
    pass
