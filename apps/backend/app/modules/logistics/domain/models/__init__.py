from apps.backend.app.modules.logistics.domain.models.bilhetagem_eletronica import (
    BilhetagemEletronica,
)
from apps.backend.app.modules.logistics.domain.models.bilhete import Bilhete
from apps.backend.app.modules.logistics.domain.models.demanda import DemandaOperacional
from apps.backend.app.modules.logistics.domain.models.fiscalizacao_transporte import (
    FiscalizacaoTransporte,
)
from apps.backend.app.modules.logistics.domain.models.frota import Frota
from apps.backend.app.modules.logistics.domain.models.linha import Linha
from apps.backend.app.modules.logistics.domain.models.manutencao import Manutencao
from apps.backend.app.modules.logistics.domain.models.qualidade_servico import QualidadeServico
from apps.backend.app.modules.logistics.domain.models.rodovia import Rodovia
from apps.backend.app.modules.logistics.domain.models.tarifa import Tarifa
from apps.backend.app.modules.logistics.domain.models.veiculo import Veiculo
from apps.backend.app.modules.logistics.domain.models.viagem import Viagem

__all__ = [
    "Rodovia",
    "Veiculo",
    "Linha",
    "Viagem",
    "Bilhete",
    "Frota",
    "Manutencao",
    "Tarifa",
    "FiscalizacaoTransporte",
    "BilhetagemEletronica",
    "DemandaOperacional",
    "QualidadeServico",
]
