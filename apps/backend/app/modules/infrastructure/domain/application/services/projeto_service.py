from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure.application.ports.projeto_repository_port import ProjetoRepositoryPort
from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto
from apps.backend.app.modules.infrastructure.domain.models.projeto_obra import ProjetoObra
from apps.backend.app.modules.infrastructure.domain.exceptions import ProjetoAlreadyExistsError, ProjetoNotFoundError

class ProjetoService:

    def __init__(self, *, projeto_repo: ProjetoRepositoryPort) -> None:
        self._projeto_repo = projeto_repo

    async def criar(self, *, nome: str, tipo: TipoProjeto, orgao_responsavel_id: UUID, responsavel_tecnico_id: UUID, valor_estimado: Decimal, data_inicio_prevista: date, data_fim_prevista: date, codigo_projeto: str | None=None, obra_id: UUID | None=None, descricao: str | None=None) -> ProjetoObra:
        codigo = codigo_projeto or await self._projeto_repo.next_codigo()
        existente = await self._projeto_repo.get_by_codigo(codigo)
        if existente:
            raise ProjetoAlreadyExistsError('Ja existe projeto com este codigo')
        item = ProjetoObra.criar(codigo_projeto=codigo, nome=nome, tipo=tipo, orgao_responsavel_id=orgao_responsavel_id, responsavel_tecnico_id=responsavel_tecnico_id, valor_estimado=valor_estimado, data_inicio_prevista=data_inicio_prevista, data_fim_prevista=data_fim_prevista, obra_id=obra_id, descricao=descricao)
        return await self._projeto_repo.save(item)

    async def aprovar(self, codigo_projeto: str) -> ProjetoObra:
        item = await self._obter_ou_erro(codigo_projeto)
        item.aprovar()
        return await self._projeto_repo.save(item)

    async def iniciar_execucao(self, codigo_projeto: str, *, data_inicio: date) -> ProjetoObra:
        item = await self._obter_ou_erro(codigo_projeto)
        item.iniciar_execucao(data_inicio)
        return await self._projeto_repo.save(item)

    async def concluir(self, codigo_projeto: str, *, data_fim: date) -> ProjetoObra:
        item = await self._obter_ou_erro(codigo_projeto)
        item.concluir(data_fim)
        return await self._projeto_repo.save(item)

    async def revisar(self, codigo_projeto: str, *, motivo: str) -> ProjetoObra:
        item = await self._obter_ou_erro(codigo_projeto)
        item.revisar(motivo)
        return await self._projeto_repo.save(item)

    async def arquivar(self, codigo_projeto: str, *, motivo: str) -> ProjetoObra:
        item = await self._obter_ou_erro(codigo_projeto)
        item.arquivar(motivo)
        return await self._projeto_repo.save(item)

    async def obter_por_codigo(self, codigo_projeto: str) -> ProjetoObra:
        return await self._obter_ou_erro(codigo_projeto)

    async def listar(self, *, status: StatusProjeto | None=None, tipo: TipoProjeto | None=None, orgao_responsavel_id: UUID | None=None, obra_id: UUID | None=None) -> list[ProjetoObra]:
        return await self._projeto_repo.list(status=status, tipo=tipo, orgao_responsavel_id=orgao_responsavel_id, obra_id=obra_id)

    async def _obter_ou_erro(self, codigo_projeto: str) -> ProjetoObra:
        item = await self._projeto_repo.get_by_codigo(codigo_projeto)
        if not item:
            raise ProjetoNotFoundError('Projeto nao encontrado')
        return item
