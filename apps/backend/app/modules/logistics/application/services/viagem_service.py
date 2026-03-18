from __future__ import annotations
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.logistics.domain.ports import ViagemRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import StatusViagem
from apps.backend.app.modules.logistics.domain.models import Viagem
from apps.backend.app.modules.logistics.domain.services import ViagemDomainService

class ViagemService:

    def __init__(self, *, viagem_repo: ViagemRepositoryPort) -> None:
        self._domain = ViagemDomainService(viagem_repo=viagem_repo)

    async def programar_viagem(self, *, linha_id: UUID, veiculo_id: UUID, motorista_id: UUID, data_hora_saida: datetime, data_hora_chegada_prevista: datetime, origem: str, destino: str, itinerario: list[dict] | None=None, observacoes: str | None=None) -> Viagem:
        return await self._domain.programar_viagem(linha_id=linha_id, veiculo_id=veiculo_id, motorista_id=motorista_id, data_hora_saida=data_hora_saida, data_hora_chegada_prevista=data_hora_chegada_prevista, origem=origem, destino=destino, itinerario=itinerario, observacoes=observacoes)

    async def iniciar_viagem(self, viagem_id: UUID) -> Viagem:
        return await self._domain.iniciar_viagem(viagem_id)

    async def concluir_viagem(self, viagem_id: UUID, *, data_hora_chegada: datetime) -> Viagem:
        return await self._domain.concluir_viagem(viagem_id, data_hora_chegada=data_hora_chegada)

    async def cancelar_viagem(self, viagem_id: UUID, *, motivo: str) -> Viagem:
        return await self._domain.cancelar_viagem(viagem_id, motivo=motivo)

    async def obter_por_id(self, viagem_id: UUID) -> Viagem:
        return await self._domain.obter_por_id(viagem_id)

    async def listar(self, *, status: StatusViagem | None=None, linha_id: UUID | None=None, veiculo_id: UUID | None=None) -> list[Viagem]:
        return await self._domain.listar(status=status, linha_id=linha_id, veiculo_id=veiculo_id)