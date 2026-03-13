from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.outorga_repository_port import OutorgaRepositoryPort
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoCaptacao, TipoOutorga, TipoUso
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.outorga import Outorga
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import OutorgaAlreadyExistsError, OutorgaNotFoundError

class OutorgaService:

    def __init__(self, *, outorga_repo: OutorgaRepositoryPort) -> None:
        self._outorga_repo = outorga_repo

    async def requerer(self, *, tipo: TipoOutorga, requerente_id: UUID, requerente_tipo: str, corpo_hidrico_id: UUID, vazao: Decimal, unidade_vazao: str, finalidade_uso: TipoUso, tipo_captacao: TipoCaptacao | None=None, tempo_captacao: int | None=None, periodo_captacao: str | None=None, coordenadas_lat: Decimal | None=None, coordenadas_long: Decimal | None=None) -> Outorga:
        existentes = await self._outorga_repo.list(requerente_id=requerente_id, tipo=tipo)
        ativos = {StatusOutorga.REQUERIDA, StatusOutorga.EM_ANALISE, StatusOutorga.DEFERIDA, StatusOutorga.SUSPENSA}
        if any((item.corpo_hidrico_id == corpo_hidrico_id and item.status in ativos for item in existentes)):
            raise OutorgaAlreadyExistsError('Ja existe outorga ativa para o mesmo requerente e corpo hidrico')
        item = Outorga.requerer(tipo=tipo, requerente_id=requerente_id, requerente_tipo=requerente_tipo, corpo_hidrico_id=corpo_hidrico_id, tipo_captacao=tipo_captacao, vazao=vazao, unidade_vazao=unidade_vazao, tempo_captacao=tempo_captacao, periodo_captacao=periodo_captacao, finalidade_uso=finalidade_uso, coordenadas_lat=coordenadas_lat, coordenadas_long=coordenadas_long)
        item.numero_outorga = await self._outorga_repo.next_numero()
        return await self._outorga_repo.save(item)

    async def iniciar_analise(self, numero_outorga: str) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.iniciar_analise()
        return await self._outorga_repo.save(item)

    async def deferir(self, numero_outorga: str, *, data_validade_inicio: date, data_validade_fim: date, data_publicacao: date, processo: str) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.deferir(data_validade_inicio=data_validade_inicio, data_validade_fim=data_validade_fim, data_publicacao=data_publicacao, processo=processo)
        return await self._outorga_repo.save(item)

    async def indeferir(self, numero_outorga: str, *, motivo: str) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.indeferir(motivo)
        return await self._outorga_repo.save(item)

    async def cancelar(self, numero_outorga: str, *, motivo: str) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.cancelar(motivo)
        return await self._outorga_repo.save(item)

    async def suspender(self, numero_outorga: str, *, motivo: str) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.suspender(motivo)
        return await self._outorga_repo.save(item)

    async def renovar(self, numero_outorga: str, *, nova_data_fim: date) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.renovar(nova_data_fim)
        return await self._outorga_repo.save(item)

    async def obter_por_numero(self, numero_outorga: str) -> Outorga:
        item = await self._obter_ou_erro(numero_outorga)
        item.atualizar_status_vencimento()
        return item

    async def listar(self, *, requerente_id: UUID | None=None, tipo: TipoOutorga | None=None, status: StatusOutorga | None=None) -> list[Outorga]:
        items = await self._outorga_repo.list(requerente_id=requerente_id, tipo=tipo, status=status)
        for item in items:
            item.atualizar_status_vencimento()
        return items

    async def _obter_ou_erro(self, numero_outorga: str) -> Outorga:
        item = await self._outorga_repo.get_by_numero(numero_outorga)
        if not item:
            raise OutorgaNotFoundError('Outorga nao encontrada')
        return item