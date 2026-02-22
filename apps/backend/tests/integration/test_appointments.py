# backend/tests/test_appointments.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from core.db.session import get_db
from modules.appointments.schemas import AppointmentCreate


@pytest.mark.asyncio
async def test_create_appointment(
    async_client: AsyncClient, db_session: AsyncSession, test_user
):
    payload = {
        "title": "Consulta médica",
        "description": "Consulta de rotina",
        "date": "2025-09-20T10:00:00",
        "user_id": str(test_user.id),
    }

    response = await async_client.post("/appointments/", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["user_id"] == str(test_user.id)


@pytest.mark.asyncio
async def test_get_appointment(
    async_client: AsyncClient, db_session: AsyncSession, test_user, test_appointment
):
    response = await async_client.get(f"/appointments/{test_appointment.id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == str(test_appointment.id)
    assert data["title"] == test_appointment.title


@pytest.mark.asyncio
async def test_list_appointments(
    async_client: AsyncClient, db_session: AsyncSession, test_user, test_appointment
):
    response = await async_client.get("/appointments/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert any(app["id"] == str(test_appointment.id) for app in data)


@pytest.mark.asyncio
async def test_update_appointment(
    async_client: AsyncClient, db_session: AsyncSession, test_user, test_appointment
):
    update_payload = {
        "title": "Consulta atualizada",
        "description": "Descrição atualizada",
    }
    response = await async_client.put(
        f"/appointments/{test_appointment.id}", json=update_payload
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == update_payload["title"]
    assert data["description"] == update_payload["description"]


@pytest.mark.asyncio
async def test_delete_appointment(
    async_client: AsyncClient, db_session: AsyncSession, test_user, test_appointment
):
    response = await async_client.delete(f"/appointments/{test_appointment.id}")
    assert response.status_code == 204

    # Verifica se foi realmente deletado
    response = await async_client.get(f"/appointments/{test_appointment.id}")
    assert response.status_code == 404
