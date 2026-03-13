from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.ambiente.application.ports.auto_infracao_repository_port import AutoInfracaoRepositoryPort
from apps.backend.app.modules.resources.ambiente.application.ports.embargo_repository_port import EmbargoRepositoryPort
from apps.backend.app.modules.resources.ambiente.application.ports.fiscalizacao_repository_port import FiscalizacaoRepositoryPort
from apps.backend.app.modules.resources.ambiente.application.ports.multa_repository_port import MultaRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusAutoInfracao, StatusEmbargo, StatusFiscalizacao, StatusMulta, TipoAutoInfracao
from apps.backend.app.modules.resources.ambiente.domain.models.auto_infracao import AutoInfracao
from apps.backend.app.modules.resources.ambiente.domain.models.embargo import Embargo
from apps.backend.app.modules.resources.ambiente.domain.models.multa import Multa
from apps.backend.app.modules.resources.ambiente.exceptions import AutoInfracaoNotFoundError, EmbargoNotFoundError, FiscalizacaoNotFoundError, MultaNotFoundError

class PenalidadeService:

    def __init__(self, *, fiscalizacao_repo: FiscalizacaoRepositoryPort, auto_infracao_repo: AutoInfracaoRepositoryPort, embargo_repo: EmbargoRepositoryPort, multa_repo: MultaRepositoryPort) -> None:
        self._fiscalizacao_repo = fiscalizacao_repo
        self._auto_infracao_repo = auto_infracao_repo
        self._embargo_repo = embargo_repo
        self._multa_repo = multa_repo

    async def lavrar_auto(self, *, numero_fiscalizacao: str, tipo: TipoAutoInfracao, descricao: str, fiscal_id: UUID, valor_multa: Decimal | None=None) -> AutoInfracao:
        fiscalizacao = await self._fiscalizacao_repo.get_by_numero(numero_fiscalizacao)
        if not fiscalizacao:
            raise FiscalizacaoNotFoundError('Fiscalizacao nao encontrada')
        if fiscalizacao.status not in {StatusFiscalizacao.EM_ANDAMENTO, StatusFiscalizacao.CONCLUIDA}:
            raise ValueError('Fiscalizacao deve estar em andamento ou concluida para lavrar auto')
        item = AutoInfracao.lavrar(numero_fiscalizacao=numero_fiscalizacao, tipo=tipo, descricao=descricao, fiscal_id=fiscal_id, valor_multa=valor_multa)
        item.numero_auto = await self._auto_infracao_repo.next_numero()
        return await self._auto_infracao_repo.save(item)

    async def notificar_auto(self, numero_auto: str) -> AutoInfracao:
        item = await self._auto_infracao_repo.get_by_numero(numero_auto)
        if not item:
            raise AutoInfracaoNotFoundError('Auto de infracao nao encontrado')
        item.notificar()
        return await self._auto_infracao_repo.save(item)

    async def registrar_recurso_auto(self, numero_auto: str) -> AutoInfracao:
        item = await self._auto_infracao_repo.get_by_numero(numero_auto)
        if not item:
            raise AutoInfracaoNotFoundError('Auto de infracao nao encontrado')
        item.registrar_recurso()
        return await self._auto_infracao_repo.save(item)

    async def julgar_auto(self, numero_auto: str, *, mantido: bool, observacoes: str | None=None) -> AutoInfracao:
        item = await self._auto_infracao_repo.get_by_numero(numero_auto)
        if not item:
            raise AutoInfracaoNotFoundError('Auto de infracao nao encontrado')
        item.julgar(mantido=mantido, observacoes=observacoes)
        return await self._auto_infracao_repo.save(item)

    async def aplicar_embargo(self, *, numero_auto_infracao: str, motivo: str) -> Embargo:
        auto = await self._auto_infracao_repo.get_by_numero(numero_auto_infracao)
        if not auto:
            raise AutoInfracaoNotFoundError('Auto de infracao nao encontrado')
        item = Embargo.aplicar(numero_auto_infracao=numero_auto_infracao, motivo=motivo)
        item.numero_embargo = await self._embargo_repo.next_numero()
        return await self._embargo_repo.save(item)

    async def suspender_embargo(self, numero_embargo: str, *, motivo: str) -> Embargo:
        item = await self._embargo_repo.get_by_numero(numero_embargo)
        if not item:
            raise EmbargoNotFoundError('Embargo nao encontrado')
        item.suspender(motivo)
        return await self._embargo_repo.save(item)

    async def levantar_embargo(self, numero_embargo: str, *, observacoes: str | None=None) -> Embargo:
        item = await self._embargo_repo.get_by_numero(numero_embargo)
        if not item:
            raise EmbargoNotFoundError('Embargo nao encontrado')
        item.levantar(observacoes)
        return await self._embargo_repo.save(item)

    async def aplicar_multa(self, *, numero_auto_infracao: str, valor: Decimal, dias_vencimento: int=30) -> Multa:
        auto = await self._auto_infracao_repo.get_by_numero(numero_auto_infracao)
        if not auto:
            raise AutoInfracaoNotFoundError('Auto de infracao nao encontrado')
        item = Multa.aplicar(numero_auto_infracao=numero_auto_infracao, valor=valor, dias_vencimento=dias_vencimento)
        item.numero_multa = await self._multa_repo.next_numero()
        return await self._multa_repo.save(item)

    async def parcelar_multa(self, numero_multa: str, *, quantidade_parcelas: int) -> Multa:
        item = await self._multa_repo.get_by_numero(numero_multa)
        if not item:
            raise MultaNotFoundError('Multa nao encontrada')
        item.atualizar_vencimento()
        item.parcelar(quantidade_parcelas)
        return await self._multa_repo.save(item)

    async def registrar_pagamento_multa(self, numero_multa: str) -> Multa:
        item = await self._multa_repo.get_by_numero(numero_multa)
        if not item:
            raise MultaNotFoundError('Multa nao encontrada')
        item.atualizar_vencimento()
        item.registrar_pagamento()
        return await self._multa_repo.save(item)

    async def cancelar_multa(self, numero_multa: str, *, motivo: str) -> Multa:
        item = await self._multa_repo.get_by_numero(numero_multa)
        if not item:
            raise MultaNotFoundError('Multa nao encontrada')
        item.cancelar(motivo)
        return await self._multa_repo.save(item)

    async def obter_auto_por_numero(self, numero_auto: str) -> AutoInfracao:
        item = await self._auto_infracao_repo.get_by_numero(numero_auto)
        if not item:
            raise AutoInfracaoNotFoundError('Auto de infracao nao encontrado')
        return item

    async def listar_autos(self, *, numero_fiscalizacao: str | None=None, tipo: TipoAutoInfracao | None=None, status: StatusAutoInfracao | None=None) -> list[AutoInfracao]:
        return await self._auto_infracao_repo.list(numero_fiscalizacao=numero_fiscalizacao, tipo=tipo, status=status)

    async def obter_embargo_por_numero(self, numero_embargo: str) -> Embargo:
        item = await self._embargo_repo.get_by_numero(numero_embargo)
        if not item:
            raise EmbargoNotFoundError('Embargo nao encontrado')
        return item

    async def listar_embargos(self, *, numero_auto_infracao: str | None=None, status: StatusEmbargo | None=None) -> list[Embargo]:
        return await self._embargo_repo.list(numero_auto_infracao=numero_auto_infracao, status=status)

    async def obter_multa_por_numero(self, numero_multa: str) -> Multa:
        item = await self._multa_repo.get_by_numero(numero_multa)
        if not item:
            raise MultaNotFoundError('Multa nao encontrada')
        item.atualizar_vencimento()
        return item

    async def listar_multas(self, *, numero_auto_infracao: str | None=None, status: StatusMulta | None=None) -> list[Multa]:
        items = await self._multa_repo.list(numero_auto_infracao=numero_auto_infracao, status=status)
        for item in items:
            item.atualizar_vencimento()
        return items