from __future__ import annotations
from uuid import UUID
from app.modules.governance.cooperacao_internacional.application.ports.projeto_repository_port import ProjetoCooperacaoRepositoryPort
from app.modules.governance.cooperacao_internacional.domain.models.projeto_cooperacao import ProjetoCooperacao

class InMemoryProjetoCooperacaoRepository(ProjetoCooperacaoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, ProjetoCooperacao] = {}

    async def save(self, projeto: ProjetoCooperacao) -> ProjetoCooperacao:
        self._items[projeto.id] = projeto
        return projeto

    async def get_by_id(self, projeto_id: UUID) -> ProjetoCooperacao | None:
        return self._items.get(projeto_id)

    async def list_all(self) -> list[ProjetoCooperacao]:
        return list(self._items.values())