from __future__ import annotations

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.aeronave_service import (
    AeronaveService,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.ocorrencia_service import (
    OcorrenciaService,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.services.voo_service import (
    VooService,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.adapters.anac_adapter import (
    AnacAdapter,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.adapters.decea_adapter import (
    DeceaAdapter,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.adapters.meteorologia_adapter import (
    MeteorologiaAdapter,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.persistence.outbox import (
    InMemoryOutbox,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.repositories.inmemory_aeronave_repository import (
    InMemoryAeronaveRepository,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.repositories.inmemory_ocorrencia_repository import (
    InMemoryOcorrenciaRepository,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.repositories.inmemory_voo_repository import (
    InMemoryVooRepository,
)

_aeronave_repo = InMemoryAeronaveRepository()
_voo_repo = InMemoryVooRepository()
_ocorrencia_repo = InMemoryOcorrenciaRepository()
_outbox = InMemoryOutbox()
_anac_adapter = AnacAdapter()
_decea_adapter = DeceaAdapter()
_meteorologia_adapter = MeteorologiaAdapter()
_aeronave_service = AeronaveService(
    aeronave_repo=_aeronave_repo, outbox=_outbox, anac_adapter=_anac_adapter
)
_voo_service = VooService(
    voo_repo=_voo_repo,
    aeronave_repo=_aeronave_repo,
    outbox=_outbox,
    decea_adapter=_decea_adapter,
    meteorologia_adapter=_meteorologia_adapter,
)
_ocorrencia_service = OcorrenciaService(ocorrencia_repo=_ocorrencia_repo, outbox=_outbox)


def get_aeronave_service() -> AeronaveService:
    return _aeronave_service


def get_voo_service() -> VooService:
    return _voo_service


def get_ocorrencia_service() -> OcorrenciaService:
    return _ocorrencia_service


def get_outbox() -> InMemoryOutbox:
    return _outbox


async def reset_state_for_tests() -> None:
    _aeronave_repo._items.clear()
    _voo_repo._items.clear()
    _ocorrencia_repo._items.clear()
    await _outbox.clear()
