"""Catálogo Nacional de Processos Transversais do Estado.

Cada processo atravessa múltiplos módulos/ministérios.
Regista: módulos envolvidos, eventos trocados, dono do processo.
"""

from sila_platform.interoperability.process_catalog.catalog import (
    ProcessDefinition,
    ProcessCatalog,
    get_catalog,
    list_processes,
    get_process,
)
