from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.operacao_urbana_repository_port import OperacaoUrbanaRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusOperacaoUrbana, TipoOperacaoUrbana
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.operacao_urbana import OperacaoUrbana
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import OperacaoUrbanaAlreadyExistsError, OperacaoUrbanaNotFoundError

class OperacaoUrbanaService:

    def __init__(self, *, operacao_urbana_repo: OperacaoUrbanaRepositoryPort) -> None:
        self._operacao_urbana_repo = operacao_urbana_repo

    async def criar(self, *, nome: str, tipo: TipoOperacaoUrbana, plano_diretor_id: UUID, orgao_responsavel_id: UUID, provincia: str, municipio: str | None=None, area_intervencao: Decimal | None=None, investimento_previsto: Decimal | None=None, data_inicio_prevista: date | None=None, data_fim_prevista: date | None=None, codigo_operacao: str | None=None) -> OperacaoUrbana:
        codigo = codigo_operacao or await self._operacao_urbana_repo.next_codigo()
        existente = await self._operacao_urbana_repo.get_by_codigo(codigo)
        if existente:
            raise OperacaoUrbanaAlreadyExistsError('Ja existe operacao urbana com este codigo')
        item = OperacaoUrbana.criar(codigo_operacao=codigo, nome=nome, tipo=tipo, plano_diretor_id=plano_diretor_id, orgao_responsavel_id=orgao_responsavel_id, provincia=provincia, municipio=municipio, area_intervencao=area_intervencao, investimento_previsto=investimento_previsto, data_inicio_prevista=data_inicio_prevista, data_fim_prevista=data_fim_prevista)
        return await self._operacao_urbana_repo.save(item)

    async def aprovar(self, codigo_operacao: str) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.aprovar()
        return await self._operacao_urbana_repo.save(item)

    async def iniciar_execucao(self, codigo_operacao: str, *, data_inicio_real: date) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.iniciar_execucao(data_inicio_real=data_inicio_real)
        return await self._operacao_urbana_repo.save(item)

    async def atualizar_execucao(self, codigo_operacao: str, *, percentual_execucao: Decimal, investimento_executado: Decimal | None=None) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.atualizar_execucao(percentual_execucao=percentual_execucao, investimento_executado=investimento_executado)
        return await self._operacao_urbana_repo.save(item)

    async def concluir(self, codigo_operacao: str, *, data_fim_real: date) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.concluir(data_fim_real=data_fim_real)
        return await self._operacao_urbana_repo.save(item)

    async def suspender(self, codigo_operacao: str, *, motivo: str) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.suspender(motivo=motivo)
        return await self._operacao_urbana_repo.save(item)

    async def retomar(self, codigo_operacao: str) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.retomar()
        return await self._operacao_urbana_repo.save(item)

    async def cancelar(self, codigo_operacao: str, *, motivo: str) -> OperacaoUrbana:
        item = await self._obter_ou_erro(codigo_operacao)
        item.cancelar(motivo=motivo)
        return await self._operacao_urbana_repo.save(item)

    async def obter_por_codigo(self, codigo_operacao: str) -> OperacaoUrbana:
        return await self._obter_ou_erro(codigo_operacao)

    async def listar(self, *, status: StatusOperacaoUrbana | None=None, tipo: TipoOperacaoUrbana | None=None, provincia: str | None=None) -> list[OperacaoUrbana]:
        return await self._operacao_urbana_repo.list(status=status, tipo=tipo, provincia=provincia)

    async def _obter_ou_erro(self, codigo_operacao: str) -> OperacaoUrbana:
        item = await self._operacao_urbana_repo.get_by_codigo(codigo_operacao)
        if not item:
            raise OperacaoUrbanaNotFoundError('Operacao urbana nao encontrada')
        return item