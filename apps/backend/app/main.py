# Importa todos os models workflow e service_requests para garantir registro único
import app.modules.workflow.infrastructure.models  # noqa
from app.modules.service_requests.infrastructure.models.service_request_model import ServiceRequestModel  # noqa
from app.modules.saude_primaria.infrastructure.models.appointment_model import AppointmentModel  # noqa
from app.modules.saude_primaria.infrastructure.models.prescription_model import PrescriptionModel  # noqa
from app.modules.saude_primaria.infrastructure.models.medical_record_model import MedicalRecordModel  # noqa
from app.modules.saude_primaria.infrastructure.models.vaccine_model import VaccineModel, VaccineDoseModel  # noqa
from app.modules.saude_primaria.infrastructure.models.health_unit_model import HealthUnitModel, HealthProfessionalModel  # noqa
from app.modules.saude_primaria.infrastructure.models.exam_request_model import ExamRequestModel  # noqa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.settings import settings
from app.api.middleware.role_router import RoleBasedRoutingMiddleware

app = FastAPI(
    title="SILA System API",
    description="Sistema Integrado de Logística de Angola",
    version="2026.1"
)


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


# Centralized Router
app.include_router(api_router, prefix="/api")

# Import and register workflow router explicitly (only here)
from app.modules.workflow.api.router import router as workflow_router
app.include_router(workflow_router)

# Import and register saude_primaria router (temporarily disabled due to missing deps)
# TODO: Fix saude_primaria deps before re-enabling
# from app.modules.saude_primaria.api.router import router as saude_router
# app.include_router(saude_router)

# Import and register BI module router (temporarily disabled due to missing deps)
# TODO: Fix BI deps before re-enabling
# from app.modules.bi.api.router import router as bi_router
# app.include_router(bi_router)

# Import and register statistics router
from app.modules.statistics.api.router import router as statistics_router
app.include_router(statistics_router)

@app.get("/")
async def root():
    return {
        "message": "SILA System API is running",
        "environment": settings.API_ENV,
        "docs": "/docs"
    }