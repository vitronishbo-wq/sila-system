# Logging setup (must be first)
from app.core.logging import setup_logging  # noqa

# Importa todos os models workflow e service_requests para garantir registro único
import app.modules.workflow.infrastructure.models  # noqa
from app.modules.service_requests.infrastructure.models.service_request_model import ServiceRequestModel  # noqa
from app.modules.saude.infrastructure.models.appointment_model import AppointmentModel  # noqa
from app.modules.saude.infrastructure.models.prescription_model import PrescriptionModel  # noqa
from app.modules.saude.infrastructure.models.medical_record_model import MedicalRecordModel  # noqa
from app.modules.saude.infrastructure.models.vaccine_model import VaccineModel, VaccineDoseModel  # noqa
from app.modules.saude.infrastructure.models.health_unit_model import HealthUnitModel, HealthProfessionalModel  # noqa
from app.modules.saude.infrastructure.models.exam_request_model import ExamRequestModel  # noqa
from app.modules.saude.infrastructure.models.exame_model import ExameImagemModel, ExameLaboratorialModel  # noqa
from app.modules.saude.infrastructure.models.internamento_model import InternamentoModel  # noqa
from app.modules.saude.infrastructure.models.urgencia_model import (
    AmbulanciaModel,
    FilaHospitalarModel,
    UrgenciaModel,
)  # noqa
from app.modules.saude.infrastructure.models.vigilancia_model import (
    AlertaSaudeModel,
    ControleVetorModel,
    ControleZoonoseModel,
    MonitorizacaoHidricaModel,
    NotificacaoSurtoModel,
    VigilanciaEpidemiologicaModel,
)  # noqa
from app.modules.saude.infrastructure.models.inspecao_model import (
    ApreensaoProdutoModel,
    ControleAbatePublicoModel,
    ControleQualidadeAlimentoModel,
    FiscalizacaoAlimentoModel,
    FiscalizacaoCadeiaFrioModel,
    InspecaoSanitariaModel,
    InspecaoTransporteAlimentarModel,
    LicencaSanitariaModel,
    LicencaTemporariaModel,
)  # noqa
from app.modules.saude.infrastructure.models.programa_model import (
    ProgramaHIVModel,
    ProgramaMalariaModel,
    ProgramaPreventivoModel,
)  # noqa
from app.modules.saude.infrastructure.models.rastreio_model import (
    RastreioTuberculoseModel,
    TriagemDiabetesModel,
)  # noqa
from app.modules.saude.infrastructure.models.relatorio_model import (
    AvaliacaoRiscoSanitarioModel,
    EducacaoSanitariaModel,
    EmergenciaSanitariaModel,
    RelatorioSegurancaAlimentarModel,
)  # noqa
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.module_registry import iter_bootstrap_modules, load_module_router
from app.core.settings import settings
from app.api.middleware.role_router import RoleBasedRoutingMiddleware
from app.core.observability import ObservabilityMiddleware
from app.core.database import engine
from app.modules.obras_publicas.infrastructure.observability import (
    instrument_fastapi,
    instrument_sqlalchemy,
    setup_tracing,
)

try:
    from app.modules.saude_primaria.api.router import router as saude_router
except Exception:  # pragma: no cover - defensive bootstrap path
    saude_router = APIRouter()

app = FastAPI(
    title="SILA System API",
    description="Sistema Integrado de Logística de Angola",
    version="2026.1"
)

# Observability Middleware (Global)
app.add_middleware(ObservabilityMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Role-Based Routing Middleware
app.add_middleware(RoleBasedRoutingMiddleware)


# Centralized Router (includes Health Check via public_router)
app.include_router(api_router, prefix="/api")
app.include_router(saude_router)

_mount_errors: list[str] = []
for _spec in iter_bootstrap_modules("main"):
    try:
        _router = load_module_router(_spec)
    except Exception as exc:  # pragma: no cover - defensive bootstrap path
        _mount_errors.append(f"{_spec.name}: {exc!r}")
        continue
    app.include_router(_router)

if _mount_errors:
    _details = "\n".join(f"- {item}" for item in _mount_errors)
    raise RuntimeError(
        "Failed to load one or more main-scope module routers from module_registry:\n"
        f"{_details}"
    )


@app.on_event("startup")
async def startup_obras_publicas_observability() -> None:
    setup_tracing()
    instrument_fastapi(app)
    instrument_sqlalchemy(engine)


@app.get("/")
async def root():
    return {
        "message": "SILA System API is running",
        "environment": settings.API_ENV,
        "docs": "/docs"
    }
