from __future__ import annotations
from fastapi import Depends
from apps.backend.app.api.deps import get_db
from apps.backend.app.domain.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.society.emprego.application.services import CandidatoService, CertificacaoService, ConcursoService, FormacaoService, MediacaoService, OfertaService, TrabalhoService
from apps.backend.app.modules.society.emprego.infrastructure.adapters import CitizenServiceAdapter, RequestServiceAdapter
from apps.backend.app.modules.society.emprego.infrastructure.repositories import SQLAlchemyCandidatoRepository, SQLAlchemyCertificacaoRepository, SQLAlchemyConcursoRepository, SQLAlchemyFormacaoRepository, SQLAlchemyMediacaoRepository, SQLAlchemyOfertaRepository, SQLAlchemyReclamacaoRepository

def _bridges(session):
    citizen = CitizenServiceAdapter(CitizenRepository(session))
    request = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return (citizen, request)

async def get_candidato_service(session=Depends(get_db)) -> CandidatoService:
    citizen, request = _bridges(session)
    return CandidatoService(candidato_repo=SQLAlchemyCandidatoRepository(session), citizen_repo=citizen, request_service=request)

async def get_oferta_service(session=Depends(get_db)) -> OfertaService:
    citizen, request = _bridges(session)
    return OfertaService(repository=SQLAlchemyOfertaRepository(session), citizen_service=citizen, request_service=request)

async def get_mediacao_service(session=Depends(get_db)) -> MediacaoService:
    citizen, request = _bridges(session)
    return MediacaoService(repository=SQLAlchemyMediacaoRepository(session), citizen_service=citizen, request_service=request)

async def get_formacao_service(session=Depends(get_db)) -> FormacaoService:
    citizen, request = _bridges(session)
    return FormacaoService(repository=SQLAlchemyFormacaoRepository(session), citizen_service=citizen, request_service=request)

async def get_trabalho_service(session=Depends(get_db)) -> TrabalhoService:
    citizen, request = _bridges(session)
    return TrabalhoService(repository=SQLAlchemyReclamacaoRepository(session), citizen_service=citizen, request_service=request)

async def get_concurso_service(session=Depends(get_db)) -> ConcursoService:
    citizen, request = _bridges(session)
    return ConcursoService(repository=SQLAlchemyConcursoRepository(session), citizen_service=citizen, request_service=request)

async def get_certificacao_service(session=Depends(get_db)) -> CertificacaoService:
    citizen, request = _bridges(session)
    return CertificacaoService(repository=SQLAlchemyCertificacaoRepository(session), citizen_service=citizen, request_service=request)