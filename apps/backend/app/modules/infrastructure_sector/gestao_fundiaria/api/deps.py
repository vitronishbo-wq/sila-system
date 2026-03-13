from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.api.deps import get_db
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.desapropriacao_service import DesapropriacaoService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.georreferenciamento_service import GeorreferenciamentoService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import ImovelService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.matricula_imovel_service import MatriculaImovelService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.oneracao_service import OneracaoService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.proprietario_service import ProprietarioService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.ambiente_service_adapter import AmbienteServiceAdapter
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.justica_service_adapter import JusticaServiceAdapter
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import SQLAlchemyGeorreferenciamentoRepository, SQLAlchemyDesapropriacaoRepository, SQLAlchemyImovelRepository, SQLAlchemyMatriculaImovelRepository, SQLAlchemyOneracaoRepository, SQLAlchemyProprietarioRepository
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.geosampa_service_adapter import GeosampaServiceAdapter

async def get_imovel_service(session: AsyncSession=Depends(get_db)) -> ImovelService:
    return ImovelService(imovel_repo=SQLAlchemyImovelRepository(session))

async def get_proprietario_service(session: AsyncSession=Depends(get_db)) -> ProprietarioService:
    return ProprietarioService(proprietario_repo=SQLAlchemyProprietarioRepository(session))

async def get_oneracao_service(session: AsyncSession=Depends(get_db)) -> OneracaoService:
    return OneracaoService(oneracao_repo=SQLAlchemyOneracaoRepository(session), imovel_repo=SQLAlchemyImovelRepository(session), justica_adapter=JusticaServiceAdapter())

async def get_desapropriacao_service(session: AsyncSession=Depends(get_db)) -> DesapropriacaoService:
    return DesapropriacaoService(desapropriacao_repo=SQLAlchemyDesapropriacaoRepository(session), imovel_repo=SQLAlchemyImovelRepository(session), ambiente_adapter=AmbienteServiceAdapter())

async def get_matricula_service(session: AsyncSession=Depends(get_db)) -> MatriculaImovelService:
    return MatriculaImovelService(matricula_repo=SQLAlchemyMatriculaImovelRepository(session), imovel_repo=SQLAlchemyImovelRepository(session), justica_adapter=JusticaServiceAdapter())

async def get_georreferenciamento_service(session: AsyncSession=Depends(get_db)) -> GeorreferenciamentoService:
    return GeorreferenciamentoService(georreferenciamento_repo=SQLAlchemyGeorreferenciamentoRepository(session), imovel_repo=SQLAlchemyImovelRepository(session), geosampa_adapter=GeosampaServiceAdapter())