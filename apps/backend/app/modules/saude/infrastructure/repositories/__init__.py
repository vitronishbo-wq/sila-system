from app.modules.saude.infrastructure.repositories.appointment_repository import (
    AppointmentRepository,
)
from app.modules.saude.infrastructure.repositories.health_unit_repository import (
    HealthUnitRepository,
)
from app.modules.saude.infrastructure.repositories.medical_record_repository import (
    MedicalRecordRepository,
)

__all__ = [
    "AppointmentRepository",
    "HealthUnitRepository",
    "MedicalRecordRepository",
]
