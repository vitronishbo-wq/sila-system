from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.health.repository import HealthRepository
from modules.health.schemas.api_schemas import (
    AppointmentCreate,
    AppointmentResponse,
    CancelAppointmentResponse,
    HealthRecordCreate,
    HealthRecordResponse,
    HealthRecordsListResponse,
    HealthRecordUpdate,
    HealthServiceItem,
    HealthServicesResponse,
    MedicalRecordResponse,
    UserAppointmentsResponse,
)


class HealthService:
    def __init__(self, db: AsyncSession):
        self.repository = HealthRepository(db)
        self.db = db

    async def create_health_record(
        self, user_id: UUID, payload: HealthRecordCreate
    ) -> HealthRecordResponse:
        record = await self.repository.create_health_record(
            user_id=user_id,
            patient_name=payload.patient_name,
            diagnosis=payload.diagnosis,
            notes=payload.notes,
        )
        return HealthRecordResponse(
            id=record.id,
            patient_name=record.patient_name,
            diagnosis=record.diagnosis,
            notes=record.notes,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    async def get_health_record(
        self, record_id: UUID
    ) -> Optional[HealthRecordResponse]:
        record = await self.repository.get_health_record(record_id)
        if not record:
            return None
        return HealthRecordResponse(
            id=record.id,
            patient_name=record.patient_name,
            diagnosis=record.diagnosis,
            notes=record.notes,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    async def list_health_records(
        self, user_id: Optional[UUID] = None, skip: int = 0, limit: int = 100
    ) -> HealthRecordsListResponse:
        records = await self.repository.list_health_records(
            user_id=user_id, skip=skip, limit=limit
        )
        total = await self.repository.count_health_records(user_id=user_id)
        items = [
            HealthRecordResponse(
                id=r.id,
                patient_name=r.patient_name,
                diagnosis=r.diagnosis,
                notes=r.notes,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in records
        ]
        return HealthRecordsListResponse(items=items, total=total)

    async def update_health_record(
        self, record_id: UUID, payload: HealthRecordUpdate
    ) -> Optional[HealthRecordResponse]:
        record = await self.repository.update_health_record(
            record_id=record_id,
            patient_name=payload.patient_name,
            diagnosis=payload.diagnosis,
            notes=payload.notes,
        )
        if not record:
            return None
        return HealthRecordResponse(
            id=record.id,
            patient_name=record.patient_name,
            diagnosis=record.diagnosis,
            notes=record.notes,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    async def delete_health_record(self, record_id: UUID) -> bool:
        return await self.repository.delete_health_record(record_id)

    async def list_health_services(
        self, category: Optional[str] = None, status_filter: Optional[str] = None
    ) -> HealthServicesResponse:
        services = await self.repository.list_health_services(
            category=category, status_filter=status_filter
        )
        total = await self.repository.count_health_services(
            category=category, status_filter=status_filter
        )
        items = [
            HealthServiceItem(
                id=str(s.id),
                name=s.name,
                category=s.category,
                status=s.status,
            )
            for s in services
        ]
        return HealthServicesResponse(services=items, total=total)

    async def create_appointment(
        self, user_id: UUID, payload: AppointmentCreate
    ) -> AppointmentResponse:
        service = await self.repository.get_health_service(UUID(payload.service_id))
        if not service:
            raise ValueError("Health service not found")
        appointment = await self.repository.create_appointment(
            user_id=user_id,
            service_id=UUID(payload.service_id),
            scheduled_date=payload.scheduled_date,
            notes=payload.notes,
        )
        return AppointmentResponse(
            id=str(appointment.id),
            service_id=str(appointment.service_id),
            scheduled_date=appointment.scheduled_date,
            notes=appointment.notes,
            status=appointment.status,
            created_at=appointment.created_at,
        )

    async def list_user_appointments(
        self,
        user_id: UUID,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> UserAppointmentsResponse:
        appointments = await self.repository.list_user_appointments(
            user_id=user_id, status_filter=status_filter, skip=skip, limit=limit
        )
        total = await self.repository.count_user_appointments(
            user_id=user_id, status_filter=status_filter
        )
        items = [
            AppointmentResponse(
                id=str(a.id),
                service_id=str(a.service_id),
                scheduled_date=a.scheduled_date,
                notes=a.notes,
                status=a.status,
                created_at=a.created_at,
            )
            for a in appointments
        ]
        return UserAppointmentsResponse(appointments=items, total=total)

    async def cancel_appointment(
        self, user_id: UUID, appointment_id: str
    ) -> Optional[CancelAppointmentResponse]:
        appointment = await self.repository.get_appointment(UUID(appointment_id))
        if not appointment:
            return None
        if appointment.user_id != user_id:
            raise ValueError("Appointment does not belong to user")
        cancelled = await self.repository.cancel_appointment(UUID(appointment_id))
        if not cancelled:
            return None
        return CancelAppointmentResponse(
            message="Appointment cancelled successfully", appointment_id=appointment_id
        )

    async def get_medical_record(
        self, user_id: UUID, appointment_id: str
    ) -> Optional[MedicalRecordResponse]:
        appointment = await self.repository.get_appointment(UUID(appointment_id))
        if not appointment or appointment.user_id != user_id:
            raise ValueError("Appointment does not belong to user")
        medical_record = await self.repository.get_medical_record_by_appointment(
            UUID(appointment_id)
        )
        if not medical_record:
            return None
        return MedicalRecordResponse(
            id=str(medical_record.id),
            appointment_id=appointment_id,
            diagnosis=medical_record.diagnosis,
            treatment=medical_record.treatment,
            notes=medical_record.notes,
            created_at=medical_record.created_at,
        )


__all__ = ["HealthService"]
