from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.infrastructure.application.ports.licitacao_repository_port import LicitacaoRepositoryPort
from app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao
from app.modules.infrastructure.domain.models.licitacao import Licitacao
from app.modules.infrastructure.core.exceptions import LicitacaoAlreadyExistsError, LicitacaoNotFoundError

class LicitacaoService:

    def __init__(self, *, licitacao_repo: LicitacaoRepositoryPort) -> None:
        self._licitacao_repo = licitacao_repo

    async def abrir(self, *, objeto: str, tipo: TipoLicitacao, obra_id: UUID, orgao_responsavel_id: UUID, valor_estimado: Decimal, data_publicacao_edital: date, data_entrega_propostas: date, numero_licitacao: str | None=None) -> Licitacao:
        numero = numero_licitacao or await self._licitacao_repo.next_numero()
        existente = await self._licitacao_repo.get_by_numero(numero)
        if existente:
            raise LicitacaoAlreadyExistsError('Ja existe licitacao com este numero')
        item = Licitacao.abrir(numero_licitacao=numero, objeto=objeto, tipo=tipo, obra_id=obra_id, orgao_responsavel_id=orgao_responsavel_id, valor_estimado=valor_estimado, data_publicacao_edital=data_publicacao_edital, data_entrega_propostas=data_entrega_propostas)
        return await self._licitacao_repo.save(item)

    async def iniciar_recebimento(self, numero_licitacao: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.iniciar_recebimento_propostas()
        return await self._licitacao_repo.save(item)

    async def encerrar_recebimento(self, numero_licitacao: str, *, data_abertura: date) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.encerrar_recebimento_propostas(data_abertura=data_abertura)
        return await self._licitacao_repo.save(item)

    async def iniciar_analise(self, numero_licitacao: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.iniciar_analise()
        return await self._licitacao_repo.save(item)

    async def abrir_habilitacao(self, numero_licitacao: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.abrir_habilitacao()
        return await self._licitacao_repo.save(item)

    async def iniciar_recursos(self, numero_licitacao: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.iniciar_recursos()
        return await self._licitacao_repo.save(item)

    async def adjudicar(self, numero_licitacao: str, *, vencedor_id: UUID, valor_adjudicado: Decimal) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.adjudicar(vencedor_id=vencedor_id, valor_adjudicado=valor_adjudicado)
        return await self._licitacao_repo.save(item)

    async def homologar(self, numero_licitacao: str, *, data_homologacao: date | None=None) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.homologar(data_homologacao=data_homologacao)
        return await self._licitacao_repo.save(item)

    async def declarar_deserta(self, numero_licitacao: str, *, motivo: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.declarar_deserta(motivo)
        return await self._licitacao_repo.save(item)

    async def revogar(self, numero_licitacao: str, *, motivo: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.revogar(motivo)
        return await self._licitacao_repo.save(item)

    async def anular(self, numero_licitacao: str, *, motivo: str) -> Licitacao:
        item = await self._obter_ou_erro(numero_licitacao)
        item.anular(motivo)
        return await self._licitacao_repo.save(item)

    async def obter_por_numero(self, numero_licitacao: str) -> Licitacao:
        return await self._obter_ou_erro(numero_licitacao)

    async def listar(self, *, status: StatusLicitacao | None=None, tipo: TipoLicitacao | None=None, obra_id: UUID | None=None, orgao_responsavel_id: UUID | None=None) -> list[Licitacao]:
        return await self._licitacao_repo.list(status=status, tipo=tipo, obra_id=obra_id, orgao_responsavel_id=orgao_responsavel_id)

    async def _obter_ou_erro(self, numero_licitacao: str) -> Licitacao:
        item = await self._licitacao_repo.get_by_numero(numero_licitacao)
        if not item:
            raise LicitacaoNotFoundError('Licitacao nao encontrada')
        return item
