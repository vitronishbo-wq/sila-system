from __future__ import annotations

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

db_dep = Depends(get_db)

from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.instituicao_pesquisa_service import (
    InstituicaoPesquisaService,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.pesquisador_service import (
    PesquisadorService,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.services.projeto_pesquisa_service import (
    ProjetoPesquisaService,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.infrastructure.repositories.sqlalchemy_instituicao_pesquisa_repository import (
    SQLAlchemyInstituicaoPesquisaRepository,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.infrastructure.repositories.sqlalchemy_pesquisador_repository import (
    SQLAlchemyPesquisadorRepository,
)
from apps.backend.app.modules.intelligence.ciencia_pesquisa.infrastructure.repositories.sqlalchemy_projeto_pesquisa_repository import (
    SQLAlchemyProjetoPesquisaRepository,
)


async def get_projeto_pesquisa_service(
    session: AsyncSession = db_dep,
) -> ProjetoPesquisaService:
    projeto_repo = SQLAlchemyProjetoPesquisaRepository(session)
    instituicao_repo = SQLAlchemyInstituicaoPesquisaRepository(session)
    pesquisador_repo = SQLAlchemyPesquisadorRepository(session)
    return ProjetoPesquisaService(
        projeto_repo=projeto_repo,
        instituicao_repo=instituicao_repo,
        pesquisador_repo=pesquisador_repo,
    )


async def get_pesquisador_service(session: AsyncSession = db_dep) -> PesquisadorService:
    instituicao_repo = SQLAlchemyInstituicaoPesquisaRepository(session)
    pesquisador_repo = SQLAlchemyPesquisadorRepository(session)
    return PesquisadorService(pesquisador_repo=pesquisador_repo, instituicao_repo=instituicao_repo)


async def get_instituicao_pesquisa_service(
    session: AsyncSession = db_dep,
) -> InstituicaoPesquisaService:
    instituicao_repo = SQLAlchemyInstituicaoPesquisaRepository(session)
    return InstituicaoPesquisaService(instituicao_repo=instituicao_repo)