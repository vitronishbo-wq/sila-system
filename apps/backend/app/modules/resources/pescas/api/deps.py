from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.resources.pescas.application.ports import ArmadorRepositoryPort
from apps.backend.app.modules.resources.pescas.application.services import (
    ArmadorService,
    CapturaService,
    ComercializacaoService,
    DefesoService,
    DesembarqueService,
    EmbarcacaoService,
    FiscalizacaoService,
    LicenciamentoPescaService,
    PescadorService,
    ProducaoPescaService,
    QuotaService,
    RastreabilidadeService,
)
from apps.backend.app.modules.resources.pescas.domain.models.armador import Armador
from apps.backend.app.modules.resources.pescas.domain.models.especie import Especie
from apps.backend.app.modules.resources.pescas.infrastructure.adapters import (
    CitizenServiceAdapter,
    RequestServiceAdapter,
)
from apps.backend.app.modules.resources.pescas.infrastructure.repositories import (
    SQLAlchemyCapturaRepository,
    SQLAlchemyEmbarcacaoRepository,
    SQLAlchemyLicencaPescaRepository,
    SQLAlchemyPescadorRepository,
)


class _InMemoryArmadorRepository(ArmadorRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Armador] = {}

    async def save(self, armador: Armador) -> Armador:
        self._items[armador.id] = armador
        return armador

    async def get_by_id(self, armador_id: UUID) -> Armador | None:
        return self._items.get(armador_id)

    async def get_by_nif(self, nif: str) -> Armador | None:
        for item in self._items.values():
            if item.nif == nif:
                return item
        return None

    async def list_all(self, ativo: bool | None = None) -> list[Armador]:
        values = list(self._items.values())
        if ativo is None:
            return values
        return [item for item in values if item.ativo is ativo]


@dataclass
class _EspecieCatalogService:
    _items: dict[UUID, Especie]

    async def cadastrar(self, *, nome_comum: str, nome_cientifico: str, codigo_fao: str) -> Especie:
        item = Especie.cadastrar(
            nome_comum=nome_comum, nome_cientifico=nome_cientifico, codigo_fao=codigo_fao
        )
        self._items[item.id] = item
        return item

    async def listar(self) -> list[Especie]:
        return list(self._items.values())

    async def obter(self, especie_id: UUID) -> Especie | None:
        return self._items.get(especie_id)


_armador_repo_singleton = _InMemoryArmadorRepository()
_quota_service_singleton = QuotaService()
_defeso_service_singleton = DefesoService()
_desembarque_service_singleton = DesembarqueService()
_producao_service_singleton = ProducaoPescaService()
_comercializacao_service_singleton = ComercializacaoService()
_fiscalizacao_service_singleton = FiscalizacaoService()
_rastreabilidade_service_singleton = RastreabilidadeService()
_especie_catalog_singleton = _EspecieCatalogService(_items={})
db_dep = Depends(get_db)


async def get_pescador_service(session: AsyncSession = db_dep) -> PescadorService:
    repository = SQLAlchemyPescadorRepository(session)
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return PescadorService(
        pescador_repo=repository, citizen_service=citizen_service, request_service=request_service
    )


async def get_armador_service() -> ArmadorService:
    return ArmadorService(repository=_armador_repo_singleton)


async def get_embarcacao_service(session: AsyncSession = db_dep) -> EmbarcacaoService:
    repository = SQLAlchemyEmbarcacaoRepository(session)
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return EmbarcacaoService(
        embarcacao_repo=repository, citizen_service=citizen_service, request_service=request_service
    )


async def get_licenciamento_pesca_service(
    session: AsyncSession = db_dep,
) -> LicenciamentoPescaService:
    return LicenciamentoPescaService(
        licenca_repo=SQLAlchemyLicencaPescaRepository(session),
        embarcacao_repo=SQLAlchemyEmbarcacaoRepository(session),
    )


async def get_captura_service(session: AsyncSession = db_dep) -> CapturaService:
    return CapturaService(
        captura_repo=SQLAlchemyCapturaRepository(session),
        licenca_repo=SQLAlchemyLicencaPescaRepository(session),
    )


async def get_quota_service() -> QuotaService:
    return _quota_service_singleton


async def get_defeso_service() -> DefesoService:
    return _defeso_service_singleton


async def get_desembarque_service() -> DesembarqueService:
    return _desembarque_service_singleton


async def get_producao_service() -> ProducaoPescaService:
    return _producao_service_singleton


async def get_comercializacao_service() -> ComercializacaoService:
    return _comercializacao_service_singleton


async def get_fiscalizacao_service() -> FiscalizacaoService:
    return _fiscalizacao_service_singleton


async def get_rastreabilidade_service() -> RastreabilidadeService:
    return _rastreabilidade_service_singleton


async def get_especie_catalog_service() -> _EspecieCatalogService:
    return _especie_catalog_singleton