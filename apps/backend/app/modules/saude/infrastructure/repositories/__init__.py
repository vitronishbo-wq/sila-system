from apps.backend.app.modules.saude.infrastructure.repositories.appointment_repository import (
    AppointmentRepository,
)
from apps.backend.app.modules.saude.infrastructure.repositories.health_unit_repository import (
    HealthUnitRepository,
)
from apps.backend.app.modules.saude.infrastructure.repositories.medical_record_repository import (
    MedicalRecordRepository,
)

__all__ = ["AppointmentRepository", "HealthUnitRepository", "MedicalRecordRepository"]
