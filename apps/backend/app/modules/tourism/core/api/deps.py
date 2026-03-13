from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from app.modules.tourism.application.services.agencia_viagens_service import AgenciaViagensService
from app.modules.tourism.application.services.atracao_service import AtracaoService
from app.modules.tourism.application.services.meio_hospedagem_service import MeioHospedagemService
from app.modules.tourism.application.services.roteiro_service import RoteiroService
from app.modules.tourism.infrastructure.adapters.comercio_servicos_service_adapter import ComercioServicosServiceAdapter
from app.modules.tourism.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from app.modules.tourism.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from app.modules.tourism.infrastructure.adapters.transportes_logistica_service_adapter import TransportesLogisticaServiceAdapter
from app.modules.tourism.infrastructure.repositories.sqlalchemy_agencia_viagens_repository import SQLAlchemyAgenciaViagensRepository
from app.modules.tourism.infrastructure.repositories.sqlalchemy_atracao_turistica_repository import SQLAlchemyAtracaoTuristicaRepository
from app.modules.tourism.infrastructure.repositories.sqlalchemy_hotel_repository import SQLAlchemyHotelRepository
from app.modules.tourism.infrastructure.repositories.sqlalchemy_pousada_repository import SQLAlchemyPousadaRepository
from app.modules.tourism.infrastructure.repositories.sqlalchemy_roteiro_repository import SQLAlchemyRoteiroRepository
_hotel_repo_singleton = SQLAlchemyHotelRepository()
_pousada_repo_singleton = SQLAlchemyPousadaRepository()
_atracao_repo_singleton = SQLAlchemyAtracaoTuristicaRepository()
_agencia_repo_singleton = SQLAlchemyAgenciaViagensRepository()
_roteiro_repo_singleton = SQLAlchemyRoteiroRepository()

class _NoopTransportesService:

    async def list_opcoes_transporte(self, *, origem: str, destino: str) -> list[str]:
        return ['rodoviario', 'taxi', 'transfer_privado']

    async def estimate_tempo_viagem_horas(self, *, origem: str, destino: str, modal: str | None=None) -> float | None:
        return None

class _NoopComercioService:

    async def list_parceiros_turisticos(self, *, municipio: str) -> list[str]:
        base = municipio.strip().title()
        return [f'{base} Centro Comercial', f'{base} Gastronomia Local']

    async def agencia_cnpj_ativo(self, *, cnpj: str) -> bool:
        return True
_transportes_adapter_singleton = TransportesLogisticaServiceAdapter(_NoopTransportesService())
_comercio_adapter_singleton = ComercioServicosServiceAdapter(_NoopComercioService())

async def get_hotel_service(session: AsyncSession=Depends(get_db)) -> MeioHospedagemService:
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return MeioHospedagemService(hotel_repo=_hotel_repo_singleton, pousada_repo=_pousada_repo_singleton, citizen_service=citizen_service, request_service=request_service)

async def get_pousada_service(session: AsyncSession=Depends(get_db)) -> MeioHospedagemService:
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return MeioHospedagemService(hotel_repo=_hotel_repo_singleton, pousada_repo=_pousada_repo_singleton, citizen_service=citizen_service, request_service=request_service)

async def get_atracao_service() -> AtracaoService:
    return AtracaoService(repository=_atracao_repo_singleton)

async def get_agencia_service(session: AsyncSession=Depends(get_db)) -> AgenciaViagensService:
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return AgenciaViagensService(repository=_agencia_repo_singleton, citizen_service=citizen_service, comercio_service=_comercio_adapter_singleton, request_service=request_service)

async def get_roteiro_service() -> RoteiroService:
    return RoteiroService(repository=_roteiro_repo_singleton, transportes_service=_transportes_adapter_singleton, comercio_service=_comercio_adapter_singleton)
