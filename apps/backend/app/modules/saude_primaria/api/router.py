"""Saúde Primária API Router"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from uuid import UUID
from datetime import date, time

from app.modules.saude_primaria.application.services.appointment_service import AppointmentService
from app.modules.saude_primaria.application.services.prescription_service import PrescriptionService
from app.modules.saude_primaria.application.services.medical_record_service import MedicalRecordService
from app.modules.saude_primaria.application.services.vaccine_service import VaccineService
from app.modules.saude_primaria.application.services.health_unit_service import HealthUnitService
from app.modules.saude_primaria.api.deps import (
    get_appointment_service,
    get_prescription_service,
    get_medical_record_service,
    get_vaccine_service,
    get_health_unit_service,
)
from app.modules.saude_primaria.api.schemas.appointment_schema import (
    AppointmentCreateSchema,
    AppointmentResponseSchema,
    AppointmentConfirmSchema,
    AppointmentCancelSchema,
    AppointmentRescheduleSchema,
    AppointmentAssignSchema,
)
from app.modules.saude_primaria.api.schemas.prescription_schema import (
    PrescriptionCreateSchema,
    PrescriptionResponseSchema,
    PrescriptionDispenseSchema,
    PrescriptionCancelSchema,
)
from app.modules.saude_primaria.api.schemas.medical_record_schema import (
    MedicalRecordCreateSchema,
    MedicalRecordResponseSchema,
    DiagnosisAddSchema,
    VitalSignsUpdateSchema,
)
from app.modules.saude_primaria.api.schemas.vaccine_schema import (
    VaccineDoseCreateSchema,
    VaccineDoseResponseSchema,
    VaccineDoseScheduleSchema,
    VaccineReactionSchema,
)
from app.modules.saude_primaria.api.schemas.health_unit_schema import (
    HealthUnitCreateSchema,
    HealthUnitResponseSchema,
    HealthUnitSpecialtySchema,
    HealthProfessionalRegisterSchema,
    HealthProfessionalResponseSchema,
)
from app.modules.saude_primaria.domain.enums import AppointmentType, PriorityLevel

# Create router
router = APIRouter(
    prefix="/api/v1/saude",
    tags=["Saúde Primária"],
    responses={404: {"description": "Not found"}},
)

# ==================== APPOINTMENTS ====================

@router.post("/appointments", response_model=AppointmentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    schema: AppointmentCreateSchema,
    service: AppointmentService = Depends(get_appointment_service)
):
    """Create new appointment"""
    try:
        appointment = await service.create_appointment(
            citizen_id=schema.citizen_id,
            created_by=schema.citizen_id,  # TODO: Get from auth
            health_unit_id=schema.health_unit_id,
            appointment_type=AppointmentType(schema.appointment_type),
            specialty=schema.specialty,
            appointment_date=schema.appointment_date,
            appointment_time=schema.appointment_time,
            reason=schema.reason,
            priority=PriorityLevel(schema.priority),
            doctor_id=schema.doctor_id,
            symptoms=schema.symptoms,
            notes=schema.notes
        )
        return appointment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/appointments/{appointment_id}", response_model=AppointmentResponseSchema)
async def get_appointment(
    appointment_id: UUID,
    service: AppointmentService = Depends(get_appointment_service)
):
    """Get appointment details"""
    appointment = await service.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment.to_dict()


@router.get("/appointments/citizen/{citizen_id}", response_model=List[AppointmentResponseSchema])
async def list_citizen_appointments(
    citizen_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: AppointmentService = Depends(get_appointment_service)
):
    """List citizen appointments"""
    appointments = await service.list_citizen_appointments(citizen_id, skip, limit)
    return [a.to_dict() for a in appointments]


@router.post("/appointments/{appointment_id}/confirm", response_model=AppointmentResponseSchema)
async def confirm_appointment(
    appointment_id: UUID,
    service: AppointmentService = Depends(get_appointment_service)
):
    """Confirm appointment"""
    try:
        appointment = await service.confirm_appointment(appointment_id)
        return appointment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/appointments/{appointment_id}/cancel", response_model=AppointmentResponseSchema)
async def cancel_appointment(
    appointment_id: UUID,
    schema: AppointmentCancelSchema,
    service: AppointmentService = Depends(get_appointment_service)
):
    """Cancel appointment"""
    try:
        appointment = await service.cancel_appointment(appointment_id, schema.reason, appointment_id)  # TODO: Get user_id from auth
        return appointment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/appointments/{appointment_id}/reschedule", response_model=AppointmentResponseSchema)
async def reschedule_appointment(
    appointment_id: UUID,
    schema: AppointmentRescheduleSchema,
    service: AppointmentService = Depends(get_appointment_service)
):
    """Reschedule appointment"""
    try:
        appointment = await service.reschedule_appointment(
            appointment_id,
            schema.new_date,
            schema.new_time,
            appointment_id  # TODO: Get user_id from auth
        )
        return appointment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/appointments/{appointment_id}/assign", response_model=AppointmentResponseSchema)
async def assign_doctor(
    appointment_id: UUID,
    schema: AppointmentAssignSchema,
    service: AppointmentService = Depends(get_appointment_service)
):
    """Assign doctor to appointment"""
    try:
        appointment = await service.assign_doctor(appointment_id, schema.doctor_id, appointment_id)  # TODO: Get user_id from auth
        return appointment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== PRESCRIPTIONS ====================

@router.post("/prescriptions", response_model=PrescriptionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_prescription(
    schema: PrescriptionCreateSchema,
    service: PrescriptionService = Depends(get_prescription_service)
):
    """Create new prescription"""
    try:
        items_data = [item.model_dump() for item in schema.items]
        prescription = await service.create_prescription(
            citizen_id=schema.citizen_id,
            doctor_id=schema.doctor_id,
            health_unit_id=schema.health_unit_id,
            items=items_data,
            appointment_id=schema.appointment_id,
            clinical_notes=schema.clinical_notes,
            recommendations=schema.recommendations
        )
        return prescription.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/prescriptions/{prescription_id}", response_model=PrescriptionResponseSchema)
async def get_prescription(
    prescription_id: UUID,
    service: PrescriptionService = Depends(get_prescription_service)
):
    """Get prescription details"""
    prescription = await service.get_prescription(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription.to_dict()


@router.get("/prescriptions/citizen/{citizen_id}", response_model=List[PrescriptionResponseSchema])
async def list_citizen_prescriptions(
    citizen_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: PrescriptionService = Depends(get_prescription_service)
):
    """List citizen prescriptions"""
    prescriptions = await service.list_citizen_prescriptions(citizen_id, skip, limit)
    return [p.to_dict() for p in prescriptions]


@router.post("/prescriptions/{prescription_id}/dispense", response_model=PrescriptionResponseSchema)
async def dispense_prescription(
    prescription_id: UUID,
    schema: PrescriptionDispenseSchema,
    service: PrescriptionService = Depends(get_prescription_service)
):
    """Dispense prescription"""
    try:
        prescription = await service.dispense_prescription(prescription_id, schema.items_dispensed)
        return prescription.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/prescriptions/{prescription_id}/cancel", response_model=PrescriptionResponseSchema)
async def cancel_prescription(
    prescription_id: UUID,
    schema: PrescriptionCancelSchema,
    service: PrescriptionService = Depends(get_prescription_service)
):
    """Cancel prescription"""
    try:
        prescription = await service.cancel_prescription(prescription_id, schema.reason, prescription_id)  # TODO: Get user_id from auth
        return prescription.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== MEDICAL RECORDS ====================

@router.post("/medical-records", response_model=MedicalRecordResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_medical_record(
    schema: MedicalRecordCreateSchema,
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    """Create new medical record"""
    try:
        record = await service.create_medical_record(
            citizen_id=schema.citizen_id,
            doctor_id=schema.doctor_id,
            health_unit_id=schema.health_unit_id,
            chief_complaint=schema.chief_complaint,
            appointment_id=schema.appointment_id,
            history_of_present_illness=schema.history_of_present_illness,
            past_medical_history=schema.past_medical_history,
            family_history=schema.family_history,
            social_history=schema.social_history,
            allergies=schema.allergies,
            physical_exam=schema.physical_exam,
            treatment_plan=schema.treatment_plan,
            recommendations=schema.recommendations
        )
        return record.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/medical-records/{record_id}", response_model=MedicalRecordResponseSchema)
async def get_medical_record(
    record_id: UUID,
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    """Get medical record details"""
    record = await service.get_medical_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record.to_dict()


@router.get("/medical-records/citizen/{citizen_id}", response_model=List[MedicalRecordResponseSchema])
async def list_citizen_medical_records(
    citizen_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    """List citizen medical records"""
    records = await service.list_citizen_records(citizen_id, skip, limit)
    return [r.to_dict() for r in records]


@router.post("/medical-records/{record_id}/diagnoses", response_model=MedicalRecordResponseSchema)
async def add_diagnosis(
    record_id: UUID,
    schema: DiagnosisAddSchema,
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    """Add diagnosis to medical record"""
    try:
        record = await service.add_diagnosis(record_id, schema.diagnosis, schema.code)
        return record.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/medical-records/{record_id}/vital-signs", response_model=MedicalRecordResponseSchema)
async def update_vital_signs(
    record_id: UUID,
    schema: VitalSignsUpdateSchema,
    service: MedicalRecordService = Depends(get_medical_record_service)
):
    """Update vital signs"""
    try:
        from app.modules.saude_primaria.domain.models.medical_record import VitalSigns
        vitals = VitalSigns(**schema.vital_signs.model_dump())
        record = await service.update_vital_signs(record_id, vitals)
        return record.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== VACCINES ====================

@router.post("/vaccine-doses", response_model=VaccineDoseResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_vaccine_dose(
    schema: VaccineDoseCreateSchema,
    service: VaccineService = Depends(get_vaccine_service)
):
    """Register vaccine dose"""
    try:
        dose = await service.register_vaccine_dose(
            citizen_id=schema.citizen_id,
            vaccine_id=schema.vaccine_id,
            health_unit_id=schema.health_unit_id,
            applied_by=schema.health_unit_id,  # TODO: Get from auth
            dose_number=schema.dose_number,
            batch_number=schema.batch_number,
            application_date=schema.application_date,
            next_dose_date=schema.next_dose_date
        )
        return dose.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== HEALTH UNITS ====================

@router.post("/health-units", response_model=HealthUnitResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_health_unit(
    schema: HealthUnitCreateSchema,
    service: HealthUnitService = Depends(get_health_unit_service)
):
    """Create new health unit"""
    try:
        from app.modules.saude_primaria.domain.enums import HealthUnitType
        unit = await service.create_health_unit(
            code=schema.code,
            name=schema.name,
            unit_type=HealthUnitType(schema.unit_type),
            province=schema.province,
            municipality=schema.municipality,
            address=schema.address,
            commune=schema.commune,
            phone=schema.phone,
            email=schema.email,
            beds=schema.beds,
            has_emergency=schema.has_emergency,
            has_laboratory=schema.has_laboratory,
            has_pharmacy=schema.has_pharmacy
        )
        return unit.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health-units/{unit_id}", response_model=HealthUnitResponseSchema)
async def get_health_unit(
    unit_id: UUID,
    service: HealthUnitService = Depends(get_health_unit_service)
):
    """Get health unit details"""
    unit = await service.get_health_unit(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Health unit not found")
    return unit.to_dict()


@router.get("/health-units/municipality/{municipality}", response_model=List[HealthUnitResponseSchema])
async def list_municipal_health_units(
    municipality: str,
    service: HealthUnitService = Depends(get_health_unit_service)
):
    """List health units by municipality"""
    units = await service.list_municipal_units(municipality)
    return [u.to_dict() for u in units]


@router.post("/health-units/{unit_id}/professionals", response_model=HealthProfessionalResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_professional(
    unit_id: UUID,
    schema: HealthProfessionalRegisterSchema,
    service: HealthUnitService = Depends(get_health_unit_service)
):
    """Register health professional"""
    try:
        professional = await service.register_professional(
            user_id=schema.user_id,
            health_unit_id=unit_id,
            license_number=schema.license_number,
            specialization=schema.specialization
        )
        return {
            "id": professional.id,
            "user_id": professional.user_id,
            "health_unit_id": professional.health_unit_id,
            "license_number": professional.license_number,
            "specialization": professional.specialization,
            "created_at": professional.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
