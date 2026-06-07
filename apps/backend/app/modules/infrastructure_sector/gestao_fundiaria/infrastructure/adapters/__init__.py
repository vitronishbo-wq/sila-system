from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.agricultura_service_adapter import (
    AgriculturaServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.ambiente_service_adapter import (
    AmbienteServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.citizen_service_adapter import (
    CitizenServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.geosampa_service_adapter import (
    GeosampaServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.justica_service_adapter import (
    JusticaServiceAdapter,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.adapters.request_service_adapter import (
    RequestServiceAdapter,
)

__all__ = [
    "CitizenServiceAdapter",
    "RequestServiceAdapter",
    "AgriculturaServiceAdapter",
    "AmbienteServiceAdapter",
    "JusticaServiceAdapter",
    "GeosampaServiceAdapter",
]
