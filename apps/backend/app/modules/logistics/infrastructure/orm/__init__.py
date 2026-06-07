from apps.backend.app.modules.logistics.infrastructure.orm.bilhetagem_evento_model import (
    BilhetagemEventoModel,
)
from apps.backend.app.modules.logistics.infrastructure.orm.frota_model import FrotaModel
from apps.backend.app.modules.logistics.infrastructure.orm.linha_model import LinhaModel
from apps.backend.app.modules.logistics.infrastructure.orm.toll_passage_model import (
    TollPassageModel,
)
from apps.backend.app.modules.logistics.infrastructure.orm.veiculo_model import VeiculoModel
from apps.backend.app.modules.logistics.infrastructure.orm.viagem_model import ViagemModel

__all__ = [
    "ViagemModel",
    "FrotaModel",
    "LinhaModel",
    "VeiculoModel",
    "BilhetagemEventoModel",
    "TollPassageModel",
]
