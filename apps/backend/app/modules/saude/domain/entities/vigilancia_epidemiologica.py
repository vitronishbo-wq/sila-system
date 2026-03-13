"""Vigilancia epidemiologica domain model."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from apps.backend.app.modules.saude.domain.enums import VigilanciaStatus


@dataclass
class VigilanciaEpidemiologica:
    """Registro de vigilancia epidemiologica."""

    health_unit_id: UUID
    reported_by: UUID
    disease_name: str
    municipality: str
    suspected_cases: int
    id: UUID = field(default_factory=uuid4)
    confirmed_cases: int = 0
    status: VigilanciaStatus = VigilanciaStatus.REPORTED
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    investigating_at: Optional[datetime] = None
    contained_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    closure_summary: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.disease_name or len(self.disease_name.strip()) < 2:
            raise ValueError("Nome da doenca invalido")
        if not self.municipality or len(self.municipality.strip()) < 2:
            raise ValueError("Municipio invalido")
        if self.suspected_cases < 0:
            raise ValueError("suspected_cases deve ser >= 0")
        if self.confirmed_cases < 0:
            raise ValueError("confirmed_cases deve ser >= 0")

    def start_investigation(self) -> None:
        if self.status != VigilanciaStatus.REPORTED:
            raise ValueError(
                f"Nao e possivel iniciar investigacao em status {self.status}"
            )
        self.status = VigilanciaStatus.INVESTIGATING
        self.investigating_at = datetime.utcnow()

    def contain(self) -> None:
        if self.status not in {
            VigilanciaStatus.REPORTED,
            VigilanciaStatus.INVESTIGATING,
        }:
            raise ValueError(f"Nao e possivel conter evento em status {self.status}")
        self.status = VigilanciaStatus.CONTAINED
        self.contained_at = datetime.utcnow()

    def close(self, summary: str) -> None:
        if self.status not in {
            VigilanciaStatus.CONTAINED,
            VigilanciaStatus.INVESTIGATING,
        }:
            raise ValueError(f"Nao e possivel encerrar evento em status {self.status}")
        if not summary or len(summary.strip()) < 5:
            raise ValueError("Resumo de encerramento invalido")
        self.status = VigilanciaStatus.CLOSED
        self.closed_at = datetime.utcnow()
        self.closure_summary = summary

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "health_unit_id": str(self.health_unit_id),
            "reported_by": str(self.reported_by),
            "disease_name": self.disease_name,
            "municipality": self.municipality,
            "suspected_cases": self.suspected_cases,
            "confirmed_cases": self.confirmed_cases,
            "status": self.status.value,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "investigating_at": (
                self.investigating_at.isoformat() if self.investigating_at else None
            ),
            "contained_at": self.contained_at.isoformat() if self.contained_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "closure_summary": self.closure_summary,
        }
