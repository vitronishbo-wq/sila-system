from __future__ import annotations
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.logistics.domain.ports import ViagemRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import StatusViagem
from apps.backend.app.modules.logistics.domain.models import Viagem
from apps.backend.app.modules.logistics.domain.exceptions import InvalidViagemStateError, ViagemConflictError, ViagemNotFoundError

class ViagemDomainService:

    def __init__(self, *, viagem_repo: ViagemRepositoryPort) -> None:
        self._viagem_repo = viagem_repo

    async def programar_viagem(self, *, linha_id: UUID, veiculo_id: UUID, motorista_id: UUID, data_hora_saida: datetime, data_hora_chegada_prevista: datetime, origem: str, destino: str, itinerario: list[dict] | None=None, observacoes: str | None=None) -> Viagem:
        conflito = await self._viagem_repo.has_active_for_veiculo(veiculo_id=veiculo_id, inicio=data_hora_saida, fim=data_hora_chegada_prevista)
        if conflito:
            raise ViagemConflictError('Veiculo ja possui viagem ativa no intervalo informado')
        viagem = Viagem.programar(linha_id=linha_id, veiculo_id=veiculo_id, motorista_id=motorista_id, data_hora_saida=data_hora_saida, data_hora_chegada_prevista=data_hora_chegada_prevista, origem=origem, destino=destino, itinerario=itinerario, observacoes=observacoes)
        return await self._viagem_repo.save(viagem)

    async def iniciar_viagem(self, viagem_id: UUID) -> Viagem:
        viagem = await self._obter_ou_erro(viagem_id)
        try:
            viagem.iniciar()
        except ValueError as exc:
            raise InvalidViagemStateError(str(exc)) from exc
        return await self._viagem_repo.save(viagem)

    async def concluir_viagem(self, viagem_id: UUID, *, data_hora_chegada: datetime) -> Viagem:
        viagem = await self._obter_ou_erro(viagem_id)
        try:
            viagem.concluir(data_hora_chegada)
        except ValueError as exc:
            raise InvalidViagemStateError(str(exc)) from exc
        return await self._viagem_repo.save(viagem)

    async def cancelar_viagem(self, viagem_id: UUID, *, motivo: str) -> Viagem:
        viagem = await self._obter_ou_erro(viagem_id)
        try:
            viagem.cancelar(motivo)
        except ValueError as exc:
            raise InvalidViagemStateError(str(exc)) from exc
        return await self._viagem_repo.save(viagem)

    async def obter_por_id(self, viagem_id: UUID) -> Viagem:
        return await self._obter_ou_erro(viagem_id)

    async def listar(self, *, status: StatusViagem | None=None, linha_id: UUID | None=None, veiculo_id: UUID | None=None) -> list[Viagem]:
        return await self._viagem_repo.list(status=status, linha_id=linha_id, veiculo_id=veiculo_id)

    async def _obter_ou_erro(self, viagem_id: UUID) -> Viagem:
        viagem = await self._viagem_repo.get_by_id(viagem_id)
        if not viagem:
            raise ViagemNotFoundError('Viagem nao encontrada')
        return viagem