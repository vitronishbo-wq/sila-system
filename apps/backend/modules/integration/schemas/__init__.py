# modules/integration/schemas/__init__.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class CitizenLegacy(BaseModel):
    """Modelo de cidadão vindo de sistema legacy"""
    legacy_id: str = Field(..., description="ID no sistema antigo")
    full_name: str
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    birth_date: str = Field(..., description="Formato DD/MM/AAAA ou YYYY-MM-DD")
    birth_province: str
    birth_municipality: str
    current_province: Optional[str] = None
    current_municipality: Optional[str] = None
    gender: str = Field(..., pattern="^(Masculino|Feminino)$")
    marital_status: Optional[str] = None
    legacy_source: str = Field(..., description="ex: 'BUAP_Luanda', 'SISPROV_Huila'")
    extra_data: Optional[Dict[str, Any]] = None


class CitizenLegacyBatch(BaseModel):
    citizens: List[CitizenLegacy] = Field(..., max_items=10000)


class CitizenLegacyResponse(BaseModel):
    sila_id: UUID
    bi_number: str
    legacy_id: str
    status: str = Field(..., description="migrated | duplicate | error")
    message: Optional[str] = None
    migrated_at: datetime


class MigrationStatusResponse(BaseModel):
    total_legacy_records: int
    total_migrated: int
    total_duplicates: int
    total_errors: int
    percentage_complete: float
    last_migration_at: Optional[datetime]
    provinces_status: Dict[str, Dict[str, Any]]  # ex: {"Luanda": {"migrated": 450000, "pending": 12000}}


class SyncProvinceRequest(BaseModel):
    force_full_sync: bool = False
    modules: List[str] = Field(
        default=["citizens", "births", "marriages", "deaths"],
        description="Módulos a sincronizar"
    )


class SyncProvinceResponse(BaseModel):
    province_id: str
    records_processed: int
    records_added: int
    records_updated: int
    errors: int
    started_at: datetime
    completed_at: datetime
    status: str  # "completed" | "failed" | "partial"


__all__ = [
    "CitizenLegacy",
    "CitizenLegacyBatch",
    "CitizenLegacyResponse",
    "MigrationStatusResponse",
    "SyncProvinceRequest",
    "SyncProvinceResponse",
]