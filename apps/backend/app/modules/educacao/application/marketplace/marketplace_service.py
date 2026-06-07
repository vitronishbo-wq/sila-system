from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from apps.backend.app.core.audit.audit_logger import audit_log
from apps.backend.app.modules.educacao.domain.event_catalog import (
    SeatCancelled,
    SeatConfirmed,
    SeatExpired,
    SeatReserved,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_institution_repository import (
    MarketplaceInstitutionRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_vacancy_repository import (
    MarketplaceVacancyRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.seat_reservation_repository import (
    ReservationStatus,
    SeatReservationRepository,
)


class _EventBus:
    """Simple in-memory event bus without Redis dependency."""

    _handlers: dict[str, list] = {}

    @classmethod
    def subscribe(cls, event_type: str, handler):
        cls._handlers.setdefault(event_type, []).append(handler)

    @classmethod
    async def publish(cls, event_type: str, data=None):
        event = {"type": event_type, "data": data}
        for handler in cls._handlers.get(event_type, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception:
                pass


event_bus = _EventBus()


@dataclass
class StudentProfile:
    student_id: uuid.UUID
    provincia: str
    municipio: str
    bairro: str | None = None
    classe: str | None = None
    nivel_ensino: str | None = None
    turno_preferido: str | None = None


class CapacityService:
    def __init__(self, vacancy_repo: MarketplaceVacancyRepository):
        self.vacancy_repo = vacancy_repo

    async def available_slots(self, institution_id: uuid.UUID, ano_letivo: str, classe: str, turno: str) -> int:
        vacancy = await self.vacancy_repo.get_by_institution_class_shift(
            institution_id, ano_letivo, classe, turno
        )
        return vacancy.vagas_disponiveis if vacancy else 0

    async def reserve_slot(self, institution_id: uuid.UUID, ano_letivo: str, classe: str, turno: str) -> bool:
        vacancy = await self.vacancy_repo.get_by_institution_class_shift(
            institution_id, ano_letivo, classe, turno
        )
        if not vacancy or vacancy.vagas_disponiveis < 1:
            return False
        return await self.vacancy_repo.reserve_slot(vacancy.id)

    async def release_slot(self, institution_id: uuid.UUID, ano_letivo: str, classe: str, turno: str) -> bool:
        vacancy = await self.vacancy_repo.get_by_institution_class_shift(
            institution_id, ano_letivo, classe, turno
        )
        if not vacancy:
            return False
        return await self.vacancy_repo.release_slot(vacancy.id)


class MatchingService:
    def __init__(
        self,
        institution_repo: MarketplaceInstitutionRepository,
        vacancy_repo: MarketplaceVacancyRepository,
    ):
        self.institution_repo = institution_repo
        self.vacancy_repo = vacancy_repo

    async def compute_score(
        self, student: StudentProfile, institution_id: uuid.UUID, ano_letivo: str
    ) -> dict:
        institution = await self.institution_repo.get_by_institution_id(institution_id)
        if not institution:
            return {"score": 0, "motivos": ["Instituicao nao encontrada"]}

        score = 0
        motivos = []

        if institution.provincia == student.provincia:
            score += 30
            motivos.append("Mesma provincia")
        if institution.municipio == student.municipio:
            score += 20
            motivos.append("Mesmo municipio")
        if student.bairro and institution.bairro and institution.bairro == student.bairro:
            score += 10
            motivos.append("Mesmo bairro")

        if institution.status == "activa":
            score += 10
            motivos.append("Instituicao activa")

        if student.nivel_ensino and institution.nivel_ensino == student.nivel_ensino:
            score += 15
            motivos.append("Nivel de ensino compativel")

        if student.classe:
            vacancy = await self.vacancy_repo.get_by_institution_class_shift(
                institution_id, ano_letivo, student.classe, student.turno_preferido or "manha"
            )
            if vacancy and vacancy.vagas_disponiveis > 0:
                score += 15
                motivos.append(f"Vaga disponivel ({vacancy.vagas_disponiveis} vagas)")

        return {"score": min(score, 100), "motivos": motivos}

    async def find_matches(
        self, student: StudentProfile, ano_letivo: str, limit: int = 10
    ) -> list[dict]:
        institutions, _ = await self.institution_repo.search(
            provincia=student.provincia,
            municipio=student.municipio,
        )
        results = []
        for inst in institutions:
            result = await self.compute_score(student, inst.institution_id, ano_letivo)
            if result["score"] > 0:
                results.append({
                    "institution_id": inst.institution_id,
                    "nome": inst.nome,
                    "tipo": inst.tipo,
                    "nivel_ensino": inst.nivel_ensino,
                    "provincia": inst.provincia,
                    "municipio": inst.municipio,
                    "bairro": inst.bairro,
                    "turnos": inst.turnos.split(","),
                    "contactos": inst.contactos,
                    "latitude": inst.latitude,
                    "longitude": inst.longitude,
                    "score": result["score"],
                    "motivos": result["motivos"],
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]


class SeatReservationService:
    def __init__(
        self,
        reservation_repo: SeatReservationRepository,
        vacancy_repo: MarketplaceVacancyRepository,
    ):
        self.reservation_repo = reservation_repo
        self.vacancy_repo = vacancy_repo

    async def create_reservation(
        self, student_id: uuid.UUID, institution_id: uuid.UUID, classe: str, turno: str, ano_letivo: str,
        request_id: str = "",
    ) -> dict:
        vacancy = await self.vacancy_repo.get_by_institution_class_shift(
            institution_id, ano_letivo, classe, turno
        )
        if not vacancy or vacancy.vagas_disponiveis < 1:
            return {"erro": "Sem vagas disponiveis", "criada": False}

        reserved = await self.vacancy_repo.reserve_slot(vacancy.id)
        if not reserved:
            return {"erro": "Falha ao reservar vaga", "criada": False}

        model = await self.reservation_repo.create(student_id, institution_id, classe, turno, ano_letivo)

        event = SeatReserved(
            reservation_id=model.id,
            student_id=model.student_id,
            institution_id=model.institution_id,
            classe=model.classe,
            turno=model.turno,
            ano_letivo=model.ano_letivo,
            expires_at=model.expires_at,
            metadata={"request_id": request_id},
        )
        await event_bus.publish("seat_reserved", event)
        audit_log("vaga_reservada", str(model.id), request_id, {
            "student_id": str(student_id),
            "institution_id": str(institution_id),
            "classe": classe,
            "turno": turno,
        })

        return {
            "reservation_id": model.id,
            "student_id": model.student_id,
            "institution_id": model.institution_id,
            "classe": model.classe,
            "turno": model.turno,
            "status": model.status,
            "expires_at": model.expires_at.isoformat(),
            "ttl_segundos": 600,
            "criada": True,
        }

    async def confirm_reservation(self, reservation_id: uuid.UUID, request_id: str = "") -> bool:
        result = await self.reservation_repo.confirm(reservation_id)
        if result:
            model = await self.reservation_repo.get_by_id(reservation_id)
            event = SeatConfirmed(
                reservation_id=reservation_id,
                student_id=model.student_id if model else None,
                metadata={"request_id": request_id},
            )
            await event_bus.publish("seat_confirmed", event)
            audit_log("vaga_confirmada", str(reservation_id), request_id, {})
        return result

    async def cancel_reservation(self, reservation_id: uuid.UUID, request_id: str = "") -> bool:
        model = await self.reservation_repo.get_by_id(reservation_id)
        if not model or model.status != ReservationStatus.PENDING.value:
            return False
        result = await self.reservation_repo.cancel(reservation_id)
        if result:
            vacancy = await self.vacancy_repo.get_by_institution_class_shift(
                model.institution_id, model.ano_letivo, model.classe, model.turno
            )
            vacancy_released = False
            if vacancy:
                vacancy_released = await self.vacancy_repo.release_slot(vacancy.id)
            event = SeatCancelled(
                reservation_id=reservation_id,
                student_id=model.student_id,
                vacancy_released=vacancy_released,
                metadata={"request_id": request_id},
            )
            await event_bus.publish("seat_cancelled", event)
            audit_log("vaga_cancelada", str(reservation_id), request_id, {"vacancy_released": str(vacancy_released)})
        return result

    async def expire_reservation(self, reservation_id: uuid.UUID, request_id: str = "") -> bool:
        model = await self.reservation_repo.get_by_id(reservation_id)
        if not model or model.status != ReservationStatus.PENDING.value:
            return False
        now = datetime.now(timezone.utc)
        if model.expires_at > now:
            return False
        from sqlalchemy import update
        from apps.backend.app.modules.educacao.infrastructure.models.seat_reservation_model import SeatReservationModel
        stmt = (
            update(SeatReservationModel)
            .where(
                SeatReservationModel.id == reservation_id,
                SeatReservationModel.status == ReservationStatus.PENDING.value,
            )
            .values(status=ReservationStatus.EXPIRED.value)
        )
        await self.reservation_repo.session.execute(stmt)

        vacancy = await self.vacancy_repo.get_by_institution_class_shift(
            model.institution_id, model.ano_letivo, model.classe, model.turno
        )
        vacancy_released = False
        if vacancy:
            vacancy_released = await self.vacancy_repo.release_slot(vacancy.id)

        event = SeatExpired(
            reservation_id=reservation_id,
            student_id=model.student_id,
            vacancy_released=vacancy_released,
            metadata={"request_id": request_id},
        )
        await event_bus.publish("seat_expired", event)
        audit_log("vaga_expirada", str(reservation_id), request_id, {"vacancy_released": str(vacancy_released)})
        return True

    async def list_active(self, student_id: uuid.UUID) -> list:
        reservations = await self.reservation_repo.list_active_by_student(student_id)
        return [
            {
                "reservation_id": r.id,
                "student_id": r.student_id,
                "institution_id": r.institution_id,
                "classe": r.classe,
                "turno": r.turno,
                "status": r.status,
                "expires_at": r.expires_at.isoformat(),
            }
            for r in reservations
        ]
