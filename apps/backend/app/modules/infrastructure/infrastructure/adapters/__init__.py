from apps.backend.app.modules.infrastructure.infrastructure.adapters.aguas_saneamento_service_adapter import (
    AguasSaneamentoServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.ambiente_service_adapter import (
    AmbienteServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.citizen_service_adapter import (
    CitizenServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.financas_publicas_adapter import (
    FinancasPublicasAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.financas_publicas_service_adapter import (
    FinancasPublicasServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.gestao_fundiaria_service_adapter import (
    GestaoFundiariaServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.justica_service_adapter import (
    JusticaServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.request_service_adapter import (
    RequestServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.service_requests_service_adapter import (
    ServiceRequestsServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.tcu_adapter import TCUAdapter
from apps.backend.app.modules.infrastructure.infrastructure.adapters.transportes_service_adapter import (
    TransportesServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.urbanismo_habitacao_service_adapter import (
    UrbanismoHabitacaoServiceAdapter,
)
from apps.backend.app.modules.infrastructure.infrastructure.adapters.workflow_service_adapter import (
    WorkflowServiceAdapter,
)

__all__ = [
    "CitizenServiceAdapter",
    "RequestServiceAdapter",
    "GestaoFundiariaServiceAdapter",
    "FinancasPublicasServiceAdapter",
    "FinancasPublicasAdapter",
    "AmbienteServiceAdapter",
    "JusticaServiceAdapter",
    "UrbanismoHabitacaoServiceAdapter",
    "TransportesServiceAdapter",
    "AguasSaneamentoServiceAdapter",
    "WorkflowServiceAdapter",
    "ServiceRequestsServiceAdapter",
    "TCUAdapter",
]
