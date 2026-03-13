from app.modules.logistics.domain.infrastructure.models.bilhetagem_evento_model import (
    BilhetagemEventoModel,
)
from app.modules.logistics.domain.infrastructure.models.frota_model import FrotaModel
from app.modules.logistics.domain.infrastructure.models.linha_model import LinhaModel
from app.modules.logistics.domain.infrastructure.models.toll_passage_model import (
    TollPassageModel,
)
from app.modules.logistics.domain.infrastructure.models.veiculo_model import VeiculoModel
from app.modules.logistics.domain.infrastructure.models.viagem_model import ViagemModel

__all__ = [
    "ViagemModel",
    "FrotaModel",
    "LinhaModel",
    "VeiculoModel",
    "BilhetagemEventoModel",
    "TollPassageModel",
]
