from __future__ import annotations

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.resources.agricultura.application.services.assistencia_service import (
    AssistenciaService,
)
from apps.backend.app.modules.resources.agricultura.application.services.certificacao_service import (
    CertificacaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.colheita_service import (
    ColheitaService,
)
from apps.backend.app.modules.resources.agricultura.application.services.comercializacao_service import (
    ComercializacaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.credito_service import (
    CreditoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.equipamento_service import (
    EquipamentoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.estoque_service import (
    EstoqueService,
)
from apps.backend.app.modules.resources.agricultura.application.services.fitossanidade_service import (
    FitossanidadeService,
)
from apps.backend.app.modules.resources.agricultura.application.services.insumo_service import (
    InsumoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.operacao_service import (
    OperacaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.plantio_service import (
    PlantioService,
)
from apps.backend.app.modules.resources.agricultura.application.services.producao_service import (
    ProducaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.produtor_service import (
    ProdutorService,
)
from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.agricultura.application.services.safra_service import (
    SafraService,
)
from apps.backend.app.modules.resources.agricultura.application.services.talhao_service import (
    TalhaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.zoneamento_service import (
    ZoneamentoService,
)
from apps.backend.app.modules.resources.agricultura.infrastructure.adapters import (
    CitizenServiceAdapter,
    RequestServiceAdapter,
)
from apps.backend.app.modules.resources.agricultura.infrastructure.repositories import (
    SQLAlchemyProdutorRepository,
)

propriedade_service_singleton = PropriedadeService()
producao_service_singleton = ProducaoService()
insumo_service_singleton = InsumoService()
safra_service_singleton = SafraService(
    propriedade_service=propriedade_service_singleton, producao_service=producao_service_singleton
)
estoque_service_singleton = EstoqueService(insumo_service=insumo_service_singleton)
operacao_service_singleton = OperacaoService(
    safra_service=safra_service_singleton, insumo_service=insumo_service_singleton
)
fitossanidade_service_singleton = FitossanidadeService(
    propriedade_service=propriedade_service_singleton
)
certificacao_service_singleton = CertificacaoService(
    propriedade_service=propriedade_service_singleton
)
comercializacao_service_singleton = ComercializacaoService(safra_service=safra_service_singleton)
credito_service_singleton = CreditoService()
assistencia_service_singleton = AssistenciaService(
    propriedade_service=propriedade_service_singleton
)
talhao_service_singleton = TalhaoService(propriedade_service=propriedade_service_singleton)
plantio_service_singleton = PlantioService(
    safra_service=safra_service_singleton, talhao_service=talhao_service_singleton
)
colheita_service_singleton = ColheitaService(
    safra_service=safra_service_singleton, talhao_service=talhao_service_singleton
)
equipamento_service_singleton = EquipamentoService()
zoneamento_service_singleton = ZoneamentoService(propriedade_service=propriedade_service_singleton)

db_dep = Depends(get_db)


async def get_produtor_service(session: AsyncSession = db_dep) -> ProdutorService:
    produtor_repo = SQLAlchemyProdutorRepository(session)
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return ProdutorService(
        produtor_repo=produtor_repo,
        citizen_service=citizen_service,
        request_service=request_service,
    )


def get_propriedade_service() -> PropriedadeService:
    return propriedade_service_singleton


def get_producao_service() -> ProducaoService:
    return producao_service_singleton


def get_safra_service() -> SafraService:
    return safra_service_singleton


def get_insumo_service() -> InsumoService:
    return insumo_service_singleton


def get_estoque_service() -> EstoqueService:
    return estoque_service_singleton


def get_operacao_service() -> OperacaoService:
    return operacao_service_singleton


def get_fitossanidade_service() -> FitossanidadeService:
    return fitossanidade_service_singleton


def get_certificacao_service() -> CertificacaoService:
    return certificacao_service_singleton


def get_comercializacao_service() -> ComercializacaoService:
    return comercializacao_service_singleton


def get_credito_service() -> CreditoService:
    return credito_service_singleton


def get_assistencia_service() -> AssistenciaService:
    return assistencia_service_singleton


def get_talhao_service() -> TalhaoService:
    return talhao_service_singleton


def get_plantio_service() -> PlantioService:
    return plantio_service_singleton


def get_colheita_service() -> ColheitaService:
    return colheita_service_singleton


def get_equipamento_service() -> EquipamentoService:
    return equipamento_service_singleton


def get_zoneamento_service() -> ZoneamentoService:
    return zoneamento_service_singleton