"""Health module tests"""
import pytest
from uuid import uuid4
from datetime import date, time, timedelta

from app.modules.saude_primaria.domain.enums import AppointmentStatus, AppointmentType, PriorityLevel
from app.modules.saude_primaria.domain.models.appointment import Appointment


@pytest.mark.asyncio
async def test_create_appointment():
    """Test appointment creation"""
    appointment = Appointment(
        citizen_id=uuid4(),
        created_by=uuid4(),
        health_unit_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE,
        specialty="Clinica Geral",
        appointment_date=date.today() + timedelta(days=7),
        appointment_time=time(9, 0),
        reason="Consulta de rotina",
        priority=PriorityLevel.MEDIUM
    )
    
    assert appointment.status == AppointmentStatus.SCHEDULED
    assert appointment.is_scheduled is True
    assert appointment.is_confirmed is False


@pytest.mark.asyncio
async def test_confirm_appointment():
    """Test appointment confirmation"""
    appointment = Appointment(
        citizen_id=uuid4(),
        created_by=uuid4(),
        health_unit_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE,
        specialty="Clinica Geral",
        appointment_date=date.today() + timedelta(days=7),
        appointment_time=time(9, 0),
        reason="Consulta de rotina"
    )
    
    appointment.confirm()
    
    assert appointment.status == AppointmentStatus.CONFIRMED
    assert appointment.is_confirmed is True
    assert appointment.confirmed_at is not None


@pytest.mark.asyncio
async def test_cancel_appointment():
    """Test appointment cancellation"""
    user_id = uuid4()
    appointment = Appointment(
        citizen_id=uuid4(),
        created_by=uuid4(),
        health_unit_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE,
        specialty="Clinica Geral",
        appointment_date=date.today() + timedelta(days=7),
        appointment_time=time(9, 0),
        reason="Consulta de rotina"
    )
    
    appointment.cancel("Mudança de horário", user_id)
    
    assert appointment.status == AppointmentStatus.CANCELLED
    assert appointment.is_cancelled is True
    assert appointment.cancelled_reason == "Mudança de horário"


@pytest.mark.asyncio
async def test_appointment_validation():
    """Test appointment validation"""
    with pytest.raises(ValueError):
        Appointment(
            citizen_id=uuid4(),
            created_by=uuid4(),
            health_unit_id=uuid4(),
            appointment_type=AppointmentType.ROUTINE,
            specialty="Clinica Geral",
            appointment_date=date.today(),
            appointment_time=time(9, 0),
            reason="abc"  # Too short (< 5 chars)
        )


@pytest.mark.asyncio
async def test_appointment_to_dict():
    """Test appointment serialization"""
    appointment = Appointment(
        citizen_id=uuid4(),
        created_by=uuid4(),
        health_unit_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE,
        specialty="Clinica Geral",
        appointment_date=date.today() + timedelta(days=7),
        appointment_time=time(9, 0),
        reason="Consulta de rotina"
    )
    
    result = appointment.to_dict()
    
    assert "id" in result
    assert "citizen_id" in result
    assert "status" in result
    assert result["status"] == AppointmentStatus.SCHEDULED.value


def test_appointment_status_properties():
    """Test appointment status properties"""
    appointment = Appointment(
        citizen_id=uuid4(),
        created_by=uuid4(),
        health_unit_id=uuid4(),
        appointment_type=AppointmentType.ROUTINE,
        specialty="Clinica Geral",
        appointment_date=date.today(),
        appointment_time=time(9, 0),
        reason="Consulta de rotina"
    )
    
    assert appointment.is_scheduled is True
    assert appointment.is_confirmed is False
    assert appointment.is_completed is False
    assert appointment.is_cancelled is False
    assert appointment.is_missed is False
