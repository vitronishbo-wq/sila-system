from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.instituicao_pesquisa_repository_port import (
    InstituicaoPesquisaRepositoryPort,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.pesquisador_repository_port import (
    PesquisadorRepositoryPort,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.projeto_pesquisa_repository_port import (
    ProjetoPesquisaRepositoryPort,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import (
    InstituicaoPesquisa,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.pesquisador import (
    Pesquisador,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.projeto_pesquisa import (
    ProjetoPesquisa,
)


class InMemoryPesquisadorRepository(PesquisadorRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Pesquisador] = {}

    async def save(self, pesquisador: Pesquisador) -> Pesquisador:
        self._items[pesquisador.id] = pesquisador
        return pesquisador

    async def get_by_id(self, pesquisador_id: UUID) -> Pesquisador | None:
        return self._items.get(pesquisador_id)

    async def get_by_documento(self, documento_identificacao: str) -> Pesquisador | None:
        normalized = documento_identificacao.strip()
        for item in self._items.values():
            if item.documento_identificacao == normalized:
                return item
        return None

    async def get_by_email(self, email_institucional: str) -> Pesquisador | None:
        normalized = email_institucional.strip().lower()
        for item in self._items.values():
            if item.email_institucional.lower() == normalized:
                return item
        return None

    async def list_all(self) -> list[Pesquisador]:
        return sorted(self._items.values(), key=lambda item: item.nome_completo)

    async def list_by_instituicao(self, instituicao_id: UUID) -> list[Pesquisador]:
        items = [item for item in self._items.values() if item.instituicao_id == instituicao_id]
        return sorted(items, key=lambda item: item.nome_completo)

    async def vincular_instituicao(
        self, *, pesquisador_id: UUID, instituicao_id: UUID, unidade_pesquisa_id: UUID | None = None
    ) -> Pesquisador | None:
        pesquisador = self._items.get(pesquisador_id)
        if pesquisador is None:
            return None
        pesquisador.instituicao_id = instituicao_id
        pesquisador.unidade_pesquisa_id = unidade_pesquisa_id
        return pesquisador

    async def delete(self, pesquisador_id: UUID) -> bool:
        return self._items.pop(pesquisador_id, None) is not None


class InMemoryInstituicaoPesquisaRepository(InstituicaoPesquisaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, InstituicaoPesquisa] = {}

    async def save(self, instituicao: InstituicaoPesquisa) -> InstituicaoPesquisa:
        self._items[instituicao.id] = instituicao
        return instituicao

    async def get_by_id(self, instituicao_id: UUID) -> InstituicaoPesquisa | None:
        return self._items.get(instituicao_id)

    async def get_by_sigla(self, sigla: str) -> InstituicaoPesquisa | None:
        normalized = sigla.strip().upper()
        for item in self._items.values():
            if item.sigla.upper() == normalized:
                return item
        return None

    async def get_by_nif(self, nif: str) -> InstituicaoPesquisa | None:
        normalized = nif.strip()
        for item in self._items.values():
            if item.nif == normalized:
                return item
        return None

    async def list_all(self) -> list[InstituicaoPesquisa]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_ativas(self) -> list[InstituicaoPesquisa]:
        items = [item for item in self._items.values() if item.ativa]
        return sorted(items, key=lambda item: item.nome)

    async def delete(self, instituicao_id: UUID) -> bool:
        return self._items.pop(instituicao_id, None) is not None


class InMemoryProjetoPesquisaRepository(ProjetoPesquisaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, ProjetoPesquisa] = {}

    async def save(self, projeto: ProjetoPesquisa) -> ProjetoPesquisa:
        self._items[projeto.id] = projeto
        return projeto

    async def get_by_id(self, projeto_id: UUID) -> ProjetoPesquisa | None:
        return self._items.get(projeto_id)

    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoPesquisa | None:
        normalized = codigo_projeto.strip()
        for item in self._items.values():
            if item.codigo_projeto == normalized:
                return item
        return None

    async def list_all(self) -> list[ProjetoPesquisa]:
        return sorted(self._items.values(), key=lambda item: item.codigo_projeto)

    async def list_by_instituicao(self, instituicao_id: UUID) -> list[ProjetoPesquisa]:
        items = [item for item in self._items.values() if item.instituicao_id == instituicao_id]
        return sorted(items, key=lambda item: item.codigo_projeto)

    async def list_by_pesquisador(self, pesquisador_id: UUID) -> list[ProjetoPesquisa]:
        items = [
            item for item in self._items.values() if pesquisador_id in item.equipe_pesquisadores_ids
        ]
        return sorted(items, key=lambda item: item.codigo_projeto)

    async def vincular_pesquisadores(
        self, *, projeto_id: UUID, pesquisador_ids: list[UUID]
    ) -> ProjetoPesquisa | None:
        projeto = self._items.get(projeto_id)
        if projeto is None:
            return None
        projeto.vincular_pesquisadores(pesquisador_ids)
        return projeto

    async def delete(self, projeto_id: UUID) -> bool:
        return self._items.pop(projeto_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"PROJ/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_projeto.startswith(prefix))
        return f"{prefix}{count + 1:05d}"
