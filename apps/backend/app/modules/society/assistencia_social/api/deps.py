from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.core.bridges.society_repository_bridges import make_educacao_matricula_repository
from app.modules.society.assistencia_social.application.services import AtendimentoService, BeneficiarioService, BeneficioService, CadastroUnicoService, CriancaRiscoService, IdosoVulneravelService, PCDService, ProgramaSocialService, SituacaoRuaService, VisitaDomiciliarService
from app.modules.society.assistencia_social.infrastructure.adapters import CitizenServiceAdapter, EducacaoServiceAdapter, EmpregoServiceAdapter, JuventudeServiceAdapter, RequestServiceAdapter, SaudeServiceAdapter
from app.modules.society.assistencia_social.infrastructure.repositories import SQLAlchemyAtendimentoRepository, SQLAlchemyBeneficiarioRepository, SQLAlchemyBeneficioRepository, SQLAlchemyCadastroUnicoRepository, SQLAlchemyCriancaRiscoRepository, SQLAlchemyIdosoVulneravelRepository, SQLAlchemyPCDRepository, SQLAlchemyProgramaSocialRepository, SQLAlchemySituacaoRuaRepository, SQLAlchemyVisitaDomiciliarRepository
from app.modules.society.emprego.infrastructure.repositories.sqlalchemy_candidato_repository import SQLAlchemyCandidatoRepository
from app.modules.society.juventude.infrastructure.repositories.sqlalchemy_jovem_repository import SQLAlchemyJovemRepository

def _bridges(session: AsyncSession):
    return (CitizenServiceAdapter(CitizenRepository(session)), EducacaoServiceAdapter(make_educacao_matricula_repository(session)), SaudeServiceAdapter(), JuventudeServiceAdapter(SQLAlchemyJovemRepository(session)), EmpregoServiceAdapter(SQLAlchemyCandidatoRepository(session)), RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_beneficiario_service(session: AsyncSession=Depends(get_db)) -> BeneficiarioService:
    citizen, _, _, _, _, request = _bridges(session)
    return BeneficiarioService(beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), citizen_service=citizen, cadastro_unico_repo=SQLAlchemyCadastroUnicoRepository(session), request_service=request)

async def get_cadastro_unico_service(session: AsyncSession=Depends(get_db)) -> CadastroUnicoService:
    citizen, educacao, _, juventude, _, request = _bridges(session)
    return CadastroUnicoService(cadastro_repo=SQLAlchemyCadastroUnicoRepository(session), citizen_service=citizen, educacao_service=educacao, juventude_service=juventude, request_service=request)

async def get_programa_social_service(session: AsyncSession=Depends(get_db)) -> ProgramaSocialService:
    return ProgramaSocialService(programa_repo=SQLAlchemyProgramaSocialRepository(session))

async def get_beneficio_service(session: AsyncSession=Depends(get_db)) -> BeneficioService:
    _, _, saude, _, emprego, request = _bridges(session)
    return BeneficioService(beneficio_repo=SQLAlchemyBeneficioRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), programa_repo=SQLAlchemyProgramaSocialRepository(session), pcd_repo=SQLAlchemyPCDRepository(session), saude_service=saude, emprego_service=emprego, request_service=request)

async def get_atendimento_service(session: AsyncSession=Depends(get_db)) -> AtendimentoService:
    _, _, _, _, _, request = _bridges(session)
    return AtendimentoService(atendimento_repo=SQLAlchemyAtendimentoRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), request_service=request)

async def get_visita_domiciliar_service(session: AsyncSession=Depends(get_db)) -> VisitaDomiciliarService:
    _, _, saude, _, _, request = _bridges(session)
    return VisitaDomiciliarService(visita_repo=SQLAlchemyVisitaDomiciliarRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), saude_service=saude, request_service=request)

async def get_situacao_rua_service(session: AsyncSession=Depends(get_db)) -> SituacaoRuaService:
    _, _, _, _, _, request = _bridges(session)
    return SituacaoRuaService(situacao_repo=SQLAlchemySituacaoRuaRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), request_service=request)

async def get_crianca_risco_service(session: AsyncSession=Depends(get_db)) -> CriancaRiscoService:
    _, educacao, _, _, _, request = _bridges(session)
    return CriancaRiscoService(crianca_repo=SQLAlchemyCriancaRiscoRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), educacao_service=educacao, request_service=request)

async def get_idoso_vulneravel_service(session: AsyncSession=Depends(get_db)) -> IdosoVulneravelService:
    _, _, saude, _, _, request = _bridges(session)
    return IdosoVulneravelService(idoso_repo=SQLAlchemyIdosoVulneravelRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), saude_service=saude, request_service=request)

async def get_pcd_service(session: AsyncSession=Depends(get_db)) -> PCDService:
    _, _, saude, _, _, request = _bridges(session)
    return PCDService(pcd_repo=SQLAlchemyPCDRepository(session), beneficiario_repo=SQLAlchemyBeneficiarioRepository(session), saude_service=saude, request_service=request)