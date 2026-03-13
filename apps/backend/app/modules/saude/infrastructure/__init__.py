"""Saude infrastructure package."""

from app.modules.saude.infrastructure.models import (
    AppointmentModel,
    HealthUnitModel,
    InternamentoModel,
    MedicalRecordModel,
    VaccineDoseModel,
)

__all__ = [
    "AppointmentModel",
    "HealthUnitModel",
    "InternamentoModel",
    "MedicalRecordModel",
    "VaccineDoseModel",
]
