from apps.backend.app.modules.resources.pescas.industrial.application.services.inspecao_industrial_service import (
    InspecaoIndustrialService,
)
from apps.backend.app.modules.resources.pescas.industrial.application.services.lote_producao_service import (
    LoteProducaoService,
)
from apps.backend.app.modules.resources.pescas.industrial.application.services.produto_processado_service import (
    ProdutoProcessadoService,
)
from apps.backend.app.modules.resources.pescas.industrial.application.services.unidade_processamento_service import (
    UnidadeProcessamentoService,
)

__all__ = [
    "UnidadeProcessamentoService",
    "ProdutoProcessadoService",
    "LoteProducaoService",
    "InspecaoIndustrialService",
]
