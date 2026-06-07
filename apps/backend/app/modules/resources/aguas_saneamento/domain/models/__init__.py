from apps.backend.app.modules.resources.aguas_saneamento.domain.models.abastecimento import (
    AbastecimentoAgua,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.consumo_agua import (
    ConsumoAgua,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.fatura_agua import FaturaAgua
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.infraestrutura import (
    InfraestruturaHidrica,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.outorga import Outorga

__all__ = ["Outorga", "InfraestruturaHidrica", "AbastecimentoAgua", "ConsumoAgua", "FaturaAgua"]
