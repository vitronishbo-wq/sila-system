from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.parcelamento_repository_port import ParcelamentoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusParcelamento, TipoParcelamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.parcelamento import Parcelamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import ParcelamentoAlreadyExistsError, ParcelamentoNotFoundError

class ParcelamentoService:

    def __init__(self, *, parcelamento_repo: ParcelamentoRepositoryPort) -> None:
        self._parcelamento_repo = parcelamento_repo

    async def criar(self, *, nome: str, tipo: TipoParcelamento, plano_diretor_id: UUID, zoneamento_id: UUID, provincia: str, area_total: Decimal, quantidade_unidades_prevista: int, municipio: str | None=None, area_publica_prevista: Decimal | None=None, area_sistema_viario_prevista: Decimal | None=None, codigo_parcelamento: str | None=None) -> Parcelamento:
        codigo = codigo_parcelamento or await self._parcelamento_repo.next_codigo()
        existente = await self._parcelamento_repo.get_by_codigo(codigo)
        if existente:
            raise ParcelamentoAlreadyExistsError('Ja existe parcelamento com este codigo')
        item = Parcelamento.criar(codigo_parcelamento=codigo, nome=nome, tipo=tipo, plano_diretor_id=plano_diretor_id, zoneamento_id=zoneamento_id, provincia=provincia, area_total=area_total, quantidade_unidades_prevista=quantidade_unidades_prevista, municipio=municipio, area_publica_prevista=area_publica_prevista, area_sistema_viario_prevista=area_sistema_viario_prevista)
        return await self._parcelamento_repo.save(item)

    async def iniciar_analise(self, codigo_parcelamento: str) -> Parcelamento:
        item = await self._obter_ou_erro(codigo_parcelamento)
        item.iniciar_analise()
        return await self._parcelamento_repo.save(item)

    async def aprovar(self, codigo_parcelamento: str) -> Parcelamento:
        item = await self._obter_ou_erro(codigo_parcelamento)
        item.aprovar()
        return await self._parcelamento_repo.save(item)

    async def iniciar_execucao(self, codigo_parcelamento: str) -> Parcelamento:
        item = await self._obter_ou_erro(codigo_parcelamento)
        item.iniciar_execucao()
        return await self._parcelamento_repo.save(item)

    async def concluir(self, codigo_parcelamento: str, *, quantidade_unidades_resultante: int) -> Parcelamento:
        item = await self._obter_ou_erro(codigo_parcelamento)
        item.concluir(quantidade_unidades_resultante=quantidade_unidades_resultante)
        return await self._parcelamento_repo.save(item)

    async def cancelar(self, codigo_parcelamento: str, *, motivo: str) -> Parcelamento:
        item = await self._obter_ou_erro(codigo_parcelamento)
        item.cancelar(motivo=motivo)
        return await self._parcelamento_repo.save(item)

    async def obter_por_codigo(self, codigo_parcelamento: str) -> Parcelamento:
        return await self._obter_ou_erro(codigo_parcelamento)

    async def listar(self, *, status: StatusParcelamento | None=None, tipo: TipoParcelamento | None=None, provincia: str | None=None) -> list[Parcelamento]:
        return await self._parcelamento_repo.list(status=status, tipo=tipo, provincia=provincia)

    async def _obter_ou_erro(self, codigo_parcelamento: str) -> Parcelamento:
        item = await self._parcelamento_repo.get_by_codigo(codigo_parcelamento)
        if not item:
            raise ParcelamentoNotFoundError('Parcelamento nao encontrado')
        return item