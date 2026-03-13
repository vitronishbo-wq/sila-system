from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.core.bridges.society_repository_bridges import make_educacao_matricula_repository
from apps.backend.app.modules.society.emprego.infrastructure.repositories.sqlalchemy_candidato_repository import SQLAlchemyCandidatoRepository
from apps.backend.app.modules.society.juventude.application.services.auxilio_service import AuxilioService
from apps.backend.app.modules.society.juventude.application.services.acompanhamento_juvenil_service import AcompanhamentoJuvenilService
from apps.backend.app.modules.society.juventude.application.services.bolsa_estudo_service import BolsaEstudoService
from apps.backend.app.modules.society.juventude.application.services.empreendedorismo_juvenil_service import EmpreendedorismoJuvenilService
from apps.backend.app.modules.society.juventude.application.services.estagio_juvenil_service import EstagioJuvenilService
from apps.backend.app.modules.society.juventude.application.services.evento_juvenil_service import EventoJuvenilService
from apps.backend.app.modules.society.juventude.application.services.formacao_service import FormacaoService
from apps.backend.app.modules.society.juventude.application.services.inscricao_programa_service import InscricaoProgramaService
from apps.backend.app.modules.society.juventude.application.services.intercambio_juvenil_service import IntercambioJuvenilService
from apps.backend.app.modules.society.juventude.application.services.jovem_service import JovemService
from apps.backend.app.modules.society.juventude.application.services.mentor_service import MentorService
from apps.backend.app.modules.society.juventude.application.services.politica_juventude_service import PoliticaJuventudeService
from apps.backend.app.modules.society.juventude.application.services.programa_service import ProgramaService
from apps.backend.app.modules.society.juventude.application.services.risco_evasao_service import RiscoEvasaoService
from apps.backend.app.modules.society.juventude.application.services.saude_juvenil_service import SaudeJuvenilService
from apps.backend.app.modules.society.juventude.application.services.voluntariado_service import VoluntariadoService
from apps.backend.app.modules.society.juventude.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.society.juventude.infrastructure.adapters.educacao_service_adapter import EducacaoServiceAdapter
from apps.backend.app.modules.society.juventude.infrastructure.adapters.emprego_service_adapter import EmpregoServiceAdapter
from apps.backend.app.modules.society.juventude.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_auxilio_repository import SQLAlchemyAuxilioRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_acompanhamento_juvenil_repository import SQLAlchemyAcompanhamentoJuvenilRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_bolsa_estudo_repository import SQLAlchemyBolsaEstudoRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_empreendedorismo_juvenil_repository import SQLAlchemyEmpreendedorismoJuvenilRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_estagio_juvenil_repository import SQLAlchemyEstagioJuvenilRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_evento_juvenil_repository import SQLAlchemyEventoJuvenilRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_formacao_repository import SQLAlchemyFormacaoRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_inscricao_programa_repository import SQLAlchemyInscricaoProgramaRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_intercambio_juvenil_repository import SQLAlchemyIntercambioJuvenilRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_jovem_repository import SQLAlchemyJovemRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_mentor_repository import SQLAlchemyMentorRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_politica_juventude_repository import SQLAlchemyPoliticaJuventudeRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_programa_repository import SQLAlchemyProgramaRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_risco_evasao_repository import SQLAlchemyRiscoEvasaoRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_saude_juvenil_repository import SQLAlchemySaudeJuvenilRepository
from apps.backend.app.modules.society.juventude.infrastructure.repositories.sqlalchemy_voluntariado_repository import SQLAlchemyVoluntariadoRepository

def _get_request_service(session: AsyncSession) -> RequestServiceAdapter:
    return RequestServiceAdapter(ServiceRequestLifecycleBridge(session))

def _get_citizen_service(session: AsyncSession) -> CitizenServiceAdapter:
    return CitizenServiceAdapter(CitizenRepository(session))

def _get_educacao_service(session: AsyncSession) -> EducacaoServiceAdapter:
    return EducacaoServiceAdapter(make_educacao_matricula_repository(session))

def _get_emprego_service(session: AsyncSession) -> EmpregoServiceAdapter:
    return EmpregoServiceAdapter(SQLAlchemyCandidatoRepository(session))

async def get_jovem_service(session: AsyncSession=Depends(get_db)) -> JovemService:
    return JovemService(jovem_repo=SQLAlchemyJovemRepository(session), citizen_service=_get_citizen_service(session), educacao_service=_get_educacao_service(session), emprego_service=_get_emprego_service(session), request_service=_get_request_service(session))

async def get_auxilio_service(session: AsyncSession=Depends(get_db)) -> AuxilioService:
    return AuxilioService(auxilio_repo=SQLAlchemyAuxilioRepository(session), jovem_repo=SQLAlchemyJovemRepository(session), request_service=_get_request_service(session))

async def get_programa_service(session: AsyncSession=Depends(get_db)) -> ProgramaService:
    return ProgramaService(programa_repo=SQLAlchemyProgramaRepository(session), request_service=_get_request_service(session))

async def get_formacao_service(session: AsyncSession=Depends(get_db)) -> FormacaoService:
    return FormacaoService(formacao_repo=SQLAlchemyFormacaoRepository(session), jovem_repo=SQLAlchemyJovemRepository(session), programa_repo=SQLAlchemyProgramaRepository(session), request_service=_get_request_service(session))

async def get_bolsa_estudo_service(session: AsyncSession=Depends(get_db)) -> BolsaEstudoService:
    return BolsaEstudoService(bolsa_repo=SQLAlchemyBolsaEstudoRepository(session), jovem_repo=SQLAlchemyJovemRepository(session), request_service=_get_request_service(session))

async def get_estagio_juvenil_service(session: AsyncSession=Depends(get_db)) -> EstagioJuvenilService:
    return EstagioJuvenilService(estagio_repo=SQLAlchemyEstagioJuvenilRepository(session), jovem_repo=SQLAlchemyJovemRepository(session), request_service=_get_request_service(session))

async def get_inscricao_programa_service(session: AsyncSession=Depends(get_db)) -> InscricaoProgramaService:
    return InscricaoProgramaService(inscricao_repo=SQLAlchemyInscricaoProgramaRepository(session), jovem_repo=SQLAlchemyJovemRepository(session), programa_repo=SQLAlchemyProgramaRepository(session), request_service=_get_request_service(session))

async def get_intercambio_juvenil_service(session: AsyncSession=Depends(get_db)) -> IntercambioJuvenilService:
    return IntercambioJuvenilService(intercambio_repo=SQLAlchemyIntercambioJuvenilRepository(session), jovem_repo=SQLAlchemyJovemRepository(session))

async def get_mentor_service(session: AsyncSession=Depends(get_db)) -> MentorService:
    return MentorService(mentor_repo=SQLAlchemyMentorRepository(session))

async def get_evento_juvenil_service(session: AsyncSession=Depends(get_db)) -> EventoJuvenilService:
    return EventoJuvenilService(evento_repo=SQLAlchemyEventoJuvenilRepository(session), jovem_repo=SQLAlchemyJovemRepository(session))

async def get_voluntariado_service(session: AsyncSession=Depends(get_db)) -> VoluntariadoService:
    return VoluntariadoService(voluntariado_repo=SQLAlchemyVoluntariadoRepository(session), jovem_repo=SQLAlchemyJovemRepository(session))

async def get_empreendedorismo_juvenil_service(session: AsyncSession=Depends(get_db)) -> EmpreendedorismoJuvenilService:
    return EmpreendedorismoJuvenilService(empreendedorismo_repo=SQLAlchemyEmpreendedorismoJuvenilRepository(session), jovem_repo=SQLAlchemyJovemRepository(session))

async def get_saude_juvenil_service(session: AsyncSession=Depends(get_db)) -> SaudeJuvenilService:
    return SaudeJuvenilService(saude_repo=SQLAlchemySaudeJuvenilRepository(session), jovem_repo=SQLAlchemyJovemRepository(session))

async def get_acompanhamento_juvenil_service(session: AsyncSession=Depends(get_db)) -> AcompanhamentoJuvenilService:
    return AcompanhamentoJuvenilService(acompanhamento_repo=SQLAlchemyAcompanhamentoJuvenilRepository(session), jovem_repo=SQLAlchemyJovemRepository(session))

async def get_politica_juventude_service(session: AsyncSession=Depends(get_db)) -> PoliticaJuventudeService:
    return PoliticaJuventudeService(politica_repo=SQLAlchemyPoliticaJuventudeRepository(session))

async def get_risco_evasao_service(session: AsyncSession=Depends(get_db)) -> RiscoEvasaoService:
    return RiscoEvasaoService(risco_repo=SQLAlchemyRiscoEvasaoRepository(session), jovem_repo=SQLAlchemyJovemRepository(session), educacao_service=_get_educacao_service(session), request_service=_get_request_service(session))