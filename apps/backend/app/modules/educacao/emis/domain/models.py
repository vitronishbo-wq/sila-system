from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class SyncDirection(str, Enum):
    PUSH = "push"
    PULL = "pull"
    BIDIRECTIONAL = "bidirectional"


class SyncStatus(str, Enum):
    PENDING = "pending"
    SYNCING = "syncing"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"
    DEAD_LETTER = "dead_letter"
    SKIPPED = "skipped"


class SyncEntityType(str, Enum):
    ENROLLMENT = "enrollment"
    STUDENT = "student"
    INSTITUTION = "institution"
    ACADEMIC_RECORD = "academic_record"
    TRANSFER = "transfer"
    CERTIFICATE = "certificate"


class EmisStudent:
    def __init__(
        self,
        *,
        student_id: UUID,
        full_name: str,
        document_id: str,
        birth_date: date,
        gender: str,
        province: str,
        municipio: str,
        parent_name: Optional[str] = None,
        parent_contact: Optional[str] = None,
        address: Optional[str] = None,
        nacionalidade: str = "ANGOLANA",
        emis_code: Optional[str] = None,
        emis_synced_at: Optional[datetime] = None,
    ):
        self.student_id = student_id
        self.full_name = full_name
        self.document_id = document_id
        self.birth_date = birth_date
        self.gender = gender
        self.province = province
        self.municipio = municipio
        self.parent_name = parent_name
        self.parent_contact = parent_contact
        self.address = address
        self.nacionalidade = nacionalidade
        self.emis_code = emis_code
        self.emis_synced_at = emis_synced_at


class EmisEnrollment:
    def __init__(
        self,
        *,
        enrollment_id: UUID,
        student_id: UUID,
        institution_id: UUID,
        institution_name: str,
        academic_year: str,
        grade: str,
        shift: str,
        status: str,
        started_at: datetime,
        ended_at: Optional[datetime] = None,
        emis_code: Optional[str] = None,
        emis_synced_at: Optional[datetime] = None,
    ):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.institution_id = institution_id
        self.institution_name = institution_name
        self.academic_year = academic_year
        self.grade = grade
        self.shift = shift
        self.status = status
        self.started_at = started_at
        self.ended_at = ended_at
        self.emis_code = emis_code
        self.emis_synced_at = emis_synced_at


class EmisInstitution:
    def __init__(
        self,
        *,
        institution_id: UUID,
        name: str,
        institution_type: str,
        nivel_ensino: str,
        province: str,
        municipio: str,
        bairro: Optional[str] = None,
        contactos: Optional[str] = None,
        turnos: Optional[str] = None,
        emis_code: Optional[str] = None,
        emis_synced_at: Optional[datetime] = None,
    ):
        self.institution_id = institution_id
        self.name = name
        self.institution_type = institution_type
        self.nivel_ensino = nivel_ensino
        self.province = province
        self.municipio = municipio
        self.bairro = bairro
        self.contactos = contactos
        self.turnos = turnos
        self.emis_code = emis_code
        self.emis_synced_at = emis_synced_at


class SyncLogEntry:
    def __init__(
        self,
        *,
        entity_type: SyncEntityType,
        entity_id: str,
        direction: SyncDirection,
        status: SyncStatus,
        payload: Optional[dict] = None,
        response: Optional[dict] = None,
        error: Optional[str] = None,
        duration_ms: int = 0,
        retry_count: int = 0,
        next_retry_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
    ):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.direction = direction
        self.status = status
        self.payload = payload
        self.response = response
        self.error = error
        self.duration_ms = duration_ms
        self.retry_count = retry_count
        self.next_retry_at = next_retry_at
        self.created_at = created_at or datetime.utcnow()

    def is_retryable(self) -> bool:
        return self.retry_count < 3

    def mark_retry(self, error: str, next_retry_at: datetime) -> "SyncLogEntry":
        self.status = SyncStatus.RETRY
        self.error = error
        self.retry_count += 1
        self.next_retry_at = next_retry_at
        return self

    def mark_dead_letter(self, error: str) -> "SyncLogEntry":
        self.status = SyncStatus.DEAD_LETTER
        self.error = error
        return self
