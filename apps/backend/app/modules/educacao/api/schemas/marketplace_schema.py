from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SchoolCard(BaseModel):
    institution_id: UUID
    nome: str
    tipo: str
    nivel_ensino: str
    provincia: str
    municipio: str
    bairro: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    turnos: list[str] = Field(default_factory=lambda: ["manha", "tarde"])
    contactos: str | None = None
    status: str = "activa"
    vagas_disponiveis: int = 0
    propina: float | None = None


class VacancyResult(BaseModel):
    institution_id: UUID
    nome_escola: str
    ano_letivo: str
    classe: str
    turno: str
    vagas_disponiveis: int
    vagas_totais: int


class SchoolSearchResult(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[SchoolCard]


class VacancySearchResult(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[VacancyResult]


class MatchingScore(BaseModel):
    escola: SchoolCard
    score: int = Field(..., ge=0, le=100)
    motivos: list[str]


class RecomendacaoResult(BaseModel):
    student_id: UUID
    total: int
    recomendacoes: list[MatchingScore]


class SeatReservationCreate(BaseModel):
    student_id: UUID
    institution_id: UUID
    classe: str
    turno: str = "manha"
    ano_letivo: str


class SeatReservationResponse(BaseModel):
    reservation_id: UUID
    student_id: UUID
    institution_id: UUID
    classe: str
    turno: str
    status: str
    expires_at: datetime
    ttl_segundos: int = 600
